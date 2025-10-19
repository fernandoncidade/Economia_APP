from PySide6.QtWidgets import QMainWindow, QTabWidget
from language.tr_01_gerenciadorTraducao import GerenciadorTraducao
from PySide6.QtCore import QCoreApplication

# Import das funções de UI (create_*) e helpers — usando os __init__.py de cada pacote
from .ui import (
    create_layout,
    get_float_from_line_edit,
    create_interest_tab,
    create_annuity_tab,
    create_gradient_tab,
    create_rates_tab,
    create_amortization_tab,
    create_investment_tab,
    create_depreciation_tab,
    generate_sac_table,
    generate_price_table,
    generate_sam_table,
    set_amort_table_row,
    get_table_data,
    export_to_pdf,
    export_amortization_pdf,
    create_menu_bar,
)

# Import dos serviços (cálculos) via source/services/__init__.py
from .services import (
    calculate_interest,
    calculate_annuity,
    calculate_gradient,
    calculate_rate_equivalence,
    calculate_real_rate,
    calculate_amortization,
    calculate_investment,
    calculate_depreciation,
)


class FinancialCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tr = lambda s: QCoreApplication.translate("App", s)
        self.setGeometry(100, 100, 900, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.gerenciador = GerenciadorTraducao()

        self.gerenciador.idioma_alterado.connect(self.on_language_changed)
        self.gerenciador.aplicar_traducao()
        self.setWindowTitle(self.tr("Calculadora de Economia de Engenharia - TT007"))
        self.rebuild_ui()

    def on_language_changed(self, codigo_idioma):
        try:
            self.setWindowTitle(self.tr("Calculadora de Economia de Engenharia - TT007"))
            self.rebuild_ui()

        except Exception as e:
            print(f"Erro ao mudar idioma: {e}")

    def rebuild_ui(self):
        # Limpa abas e recria tudo para reaplicar traduções
        self.tabs.clear()

        # Chamadas de criação das abas — essas funções foram importadas acima
        self.create_interest_tab()
        self.create_annuity_tab()
        self.create_gradient_tab()
        self.create_rates_tab()
        self.create_amortization_tab()
        self.create_investment_tab()
        self.create_depreciation_tab()

        # Barra de menus (recria para atualizar textos traduzíveis)
        self.create_menu_bar()

# Vincular as funções importadas como métodos da classe (disponíveis via self)
FinancialCalculatorApp.create_layout = create_layout
FinancialCalculatorApp.get_float_from_line_edit = get_float_from_line_edit

FinancialCalculatorApp.create_interest_tab = create_interest_tab
FinancialCalculatorApp.create_annuity_tab = create_annuity_tab
FinancialCalculatorApp.create_gradient_tab = create_gradient_tab
FinancialCalculatorApp.create_rates_tab = create_rates_tab
FinancialCalculatorApp.create_amortization_tab = create_amortization_tab
FinancialCalculatorApp.create_investment_tab = create_investment_tab
FinancialCalculatorApp.create_depreciation_tab = create_depreciation_tab

# Amortization helpers
FinancialCalculatorApp.generate_sac_table = generate_sac_table
FinancialCalculatorApp.generate_price_table = generate_price_table
FinancialCalculatorApp.generate_sam_table = generate_sam_table
FinancialCalculatorApp.set_amort_table_row = set_amort_table_row
FinancialCalculatorApp.get_table_data = get_table_data

# Services (cálculos)
FinancialCalculatorApp.calculate_interest = calculate_interest
FinancialCalculatorApp.calculate_annuity = calculate_annuity
FinancialCalculatorApp.calculate_gradient = calculate_gradient
FinancialCalculatorApp.calculate_rate_equivalence = calculate_rate_equivalence
FinancialCalculatorApp.calculate_real_rate = calculate_real_rate
FinancialCalculatorApp.calculate_amortization = calculate_amortization
FinancialCalculatorApp.calculate_investment = calculate_investment
FinancialCalculatorApp.calculate_depreciation = calculate_depreciation

# Export PDF helper
FinancialCalculatorApp.export_to_pdf = export_to_pdf
FinancialCalculatorApp.export_amortization_pdf = export_amortization_pdf
# Menu bar
FinancialCalculatorApp.create_menu_bar = create_menu_bar
