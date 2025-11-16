from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, 
                                QSizePolicy, QLabel, QCheckBox)
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_23_history_container import HistoryContainer
from utils.LogManager import LogManager
from utils.TextFormat import to_html_subscripts

logger = LogManager.get_logger()

def create_vpl_tax_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "VPL com Impostos"))

        # Campos de entrada obrigatórios
        self.vpl_tax_investment = QLineEdit()
        self.vpl_tax_annual_profit = QLineEdit()
        self.vpl_tax_useful_life = QLineEdit()
        self.vpl_tax_irpj = QLineEdit()
        self.vpl_tax_csll = QLineEdit()
        self.vpl_tax_tma = QLineEdit()
        
        # Campos opcionais
        self.vpl_tax_residual_value = QLineEdit()
        self.vpl_tax_sale_year = QLineEdit()
        self.vpl_tax_sale_value = QLineEdit()
        
        # Campos de financiamento
        self.vpl_tax_financed = QCheckBox(tr("App", "Investimento Financiado (SAC)"))
        self.vpl_tax_finance_rate = QLineEdit()
        self.vpl_tax_finance_periods = QLineEdit()

        # Validadores
        for field in [self.vpl_tax_investment, self.vpl_tax_annual_profit, 
                      self.vpl_tax_useful_life, self.vpl_tax_irpj, self.vpl_tax_csll,
                      self.vpl_tax_tma, self.vpl_tax_residual_value,
                      self.vpl_tax_sale_year, self.vpl_tax_sale_value,
                      self.vpl_tax_finance_rate, self.vpl_tax_finance_periods]:
            field.setValidator(QDoubleValidator())

        # Placeholders
        self.vpl_tax_residual_value.setPlaceholderText(tr("App", "Padrão: 0"))
        self.vpl_tax_sale_year.setPlaceholderText(tr("App", "Padrão: último ano"))
        self.vpl_tax_sale_value.setPlaceholderText(tr("App", "Padrão: 0"))
        self.vpl_tax_finance_rate.setPlaceholderText(tr("App", "Taxa de juros (%)"))
        self.vpl_tax_finance_periods.setPlaceholderText(tr("App", "Número de parcelas"))

        # Valores padrão
        self.vpl_tax_irpj.setText("25")
        self.vpl_tax_csll.setText("9")
        
        # Habilitar/desabilitar campos de financiamento
        def toggle_finance_fields():
            enabled = self.vpl_tax_financed.isChecked()
            self.vpl_tax_finance_rate.setEnabled(enabled)
            self.vpl_tax_finance_periods.setEnabled(enabled)
        
        self.vpl_tax_financed.toggled.connect(toggle_finance_fields)
        self.vpl_tax_finance_rate.setEnabled(False)
        self.vpl_tax_finance_periods.setEnabled(False)

        # Área de resultado
        self.vpl_tax_result = HistoryContainer(self)
        self.vpl_tax_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.vpl_tax_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular VPL"))
        calc_button.clicked.connect(self.calculate_vpl_with_taxes)

        # Layout
        layout.addRow(QLabel(to_html_subscripts(tr("App", "<b>Dados Obrigatórios</b>"))))
        layout.addRow(tr("App", "Investimento Inicial (R$):"), self.vpl_tax_investment)
        layout.addRow(tr("App", "Lucro Antes dos Impostos (R$/ano):"), self.vpl_tax_annual_profit)
        layout.addRow(tr("App", "Vida Útil (anos):"), self.vpl_tax_useful_life)
        layout.addRow(tr("App", "IRPJ (%):"), self.vpl_tax_irpj)
        layout.addRow(tr("App", "CSLL (%):"), self.vpl_tax_csll)
        layout.addRow(tr("App", "TMA (% ao ano):"), self.vpl_tax_tma)
        
        layout.addRow(QLabel(to_html_subscripts(tr("App", "<b>Financiamento (Opcional)</b>"))))
        layout.addRow(self.vpl_tax_financed)
        layout.addRow(tr("App", "Taxa de Juros (%):"), self.vpl_tax_finance_rate)
        layout.addRow(tr("App", "Número de Parcelas:"), self.vpl_tax_finance_periods)
        
        layout.addRow(QLabel(to_html_subscripts(tr("App", "<b>Venda Antecipada (Opcional)</b>"))))
        layout.addRow(tr("App", "Valor Residual (R$):"), self.vpl_tax_residual_value)
        layout.addRow(tr("App", "Ano de Venda:"), self.vpl_tax_sale_year)
        layout.addRow(tr("App", "Valor de Venda (R$):"), self.vpl_tax_sale_value)
        
        layout.addRow(calc_button)

        # Botões de controle
        btn_widget = QWidget()
        btn_vlayout = QVBoxLayout(btn_widget)
        btn_vlayout.setContentsMargins(0, 0, 0, 0)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        btn_clear_inputs = QPushButton(tr("App", "Limpar Entrada"))
        btn_clear_output = QPushButton(tr("App", "Limpar Saída"))
        btn_clear_all = QPushButton(tr("App", "Limpar Tudo"))
        top_layout.addWidget(btn_clear_inputs)
        top_layout.addWidget(btn_clear_output)
        top_layout.addWidget(btn_clear_all)
        btn_vlayout.addWidget(top_row)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        btn_edit = QPushButton(tr("App", "Editar Cálculo"))
        btn_delete = QPushButton(tr("App", "Excluir Seleção"))
        btn_export = QPushButton(tr("App", "Exportar PDF"))
        bottom_layout.addWidget(btn_edit)
        bottom_layout.addWidget(btn_delete)
        bottom_layout.addWidget(btn_export)
        btn_vlayout.addWidget(bottom_row)

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.vpl_tax_result, "vpl_impostos.pdf"))
        btn_delete.clicked.connect(lambda: self.vpl_tax_result.delete_selected())

        def toggle_edit():
            if self.vpl_tax_result.is_editing():
                self.vpl_tax_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.vpl_tax_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit)

        def clear_inputs():
            self.vpl_tax_investment.clear()
            self.vpl_tax_annual_profit.clear()
            self.vpl_tax_useful_life.clear()
            self.vpl_tax_tma.clear()
            self.vpl_tax_residual_value.clear()
            self.vpl_tax_sale_year.clear()
            self.vpl_tax_sale_value.clear()
            self.vpl_tax_finance_rate.clear()
            self.vpl_tax_finance_periods.clear()
            self.vpl_tax_financed.setChecked(False)
            self.vpl_tax_irpj.setText("25")
            self.vpl_tax_csll.setText("9")

        def clear_output():
            self.vpl_tax_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        layout.addRow(btn_widget)
        right_layout.addWidget(self.vpl_tax_result)

    except Exception as e:
        logger.error(f"Erro ao criar aba VPL com impostos: {e}", exc_info=True)
        raise