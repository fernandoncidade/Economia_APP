from PySide6.QtWidgets import (QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QCheckBox, QTextEdit, QSizePolicy)
from PySide6.QtCore import Qt


class HistoryContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._entries = []
        self._editing_index = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        main_layout.addWidget(self._scroll)

        self._inner = QWidget()
        self._inner_layout = QVBoxLayout(self._inner)
        self._inner_layout.setAlignment(Qt.AlignTop)
        self._inner.setLayout(self._inner_layout)

        self._scroll.setWidget(self._inner)

    def append(self, text: str):
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
        chk.setToolTip("Marque para editar/excluir esta entrada")
        entry_layout.addWidget(chk, 0, Qt.AlignTop)

        te = QTextEdit(entry_w)
        te.setReadOnly(True)
        te.setPlainText(text)
        te.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        entry_layout.addWidget(te, 1)

        entry_w.setLayout(entry_layout)

        self._inner_layout.addWidget(entry_w)
        self._entries.append((entry_w, chk, te))

    def clear(self):
        for widget, _, _ in list(self._entries):
            self._inner_layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

        self._entries.clear()
        self._editing_index = None

    def toPlainText(self) -> str:
        parts = []
        for _, _, te in self._entries:
            txt = te.toPlainText().strip()
            if txt:
                parts.append(txt)

        return "\n\n".join(parts)

    def setReadOnly(self, value: bool):
        for _, _, te in self._entries:
            te.setReadOnly(value)

    def get_selected_indices(self):
        return [i for i, (_, chk, _) in enumerate(self._entries) if chk.isChecked()]

    def edit_selected(self):
        selected = self.get_selected_indices()
        if len(selected) != 1:
            return False

        idx = selected[0]
        _, chk, te = self._entries[idx]
        self._editing_index = idx
        te.setReadOnly(False)
        te.setFocus()
        return True

    def commit_edit(self):
        if self._editing_index is None:
            return False

        _, chk, te = self._entries[self._editing_index]
        te.setReadOnly(True)
        chk.setChecked(False)
        self._editing_index = None
        return True

    def cancel_edit(self):
        return self.commit_edit()

    def delete_selected(self):
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

        return

    def is_editing(self):
        return self._editing_index is not None
