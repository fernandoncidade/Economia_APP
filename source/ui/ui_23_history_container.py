from PySide6.QtWidgets import (QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QCheckBox, QTextEdit, QSizePolicy, QWidgetItem)
from PySide6.QtCore import Qt, QCoreApplication, QTimer
from source.utils.LogManager import LogManager
from source.utils.FontManager import FontManager
from source.utils.TextFormat import to_html_subscripts

logger = LogManager.get_logger()


class HistoryContainer(QWidget):
    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self._entries = []
            self._editing_index = None
            self._entry_height = None
            self._syncing = False
            self._sync_timer = QTimer(self)
            self._sync_timer.setSingleShot(True)
            self._sync_timer.setInterval(50)
            self._sync_timer.timeout.connect(self._sync_entry_sizes)

            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)

            self._scroll = QScrollArea(self)
            self._scroll.setWidgetResizable(True)
            main_layout.addWidget(self._scroll)

            self._inner = QWidget()
            self._inner_layout = QVBoxLayout(self._inner)
            self._inner_layout.setAlignment(Qt.AlignTop)
            self._inner_layout.setSpacing(2)
            self._inner_layout.setContentsMargins(4, 4, 4, 4)
            self._inner.setLayout(self._inner_layout)

            self._scroll.setWidget(self._inner)
            self._setup_resize_handler()

        except Exception as e:
            logger.error(f"Erro ao inicializar HistoryContainer: {e}", exc_info=True)
            raise

    def _setup_resize_handler(self):
        try:
            def custom_resize(event):
                QScrollArea.resizeEvent(self._scroll, event)
                if not self._syncing and not self._sync_timer.isActive():
                    self._sync_timer.start()

            self._scroll.resizeEvent = custom_resize

        except Exception as e:
            logger.error(f"Erro ao configurar resize handler: {e}", exc_info=True)
            raise

    def changeEvent(self, event):
        try:
            from PySide6.QtCore import QEvent
            if event.type() == QEvent.PaletteChange:
                self._update_theme()

            super().changeEvent(event)

        except Exception as e:
            logger.error(f"Erro em changeEvent do HistoryContainer: {e}", exc_info=True)
            super().changeEvent(event)

    def _update_theme(self):
        try:
            for entry_w, chk, te, ev in self._entries:
                chk.setStyleSheet("""
                    QCheckBox {
                        spacing: 0px;
                        padding: 0px;
                        margin: 0px;
                    }
                    QCheckBox::indicator {
                        width: 18px;
                        height: 18px;
                    }
                """)
                chk.style().polish(chk)
                te.style().polish(te)
                if ev is not None:
                    ev.style().polish(ev)

            logger.info("Tema atualizado para HistoryContainer")

        except Exception as e:
            logger.error(f"Erro ao atualizar tema: {e}", exc_info=True)

    def _sync_entry_sizes(self):
        try:
            if self._syncing:
                return

            self._syncing = True

            if not self._entries:
                return

            vh = self._scroll.viewport().height()
            if not vh:
                return

            total_margin = 8
            spacing_per_entry = 2
            h = max(1, vh - total_margin - spacing_per_entry)

            self._scroll.setUpdatesEnabled(False)

            for entry_w, chk, te, ev in self._entries:
                entry_w.setFixedHeight(h)
                te.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                if ev is not None:
                    ev.setFixedHeight(max(80, int(h * 0.28)))
                    te.setMinimumHeight(max(40, h - ev.height() - 16))

                else:
                    te.setMinimumHeight(max(1, h - 16))

            self._scroll.setUpdatesEnabled(True)

        except Exception as e:
            logger.error(f"Erro ao sincronizar tamanhos das entradas: {e}", exc_info=True)
            self._scroll.setUpdatesEnabled(True)
            raise

        finally:
            self._syncing = False

    def _convert_to_html(self, text: str) -> str:
        try:
            from html import escape

            text_with_subs = to_html_subscripts(text)

            PLACEHOLDER_OPEN = "___SUBSOPEN___"
            PLACEHOLDER_CLOSE = "___SUBSCLOSE___"

            text_protected = text_with_subs.replace("<sub>", PLACEHOLDER_OPEN)
            text_protected = text_protected.replace("</sub>", PLACEHOLDER_CLOSE)

            escaped_text = escape(text_protected)
            escaped_text = escaped_text.replace(PLACEHOLDER_OPEN, "<sub>")
            escaped_text = escaped_text.replace(PLACEHOLDER_CLOSE, "</sub>")

            html_style = FontManager.get_html_style()
            html_content = f"{html_style}<body><pre>{escaped_text}</pre></body>"
            return html_content

        except Exception as e:
            logger.error(f"Erro ao converter para HTML: {e}", exc_info=True)
            return text

    def append(self, text: str, extra_widget=None):
        try:
            if self._editing_index is not None and 0 <= self._editing_index < len(self._entries):
                _, chk, te, ev = self._entries[self._editing_index]
                te.setPlainText(text)
                te.setProperty("raw_text", text)
                te.setReadOnly(False)
                te.setFocus()
                return

            entry_w = QWidget()
            entry_layout = QHBoxLayout(entry_w)
            entry_layout.setContentsMargins(4, 4, 4, 4)
            entry_layout.setSpacing(6)

            chk = QCheckBox(entry_w)
            chk.setToolTip(QCoreApplication.translate("App", "Marque para editar/excluir esta entrada"))
            chk.setFixedSize(20, 20)
            chk.setStyleSheet("""
                QCheckBox {
                    spacing: 0px;
                    padding: 0px;
                    margin: 0px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
            entry_layout.addWidget(chk, 0, Qt.AlignTop)

            # Criar um container vertical para o texto e o widget extra (se houver)
            right_container = QWidget(entry_w)
            right_vlayout = QVBoxLayout(right_container)
            right_vlayout.setContentsMargins(0, 0, 0, 0)
            right_vlayout.setSpacing(6)

            te = QTextEdit(right_container)
            te.setReadOnly(True)

            html_content = self._convert_to_html(text)
            te.setHtml(html_content)
            te.setProperty("raw_text", text)

            # Ajuste: não deixar o QTextEdit crescer indefinidamente (preferência)
            te.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            te.setMinimumHeight(120)
            te.setAcceptRichText(True)
            right_vlayout.addWidget(te)

            # Se houver um widget extra (ex: tabela), adiciona abaixo do texto
            ev = None
            if extra_widget is not None:
                ev = extra_widget
                ev.setParent(right_container)
                # Ajuste: tabela com tamanho fixo para evitar sobrepor o QTextEdit
                ev.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                try:
                    # preferir altura fixa se disponível
                    ev.setFixedHeight(140)

                except Exception:
                    pass

                right_vlayout.addWidget(ev)

            # garantir proporção: te expande; tabela fica em tamanho fixo
            right_vlayout.setStretch(0, 1)
            if ev is not None:
                right_vlayout.setStretch(1, 0)

            entry_layout.setStretch(0, 0)
            entry_layout.setStretch(1, 1)
            entry_layout.addWidget(right_container, 1)

            entry_w.setLayout(entry_layout)

            self._inner_layout.addWidget(entry_w)

            # Armazenar sempre 4 elementos (compatível com demais métodos)
            self._entries.append((entry_w, chk, te, ev))

            if not self._entry_height:
                vh = self._scroll.viewport().height()
                self._entry_height = vh if vh > 0 else 300

            if not self._sync_timer.isActive():
                self._sync_timer.start()

        except Exception as e:
            logger.error(f"Erro ao adicionar entrada no HistoryContainer: {e}", exc_info=True)
            raise

    def refresh_all_fonts(self):
        try:
            for entry_w, chk, te, ev in self._entries:
                raw_text = te.property("raw_text")
                if not raw_text:
                    raw_text = te.toPlainText()

                if raw_text:
                    html_content = self._convert_to_html(raw_text)
                    te.setHtml(html_content)

            logger.info("Fontes de todas as entradas atualizadas")

        except Exception as e:
            logger.error(f"Erro ao atualizar fontes: {e}", exc_info=True)

    def clear(self):
        try:
            for widget, _, _, _ in list(self._entries):
                self._inner_layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()

            self._entries.clear()
            self._editing_index = None

        except Exception as e:
            logger.error(f"Erro ao limpar HistoryContainer: {e}", exc_info=True)
            raise

    def toPlainText(self) -> str:
        try:
            parts = []
            for _, _, te, _ in self._entries:
                txt = te.toPlainText().strip()
                if txt:
                    parts.append(txt)

            return "\n\n".join(parts)

        except Exception as e:
            logger.error(f"Erro ao obter texto do HistoryContainer: {e}", exc_info=True)
            raise

    def setReadOnly(self, value: bool):
        try:
            for _, _, te in self._entries:
                te.setReadOnly(value)

        except Exception as e:
            logger.error(f"Erro ao definir ReadOnly no HistoryContainer: {e}", exc_info=True)
            raise

    def get_selected_indices(self):
        try:
            return [i for i, (_, chk, _, _) in enumerate(self._entries) if chk.isChecked()]

        except Exception as e:
            logger.error(f"Erro ao obter índices selecionados no HistoryContainer: {e}", exc_info=True)
            raise

    def edit_selected(self):
        try:
            selected = self.get_selected_indices()
            if len(selected) != 1:
                return False

            idx = selected[0]
            _, chk, te, _ = self._entries[idx]
            raw_text = te.property("raw_text") or te.toPlainText()
            te.setPlainText(raw_text)
            self._editing_index = idx
            te.setReadOnly(False)
            te.setFocus()
            return True

        except Exception as e:
            logger.error(f"Erro ao iniciar edição no HistoryContainer: {e}", exc_info=True)
            raise

    def commit_edit(self):
        try:
            if self._editing_index is None:
                return False

            _, chk, te, _ = self._entries[self._editing_index]
            current_text = te.toPlainText()
            te.setProperty("raw_text", current_text)

            html_content = self._convert_to_html(current_text)
            te.setHtml(html_content)

            te.setReadOnly(True)
            chk.setChecked(False)
            self._editing_index = None
            return True

        except Exception as e:
            logger.error(f"Erro ao confirmar edição no HistoryContainer: {e}", exc_info=True)
            raise

    def cancel_edit(self):
        try:
            return self.commit_edit()

        except Exception as e:
            logger.error(f"Erro ao cancelar edição no HistoryContainer: {e}", exc_info=True)
            raise

    def delete_selected(self):
        try:
            for i in reversed(range(len(self._entries))):
                widget, chk, _, ev = self._entries[i]
                if chk.isChecked():
                    self._inner_layout.removeWidget(widget)
                    widget.setParent(None)
                    widget.deleteLater()
                    self._entries.pop(i)
                    if self._editing_index is not None:
                        if i < self._editing_index:
                            self._editing_index -= 1

                        elif i == self._editing_index:
                            self._editing_index = None

            self._sync_entry_sizes()
            return

        except Exception as e:
            logger.error(f"Erro ao deletar entradas no HistoryContainer: {e}", exc_info=True)
            raise

    def is_editing(self):
        try:
            return self._editing_index is not None

        except Exception as e:
            logger.error(f"Erro ao verificar estado de edição no HistoryContainer: {e}", exc_info=True)
            raise
