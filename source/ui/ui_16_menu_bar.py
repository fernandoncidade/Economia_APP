from PySide6.QtWidgets import QMenuBar, QTextEdit
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import QCoreApplication
from html import escape
from .ui_15_export_pdf import amort_table_to_html
from .ui_19_exibir_sobre import exibir_sobre
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_menu_bar(self):
    tr = QCoreApplication.translate
    try:
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu(tr("App", "Arquivos"))
        export_current_action = QAction(tr("App", "Exportar Atual"), self)
        export_all_action = QAction(tr("App", "Exportar Todos"), self)
        file_menu.addAction(export_current_action)
        file_menu.addAction(export_all_action)

        config_menu = menubar.addMenu(tr("App", "Configuração"))
        idiomas_menu = config_menu.addMenu(tr("App", "Idiomas"))

        action_pt = QAction(tr("App", "Português (Brasil)"), self)
        action_en = QAction(tr("App", "English (United States)"), self)
        action_pt.setCheckable(True)
        action_en.setCheckable(True)
        ag = QActionGroup(self)
        ag.setExclusive(True)
        ag.addAction(action_pt)
        ag.addAction(action_en)
        idiomas_menu.addAction(action_pt)
        idiomas_menu.addAction(action_en)

        def _get_gerenciador():
            return getattr(self, "gerenciador", None) or getattr(self, "gerenciador_traducao", None)

        def _update_language_checks(codigo):
            try:
                action_pt.setChecked(codigo == "pt_BR")
                action_en.setChecked(codigo == "en_US")

            except Exception:
                action_pt.setChecked(False)
                action_en.setChecked(False)

        gm = _get_gerenciador()
        try:
            if gm and hasattr(gm, "obter_idioma_atual"):
                current = gm.obter_idioma_atual()
                _update_language_checks(current)

                try:
                    gm.idioma_alterado.connect(_update_language_checks)

                except Exception:
                    pass

        except Exception:
            _update_language_checks(None)

        config_menu.addSeparator()

        font_config_action = QAction(tr("App", "Configurar Fontes"), self)
        def open_font_config():
            try:
                from .ui_21_font_config_dialog import FontConfigDialog
                dialog = FontConfigDialog(self)
                if dialog.exec():
                    for i in range(self.tabs.count()):
                        tab = self.tabs.widget(i)
                        result_widget = getattr(self, f"interest_result", None) or \
                                       getattr(self, f"annuity_result", None) or \
                                       getattr(self, f"grad_result", None) or \
                                       getattr(self, f"rate_equiv_result", None) or \
                                       getattr(self, f"rate_real_result", None) or \
                                       getattr(self, f"invest_result", None) or \
                                       getattr(self, f"deprec_result", None)

                        if hasattr(result_widget, 'refresh_all_fonts'):
                            result_widget.refresh_all_fonts()

            except Exception as e:
                logger.error(f"Erro ao abrir configuração de fontes: {e}", exc_info=True)

        font_config_action.triggered.connect(open_font_config)
        config_menu.addAction(font_config_action)

        options_menu = menubar.addMenu(tr("App", "Opções"))

        about_action = QAction(tr("App", "Sobre"), self)
        about_action.triggered.connect(lambda: exibir_sobre(self))
        options_menu.addAction(about_action)

        def set_language(code):
            gm = getattr(self, "gerenciador", None)
            if gm:
                gm.definir_idioma(code)
                _update_language_checks(code)

        action_pt.triggered.connect(lambda: set_language("pt_BR"))
        action_en.triggered.connect(lambda: set_language("en_US"))

        def export_all():
            sections = []

            def add_section(title, widget):
                if not widget:
                    return

                text = widget.toPlainText().strip()
                if text:
                    sections.append((title, text))

            add_section(tr("App", "Juros (Simples/Compostos)"), getattr(self, "interest_result", None))
            add_section(tr("App", "Anuidades"), getattr(self, "annuity_result", None))
            add_section(tr("App", "Gradientes"), getattr(self, "grad_result", None))
            add_section(tr("App", "Equivalência de Taxas"), getattr(self, "rate_equiv_result", None))
            add_section(tr("App", "Taxa Real / Aparente"), getattr(self, "rate_real_result", None))
            add_section(tr("App", "Amortização"), getattr(self, "amort_result", None))
            add_section(tr("App", "Análise de Investimentos"), getattr(self, "invest_result", None))
            add_section(tr("App", "Depreciação"), getattr(self, "deprec_result", None))

            html_parts = [
                "<html><head><meta charset='utf-8'></head><body>",
                f"<h1>{escape(tr('App','Todos os Cálculos'))}</h1>",
                ]

            for title, text in sections:
                html_parts.append(f"<h2>{escape(title)}</h2><pre>{escape(text)}</pre>")

            table_html = amort_table_to_html(self)
            if table_html:
                html_parts.append(table_html)

            html_parts.append("</body></html>")
            full_html = "\n".join(html_parts)

            combined = QTextEdit()
            combined.setReadOnly(True)
            combined.setHtml(full_html)
            self.export_to_pdf(combined, "todos_calculos.pdf")

        def export_current():
            idx = self.tabs.currentIndex()
            tab_name = self.tabs.tabText(idx)

            mapping = {
                tr("App", "Juros Simples e Compostos"): (getattr(self, "interest_result", None), "juros.pdf"),
                tr("App", "Anuidades"): (getattr(self, "annuity_result", None), "anuidades.pdf"),
                tr("App", "Gradientes"): (getattr(self, "grad_result", None), "gradiente.pdf"),
                tr("App", "Amortização"): (None, None),
                tr("App", "Análise de Investimentos"): (getattr(self, "invest_result", None), "investimento.pdf"),
                tr("App", "Depreciação"): (getattr(self, "deprec_result", None), "depreciacao.pdf"),
                tr("App", "Conversão de Taxas"): (None, None),
                }

            if tab_name == tr("App", "Amortização"):
                self.export_amortization_pdf("amortizacao.pdf")
                return

            if tab_name == tr("App", "Conversão de Taxas"):
                real_widget = getattr(self, "rate_real_result", None)
                equiv_widget = getattr(self, "rate_equiv_result", None)
                if real_widget and real_widget.toPlainText().strip():
                    self.export_to_pdf(real_widget, "taxa_real_aparente.pdf")
                    return

                if equiv_widget and equiv_widget.toPlainText().strip():
                    self.export_to_pdf(equiv_widget, "equivalencia_taxa.pdf")
                    return

                if equiv_widget:
                    self.export_to_pdf(equiv_widget, "equivalencia_taxa.pdf")
                    return

            widget, name = mapping.get(tab_name, (None, None))
            if widget:
                self.export_to_pdf(widget, name or "export.pdf")
                return

            export_all()

        export_current_action.triggered.connect(export_current)
        export_all_action.triggered.connect(export_all)

        self.setMenuBar(menubar)

    except Exception as e:
        logger.error(f"Erro ao criar menu: {e}", exc_info=True)
        raise
