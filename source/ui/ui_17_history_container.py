from PySide6.QtWidgets import (QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QCheckBox, QTextEdit, QSizePolicy)
from PySide6.QtCore import Qt, QCoreApplication, QEvent
from utils.LogManager import LogManager
from utils.FontManager import FontManager

logger = LogManager.get_logger()


class HistoryContainer(QWidget):
    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self._entries = []
            self._editing_index = None
            self._entry_height = None

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
            self._scroll.viewport().installEventFilter(self)

        except Exception as e:
            logger.error(f"Erro ao inicializar HistoryContainer: {e}", exc_info=True)
            raise

    def eventFilter(self, obj, event):
        try:
            if obj is self._scroll.viewport() and event.type() == QEvent.Resize:
                vh = obj.height()
                if vh > 0:
                    self._entry_height = vh
                    self._sync_entry_sizes()

            return super().eventFilter(obj, event)

        except Exception as e:
            logger.error(f"Erro em eventFilter do HistoryContainer: {e}", exc_info=True)
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
            for entry_w, chk, te in self._entries:
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

            logger.info("Tema atualizado para HistoryContainer")

        except Exception as e:
            logger.error(f"Erro ao atualizar tema: {e}", exc_info=True)

    def _sync_entry_sizes(self):
        try:
            if not self._entries or not self._entry_height:
                return

            total_margin = 8
            spacing_per_entry = 2
            h = max(1, self._entry_height - total_margin - spacing_per_entry)
            for entry_w, chk, te in self._entries:
                entry_w.setFixedHeight(h)
                te.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                te.setMinimumHeight(max(1, h - 40))

        except Exception as e:
            logger.error(f"Erro ao sincronizar tamanhos das entradas: {e}", exc_info=True)
            raise

    def _convert_to_html(self, text: str) -> str:
        try:
            from html import escape
            escaped_text = escape(text)
            html_style = FontManager.get_html_style()
            html_content = f"{html_style}<body><pre>{escaped_text}</pre></body>"
            return html_content

        except Exception as e:
            logger.error(f"Erro ao converter para HTML: {e}", exc_info=True)
            return text

    def append(self, text: str):
        try:
            if self._editing_index is not None and 0 <= self._editing_index < len(self._entries):
                _, chk, te = self._entries[self._editing_index]
                te.setPlainText(text)
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
                    background-color: transparent;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
            entry_layout.addWidget(chk, 0, Qt.AlignTop)

            te = QTextEdit(entry_w)
            te.setReadOnly(True)

            html_content = self._convert_to_html(text)
            te.setHtml(html_content)
            
            te.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            entry_layout.setStretch(0, 0)
            entry_layout.setStretch(1, 1)
            entry_layout.addWidget(te, 1)

            entry_w.setLayout(entry_layout)

            self._inner_layout.addWidget(entry_w)
            self._entries.append((entry_w, chk, te))
            if not self._entry_height:
                vh = self._scroll.viewport().height()
                self._entry_height = vh if vh > 0 else 300

            self._sync_entry_sizes()

        except Exception as e:
            logger.error(f"Erro ao adicionar entrada no HistoryContainer: {e}", exc_info=True)
            raise

    def refresh_all_fonts(self):
        try:
            for entry_w, chk, te in self._entries:
                current_text = te.toPlainText()
                if current_text:
                    html_content = self._convert_to_html(current_text)
                    te.setHtml(html_content)

            logger.info("Fontes de todas as entradas atualizadas")

        except Exception as e:
            logger.error(f"Erro ao atualizar fontes: {e}", exc_info=True)

    def clear(self):
        try:
            for widget, _, _ in list(self._entries):
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
            for _, _, te in self._entries:
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
            return [i for i, (_, chk, _) in enumerate(self._entries) if chk.isChecked()]

        except Exception as e:
            logger.error(f"Erro ao obter índices selecionados no HistoryContainer: {e}", exc_info=True)
            raise

    def edit_selected(self):
        try:
            selected = self.get_selected_indices()
            if len(selected) != 1:
                return False

            idx = selected[0]
            _, chk, te = self._entries[idx]
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

            _, chk, te = self._entries[self._editing_index]
            current_text = te.toPlainText()

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
                widget, chk, _ = self._entries[i]
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
