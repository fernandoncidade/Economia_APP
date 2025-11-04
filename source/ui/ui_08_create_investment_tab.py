from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QSizePolicy, QComboBox, QLabel
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_20_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_investment_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Análise de Investimentos"))

        # ComboBox para selecionar tipo de análise
        self.invest_analysis_type = QComboBox()
        self.invest_analysis_type.addItems([
            tr("App", "VPL e VAUE (Fluxo Uniforme)"),
            tr("App", "VPL Detalhado (Receitas e Custos)"),
            tr("App", "Payback Descontado"),
            tr("App", "Análise de Sensibilidade do VPL")
        ])

        # Campos comuns
        self.invest_initial = QLineEdit()
        self.invest_cashflow = QLineEdit()
        self.invest_n = QLineEdit()
        self.invest_tma = QLineEdit()

        # Campos adicionais para VPL Detalhado e Análise de Sensibilidade
        self.invest_annual_revenue = QLineEdit()
        self.invest_annual_cost = QLineEdit()

        # Campo adicional para Análise de Sensibilidade
        self.invest_sensitivity_variation = QLineEdit()

        self.invest_initial.setValidator(QDoubleValidator())
        self.invest_cashflow.setValidator(QDoubleValidator())
        self.invest_n.setValidator(QDoubleValidator())
        self.invest_tma.setValidator(QDoubleValidator())
        self.invest_annual_revenue.setValidator(QDoubleValidator())
        self.invest_annual_cost.setValidator(QDoubleValidator())
        self.invest_sensitivity_variation.setValidator(QDoubleValidator())

        self.invest_result = HistoryContainer(self)
        self.invest_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.invest_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular"))
        calc_button.clicked.connect(self.calculate_investment)

        # Labels dinâmicos - criar ANTES de adicionar ao layout
        self.label_cashflow = QLabel(tr("App", "Fluxo de Caixa Líquido Periódico (Benefícios - Custos):"))
        self.label_revenue = QLabel(tr("App", "Receita Anual:"))
        self.label_cost = QLabel(tr("App", "Custo/Desembolso Anual:"))
        self.label_sensitivity = QLabel(tr("App", "Variação Percentual na Receita (%):"))

        # Adicionar ao layout
        layout.addRow(tr("App", "Tipo de Análise:"), self.invest_analysis_type)
        layout.addRow(tr("App", "Investimento Inicial:"), self.invest_initial)

        # Adicionar campos com labels que serão alternados
        layout.addRow(self.label_cashflow, self.invest_cashflow)
        layout.addRow(self.label_revenue, self.invest_annual_revenue)
        layout.addRow(self.label_cost, self.invest_annual_cost)
        layout.addRow(self.label_sensitivity, self.invest_sensitivity_variation)

        layout.addRow(tr("App", "Número de Períodos (n):"), self.invest_n)
        layout.addRow(tr("App", "Taxa Mínima de Atratividade (TMA %):"), self.invest_tma)
        layout.addRow(calc_button)

        # Função para alternar visibilidade dos campos
        def toggle_fields():
            analysis_type = self.invest_analysis_type.currentIndex()
            # 0 = VPL/VAUE Uniforme, 1 = VPL Detalhado, 2 = Payback, 3 = Análise Sensibilidade

            if analysis_type == 0:  # VPL/VAUE Uniforme
                self.label_cashflow.setVisible(True)
                self.invest_cashflow.setVisible(True)
                self.label_revenue.setVisible(False)
                self.invest_annual_revenue.setVisible(False)
                self.label_cost.setVisible(False)
                self.invest_annual_cost.setVisible(False)
                self.label_sensitivity.setVisible(False)
                self.invest_sensitivity_variation.setVisible(False)
                calc_button.setText(tr("App", "Calcular VPL e VAUE"))

            elif analysis_type == 1:  # VPL Detalhado
                self.label_cashflow.setVisible(False)
                self.invest_cashflow.setVisible(False)
                self.label_revenue.setVisible(True)
                self.invest_annual_revenue.setVisible(True)
                self.label_cost.setVisible(True)
                self.invest_annual_cost.setVisible(True)
                self.label_sensitivity.setVisible(False)
                self.invest_sensitivity_variation.setVisible(False)
                calc_button.setText(tr("App", "Calcular VPL Detalhado"))

            elif analysis_type == 2:  # Payback Descontado
                self.label_cashflow.setVisible(True)
                self.invest_cashflow.setVisible(True)
                self.label_revenue.setVisible(False)
                self.invest_annual_revenue.setVisible(False)
                self.label_cost.setVisible(False)
                self.invest_annual_cost.setVisible(False)
                self.label_sensitivity.setVisible(False)
                self.invest_sensitivity_variation.setVisible(False)
                calc_button.setText(tr("App", "Calcular Payback Descontado"))

            else:  # Análise de Sensibilidade (index 3)
                self.label_cashflow.setVisible(False)
                self.invest_cashflow.setVisible(False)
                self.label_revenue.setVisible(True)
                self.invest_annual_revenue.setVisible(True)
                self.label_cost.setVisible(True)
                self.invest_annual_cost.setVisible(True)
                self.label_sensitivity.setVisible(True)
                self.invest_sensitivity_variation.setVisible(True)
                calc_button.setText(tr("App", "Calcular Análise de Sensibilidade"))

        self.invest_analysis_type.currentIndexChanged.connect(toggle_fields)
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

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.invest_result, "investimento.pdf"))
        btn_delete.clicked.connect(lambda: self.invest_result.delete_selected())
        
        def toggle_edit_invest():
            if self.invest_result.is_editing():
                self.invest_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.invest_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit_invest)
        layout.addRow(btn_widget)

        def clear_inputs():
            self.invest_initial.clear()
            self.invest_cashflow.clear()
            self.invest_annual_revenue.clear()
            self.invest_annual_cost.clear()
            self.invest_sensitivity_variation.clear()
            self.invest_n.clear()
            self.invest_tma.clear()
            self.invest_analysis_type.setCurrentIndex(0)

        def clear_output():
            self.invest_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        right_layout.addWidget(self.invest_result)

    except Exception as e:
        logger.error(f"Erro ao criar aba de investimento: {e}", exc_info=True)
        raise
