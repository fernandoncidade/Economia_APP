from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QSizePolicy, QComboBox, QLabel
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_20_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_fisher_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "TMA Real e Nominal"))

        # ComboBox para selecionar tipo de cálculo
        self.fisher_calc_type = QComboBox()
        self.fisher_calc_type.addItems([
            tr("App", "Calcular TMA Nominal (a partir da Real)"),
            tr("App", "Calcular TMA Real (a partir da Nominal)")
        ])

        # Campos de entrada
        self.fisher_tma_real = QLineEdit()
        self.fisher_tma_nominal = QLineEdit()
        self.fisher_inflation = QLineEdit()

        self.fisher_tma_real.setValidator(QDoubleValidator())
        self.fisher_tma_nominal.setValidator(QDoubleValidator())
        self.fisher_inflation.setValidator(QDoubleValidator())

        self.fisher_result = HistoryContainer(self)
        self.fisher_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.fisher_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular"))
        calc_button.clicked.connect(self.calculate_fisher)

        # Labels dinâmicos
        self.label_tma_real = QLabel(tr("App", "TMA Real (% ao ano):"))
        self.label_tma_nominal = QLabel(tr("App", "TMA Nominal (% ao ano):"))

        # Adicionar ao layout
        layout.addRow(tr("App", "Tipo de Cálculo:"), self.fisher_calc_type)
        layout.addRow(self.label_tma_real, self.fisher_tma_real)
        layout.addRow(self.label_tma_nominal, self.fisher_tma_nominal)
        layout.addRow(tr("App", "Taxa de Inflação (% ao ano):"), self.fisher_inflation)
        layout.addRow(calc_button)

        # Função para alternar visibilidade dos campos
        def toggle_fields():
            calc_type = self.fisher_calc_type.currentIndex()
            # 0 = Calcular Nominal, 1 = Calcular Real

            if calc_type == 0:  # Calcular Nominal
                self.label_tma_real.setVisible(True)
                self.fisher_tma_real.setVisible(True)
                self.label_tma_nominal.setVisible(False)
                self.fisher_tma_nominal.setVisible(False)
                calc_button.setText(tr("App", "Calcular TMA Nominal"))

            else:  # Calcular Real
                self.label_tma_real.setVisible(False)
                self.fisher_tma_real.setVisible(False)
                self.label_tma_nominal.setVisible(True)
                self.fisher_tma_nominal.setVisible(True)
                calc_button.setText(tr("App", "Calcular TMA Real"))

        self.fisher_calc_type.currentIndexChanged.connect(toggle_fields)
        toggle_fields()  # Inicializar visibilidade

        btn_widget = QWidget()
        btn_vlayout = QVBoxLayout(btn_widget)
        btn_vlayout.setContentsMargins(0,0,0,0)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0,0,0,0)
        btn_clear_inputs = QPushButton(tr("App", "Limpar Entrada"))
        btn_clear_output = QPushButton(tr("App", "Limpar Saída"))
        btn_clear_all = QPushButton(tr("App", "Limpar Tudo"))
        top_layout.addWidget(btn_clear_inputs)
        top_layout.addWidget(btn_clear_output)
        top_layout.addWidget(btn_clear_all)
        btn_vlayout.addWidget(top_row)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0,0,0,0)
        btn_edit = QPushButton(tr("App", "Editar Cálculo"))
        btn_delete = QPushButton(tr("App", "Excluir Seleção"))
        btn_export = QPushButton(tr("App", "Exportar PDF"))
        bottom_layout.addWidget(btn_edit)
        bottom_layout.addWidget(btn_delete)
        bottom_layout.addWidget(btn_export)
        btn_vlayout.addWidget(bottom_row)

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.fisher_result, "fisher.pdf"))
        btn_delete.clicked.connect(lambda: self.fisher_result.delete_selected())

        def toggle_edit_fisher():
            if self.fisher_result.is_editing():
                self.fisher_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.fisher_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit_fisher)
        layout.addRow(btn_widget)

        def clear_inputs():
            self.fisher_tma_real.clear()
            self.fisher_tma_nominal.clear()
            self.fisher_inflation.clear()
            self.fisher_calc_type.setCurrentIndex(0)

        def clear_output():
            self.fisher_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        right_layout.addWidget(self.fisher_result)

    except Exception as e:
        logger.error(f"Erro ao criar aba Fisher: {e}", exc_info=True)
        raise
