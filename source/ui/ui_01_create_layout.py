from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_layout(self):
    try:
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

    except Exception as e:
        logger.error(f"Erro ao criar layout: {e}", exc_info=True)
        raise
