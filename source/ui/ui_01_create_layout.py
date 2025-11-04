from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

def create_layout(self):
    widget = QWidget()
    main_h = QHBoxLayout(widget)
    form_widget = QWidget()
    form_layout = QFormLayout(form_widget)
    form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
    form_widget.setMinimumWidth(320)
    main_h.addWidget(form_widget, 0)

    right_widget = QWidget()
    right_layout = QVBoxLayout(right_widget)
    right_layout.setAlignment(Qt.AlignTop)
    right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    main_h.addWidget(right_widget, 1)

    return widget, form_layout, right_layout
