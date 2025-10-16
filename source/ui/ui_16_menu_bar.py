from PySide6.QtWidgets import QMenuBar, QTextEdit
from PySide6.QtGui import QAction
from html import escape
from .ui_15_export_pdf import amort_table_to_html

def create_menu_bar(self):
    menubar = QMenuBar(self)
    file_menu = menubar.addMenu("Arquivos")

    export_current_action = QAction("Exportar Atual", self)
    export_all_action = QAction("Exportar Todos", self)

    file_menu.addAction(export_current_action)
    file_menu.addAction(export_all_action)

    def export_all():
        sections = []

        def add_section(title, widget):
            if not widget:
                return

            text = widget.toPlainText().strip()
            if text:
                sections.append((title, text))

        add_section("Juros (Simples/Compostos)", getattr(self, "interest_result", None))
        add_section("Anuidades", getattr(self, "annuity_result", None))
        add_section("Gradientes", getattr(self, "grad_result", None))
        add_section("Equivalência de Taxas", getattr(self, "rate_equiv_result", None))
        add_section("Taxa Real / Aparente", getattr(self, "rate_real_result", None))
        add_section("Amortização", getattr(self, "amort_result", None))
        add_section("Análise de Investimentos", getattr(self, "invest_result", None))
        add_section("Depreciação", getattr(self, "deprec_result", None))

        html_parts = [
            "<html><head><meta charset='utf-8'></head><body>",
            "<h1>Todos os Cálculos</h1>",
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
            "Juros Simples e Compostos": (getattr(self, "interest_result", None), "juros.pdf"),
            "Anuidades": (getattr(self, "annuity_result", None), "anuidades.pdf"),
            "Gradientes": (getattr(self, "grad_result", None), "gradiente.pdf"),
            "Amortização": (None, None),
            "Análise de Investimentos": (getattr(self, "invest_result", None), "investimento.pdf"),
            "Depreciação": (getattr(self, "deprec_result", None), "depreciacao.pdf"),
            "Conversão de Taxas": (None, None),
        }

        if tab_name == "Amortização":
            self.export_amortization_pdf("amortizacao.pdf")
            return

        if tab_name == "Conversão de Taxas":
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
