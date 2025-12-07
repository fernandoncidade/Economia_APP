from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QCheckBox, QSplitter
from PySide6.QtGui import QDoubleValidator, QFontDatabase, QIntValidator
from PySide6.QtCore import QCoreApplication, Qt, QTimer
from .ui_23_history_container import HistoryContainer
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_amortization_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Amortização"))

        self.amort_system = QComboBox()
        self.amort_system.addItems([
            tr("App", "Sistema Francês (Price)"), 
            tr("App", "Sistema de Amortização Constante (SAC)"), 
            tr("App", "Sistema de Amortização Misto (SAM)"),
            tr("App", "Sistema Americano"),
            tr("App", "Sistema Hamburguês (SAC com Carência)")
        ])

        self.amort_p = QLineEdit()
        self.amort_i = QLineEdit()
        self.amort_n = QLineEdit()

        self.amort_e = QLineEdit()
        self.amort_e.setPlaceholderText(tr("App", "Entrada (E)"))
        self.amort_k = QLineEdit()
        self.amort_k.setPlaceholderText(tr("App", "Período desejado (k)"))

        self.amort_carencia = QLineEdit()
        self.amort_carencia.setPlaceholderText(tr("App", "Períodos de carência"))

        self.amort_juros_capitalizados = QCheckBox(tr("App", "Capitalizar juros durante carência"))
        self.amort_juros_capitalizados.setChecked(False)

        self.amort_p.setValidator(QDoubleValidator())
        self.amort_i.setValidator(QDoubleValidator())
        self.amort_n.setValidator(QDoubleValidator())
        self.amort_carencia.setValidator(QDoubleValidator())
        self.amort_e.setValidator(QDoubleValidator())
        self.amort_k.setValidator(QIntValidator(1, 10**9))

        calc_button = QPushButton(tr("App", "Gerar Tabela de Amortização"))
        calc_button.clicked.connect(self.calculate_amortization)

        calc_k_button = QPushButton(tr("App", "Calcular valor no período k"))
        calc_k_button.clicked.connect(self.calculate_value_at_k)

        self.amort_layout_mode = QComboBox()
        self.amort_layout_mode.addItems([
            tr("App", "Empilhadas (acima e abaixo)"),
            tr("App", "Lado a lado")
        ])

        self.amort_table = QTableWidget()
        self.amort_table.setColumnCount(5)
        headers = [tr("App", "Período (k)"), tr("App", "Prestação"), tr("App", "Juros"), tr("App", "Amortização"), tr("App", "Saldo Devedor")]
        self.amort_table.setHorizontalHeaderLabels(headers)
        self.amort_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.amort_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.amort_table.setMinimumSize(0, 0)

        self.amort_result = HistoryContainer(self)
        self.amort_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.amort_result.setFont(fixed_font)
        self.amort_result.setMinimumSize(0, 0)

        self.amort_splitter = QSplitter(Qt.Vertical, self)
        self.amort_splitter.setChildrenCollapsible(False)
        self.amort_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.amort_splitter.addWidget(self.amort_result)
        self.amort_splitter.addWidget(self.amort_table)
        self.amort_splitter.setStretchFactor(0, 1)
        self.amort_splitter.setStretchFactor(1, 1)

        layout.addRow(tr("App", "Sistema de Amortização:"), self.amort_system)
        layout.addRow(tr("App", "Valor do Financiamento (P):"), self.amort_p)
        layout.addRow(tr("App", "Entrada (E):"), self.amort_e)
        layout.addRow(tr("App", "Taxa de Juros (i % ao período):"), self.amort_i)
        layout.addRow(tr("App", "Prazo (n períodos):"), self.amort_n)
        layout.addRow(tr("App", "Carência (períodos):"), self.amort_carencia)
        layout.addRow(self.amort_juros_capitalizados)
        layout.addRow(tr("App", "Período desejado (k):"), self.amort_k)
        layout.addRow(calc_button)
        layout.addRow(calc_k_button)
        layout.addRow(tr("App", "Disposição da visualização:"), self.amort_layout_mode)

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

        btn_export.clicked.connect(lambda: self.export_amortization_pdf("amortizacao.pdf"))
        btn_delete.clicked.connect(lambda: self.amort_result.delete_selected())
        def toggle_edit_amort():
            if self.amort_result.is_editing():
                self.amort_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.amort_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit_amort)

        layout.addRow(btn_widget)

        def clear_inputs():
            self.amort_p.clear()
            self.amort_i.clear()
            self.amort_n.clear()
            self.amort_carencia.clear()
            self.amort_e.clear()
            self.amort_k.clear()
            self.amort_system.setCurrentIndex(0)
            self.amort_juros_capitalizados.setChecked(False)

        def clear_output():
            self.amort_table.clearContents()
            self.amort_table.setRowCount(1)
            for c in range(self.amort_table.columnCount()):
                self.amort_table.setItem(0, c, QTableWidgetItem(""))

            self.amort_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        def toggle_carencia_fields():
            system_index = self.amort_system.currentIndex()
            is_price_or_sac_or_hamb = system_index in (0, 1, 4)
            self.amort_carencia.setVisible(is_price_or_sac_or_hamb)
            self.amort_juros_capitalizados.setVisible(is_price_or_sac_or_hamb)

        self.amort_system.currentIndexChanged.connect(toggle_carencia_fields)
        toggle_carencia_fields()

        def set_amort_orientation(index: int):
            orientation = Qt.Vertical if index == 0 else Qt.Horizontal
            self.amort_splitter.setOrientation(orientation)

            def adjust_sizes():
                total_size = self.amort_splitter.size()
                if orientation == Qt.Horizontal:
                    width = max(total_size.width(), 2)
                    half = width // 2
                    self.amort_splitter.setSizes([half, width - half])
                else:
                    height = max(total_size.height(), 2)
                    half = height // 2
                    self.amort_splitter.setSizes([half, height - half])

            QTimer.singleShot(0, adjust_sizes)

        self.amort_layout_mode.currentIndexChanged.connect(set_amort_orientation)
        set_amort_orientation(self.amort_layout_mode.currentIndex())

        right_layout.addWidget(self.amort_splitter)

    except Exception as e:
        logger.error(f"Erro ao criar aba de amortização: {e}", exc_info=True)
        raise
