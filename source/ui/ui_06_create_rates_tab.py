from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSizePolicy, QSplitter
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import Qt, QCoreApplication, QTimer
from .ui_23_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_rates_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Conversão de Taxas"))

        layout.addRow(QLabel(tr("App", "<b>Equivalência de Taxas Efetivas</b>")))
        self.rate_equiv_i = QLineEdit()
        self.rate_equiv_current_n = QLineEdit()
        self.rate_equiv_target_n = QLineEdit()

        self.rate_equiv_i.setValidator(QDoubleValidator())
        self.rate_equiv_current_n.setValidator(QDoubleValidator())
        self.rate_equiv_target_n.setValidator(QDoubleValidator())

        calc_equiv_button = QPushButton(tr("App", "Calcular Taxa Equivalente"))
        calc_equiv_button.clicked.connect(self.calculate_rate_equivalence)

        layout.addRow(tr("App", "Taxa Atual (%):"), self.rate_equiv_i)
        layout.addRow(tr("App", "Período da Taxa Atual (em unidades de tempo):"), self.rate_equiv_current_n)
        layout.addRow(tr("App", "Período da Taxa Desejada (em unidades de tempo):"), self.rate_equiv_target_n)
        layout.addRow(calc_equiv_button)

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
        btn_edit_equiv = QPushButton(tr("App", "Editar Cálculo"))
        btn_delete_equiv = QPushButton(tr("App", "Excluir Seleção"))
        btn_export_equiv = QPushButton(tr("App", "Exportar PDF"))
        bottom_layout.addWidget(btn_edit_equiv)
        bottom_layout.addWidget(btn_delete_equiv)
        bottom_layout.addWidget(btn_export_equiv)
        btn_vlayout.addWidget(bottom_row)

        btn_export_equiv.clicked.connect(lambda: self.export_to_pdf(self.rate_equiv_result, "equivalencia_taxa.pdf"))
        btn_delete_equiv.clicked.connect(lambda: self.rate_equiv_result.delete_selected())
        def toggle_edit_equiv():
            if self.rate_equiv_result.is_editing():
                self.rate_equiv_result.commit_edit()
                btn_edit_equiv.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.rate_equiv_result.edit_selected()
                if ok:
                    btn_edit_equiv.setText(tr("App", "Salvar Edição"))

        btn_edit_equiv.clicked.connect(toggle_edit_equiv)
        layout.addRow(btn_widget)

        # Seção Taxa Real
        rate_real_title = tr("App", "Taxa Real e Aparente (Inflação)")
        layout.addRow(QLabel(f"<b>{rate_real_title}</b>"))
        self.rate_real_calc_type = QComboBox()
        self.rate_real_calc_type.addItems([tr("App", "Calcular Taxa Aparente (i)"), tr("App", "Calcular Taxa Real (r)")])
        self.rate_real_r = QLineEdit()
        self.rate_real_i = QLineEdit()
        self.rate_real_inflation = QLineEdit()

        self.rate_real_r.setValidator(QDoubleValidator())
        self.rate_real_i.setValidator(QDoubleValidator())
        self.rate_real_inflation.setValidator(QDoubleValidator())

        calc_real_button = QPushButton(tr("App", "Calcular"))
        calc_real_button.clicked.connect(self.calculate_real_rate)

        layout.addRow(self.rate_real_calc_type)
        layout.addRow(tr("App", "Taxa Real (r %):"), self.rate_real_r)
        layout.addRow(tr("App", "Taxa Aparente (i %):"), self.rate_real_i)
        layout.addRow(tr("App", "Taxa de Inflação (θ %):"), self.rate_real_inflation)
        layout.addRow(calc_real_button)

        btn_widget_real = QWidget()
        btn_vlayout_real = QVBoxLayout(btn_widget_real)
        btn_vlayout_real.setContentsMargins(0,0,0,0)

        top_row_r = QWidget()
        top_layout_r = QHBoxLayout(top_row_r)
        top_layout_r.setContentsMargins(0,0,0,0)
        btn_clear_inputs_r = QPushButton(tr("App", "Limpar Entrada"))
        btn_clear_output_r = QPushButton(tr("App", "Limpar Saída"))
        btn_clear_all_r = QPushButton(tr("App", "Limpar Tudo"))
        top_layout_r.addWidget(btn_clear_inputs_r)
        top_layout_r.addWidget(btn_clear_output_r)
        top_layout_r.addWidget(btn_clear_all_r)
        btn_vlayout_real.addWidget(top_row_r)

        bottom_row_r = QWidget()
        bottom_layout_r = QHBoxLayout(bottom_row_r)
        bottom_layout_r.setContentsMargins(0,0,0,0)
        btn_edit_real = QPushButton(tr("App", "Editar Cálculo"))
        btn_delete_real = QPushButton(tr("App", "Excluir Seleção"))
        btn_export_real = QPushButton(tr("App", "Exportar PDF"))
        bottom_layout_r.addWidget(btn_edit_real)
        bottom_layout_r.addWidget(btn_delete_real)
        bottom_layout_r.addWidget(btn_export_real)
        btn_vlayout_real.addWidget(bottom_row_r)

        btn_export_real.clicked.connect(lambda: self.export_to_pdf(self.rate_real_result, "taxa_real_aparente.pdf"))
        btn_delete_real.clicked.connect(lambda: self.rate_real_result.delete_selected())
        def toggle_edit_real():
            if self.rate_real_result.is_editing():
                self.rate_real_result.commit_edit()
                btn_edit_real.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.rate_real_result.edit_selected()
                if ok:
                    btn_edit_real.setText(tr("App", "Salvar Edição"))

        btn_edit_real.clicked.connect(toggle_edit_real)

        layout.addRow(btn_widget_real)

        # Controle de disposição
        self.rate_layout_mode = QComboBox()
        self.rate_layout_mode.addItems([
            tr("App", "Empilhadas (acima e abaixo)"),
            tr("App", "Lado a lado")
        ])
        layout.addRow(tr("App", "Disposição da visualização:"), self.rate_layout_mode)

        # Criar containers de resultado com rótulos
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        
        # Container para Equivalência de Taxas
        self.rate_equiv_container = QWidget()
        equiv_layout = QVBoxLayout(self.rate_equiv_container)
        equiv_layout.setContentsMargins(0, 0, 0, 0)
        equiv_layout.setSpacing(2)
        
        self.rate_equiv_label = QLabel(tr("App", "<b>Resultado — Equivalência de Taxas</b>"))
        self.rate_equiv_label.setAlignment(Qt.AlignCenter)
        equiv_layout.addWidget(self.rate_equiv_label)
        
        self.rate_equiv_result = HistoryContainer(self)
        self.rate_equiv_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rate_equiv_result.setFont(fixed_font)
        self.rate_equiv_result.setMinimumSize(0, 0)
        equiv_layout.addWidget(self.rate_equiv_result)

        # Container para Taxa Real/Aparente
        self.rate_real_container = QWidget()
        real_layout = QVBoxLayout(self.rate_real_container)
        real_layout.setContentsMargins(0, 0, 0, 0)
        real_layout.setSpacing(2)
        
        self.rate_real_label = QLabel(tr("App", "<b>Resultado — Taxa Real / Aparente</b>"))
        self.rate_real_label.setAlignment(Qt.AlignCenter)
        real_layout.addWidget(self.rate_real_label)
        
        self.rate_real_result = HistoryContainer(self)
        self.rate_real_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rate_real_result.setFont(fixed_font)
        self.rate_real_result.setMinimumSize(0, 0)
        real_layout.addWidget(self.rate_real_result)

        # Criar splitter para os resultados
        self.rate_splitter = QSplitter(Qt.Vertical, self)
        self.rate_splitter.setChildrenCollapsible(False)
        self.rate_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rate_splitter.addWidget(self.rate_equiv_container)
        self.rate_splitter.addWidget(self.rate_real_container)
        self.rate_splitter.setStretchFactor(0, 1)
        self.rate_splitter.setStretchFactor(1, 1)

        # Funções de limpeza
        def clear_inputs():
            self.rate_equiv_i.clear()
            self.rate_equiv_current_n.clear()
            self.rate_equiv_target_n.clear()
            self.rate_real_calc_type.setCurrentIndex(0)
            self.rate_real_r.clear()
            self.rate_real_i.clear()
            self.rate_real_inflation.clear()

        def clear_output():
            self.rate_equiv_result.clear()
            self.rate_real_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        btn_clear_inputs_r.clicked.connect(clear_inputs)
        btn_clear_output_r.clicked.connect(clear_output)
        btn_clear_all_r.clicked.connect(clear_all)

        # Função para alternar orientação
        def set_rate_orientation(index: int):
            orientation = Qt.Vertical if index == 0 else Qt.Horizontal
            self.rate_splitter.setOrientation(orientation)

            def adjust_sizes():
                total_size = self.rate_splitter.size()
                if orientation == Qt.Horizontal:
                    width = max(total_size.width(), 2)
                    half = width // 2
                    self.rate_splitter.setSizes([half, width - half])
                else:
                    height = max(total_size.height(), 2)
                    half = height // 2
                    self.rate_splitter.setSizes([half, height - half])

            QTimer.singleShot(0, adjust_sizes)

        self.rate_layout_mode.currentIndexChanged.connect(set_rate_orientation)
        set_rate_orientation(self.rate_layout_mode.currentIndex())

        right_layout.addWidget(self.rate_splitter)

    except Exception as e:
        logger.error(f"Erro ao criar aba de conversão de taxas: {e}", exc_info=True)
        raise
