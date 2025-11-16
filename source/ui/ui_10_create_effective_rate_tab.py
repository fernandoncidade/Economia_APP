from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QSizePolicy, QLabel
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_23_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_effective_rate_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Taxa Efetiva / TIR / Taxa Global"))

        # Modo de cálculo
        self.eff_rate_calc_mode = QComboBox()
        self.eff_rate_calc_mode.addItems([
            tr("App", "Taxa Efetiva Anual"),
            tr("App", "Taxa Interna de Retorno (TIR)"),
            tr("App", "Taxa Global de Juros"),
            tr("App", "Taxa Efetiva em Cobrança Antecipada"),
            tr("App", "TIR Modificada (TIRm)"),
            tr("App", "TMA vs Rentabilidade"),
            tr("App", "Juros Reais")
        ])

        # Campos para Taxa Efetiva
        self.eff_rate_nominal = QLineEdit()
        self.eff_rate_period_nominal = QLineEdit()
        self.eff_rate_period_cap = QLineEdit()
        self.eff_rate_period_target = QLineEdit()

        # Campos para TIR
        self.tir_initial = QLineEdit()
        self.tir_periods = QLineEdit()
        self.tir_return = QLineEdit()

        # Campos para Taxa Global
        self.tax_global_real = QLineEdit()
        self.tax_global_inf_m1 = QLineEdit()
        self.tax_global_inf_m2 = QLineEdit()
        self.tax_global_inf_m3 = QLineEdit()

        # Campos para Cobrança Antecipada
        self.adv_int_nominal = QLineEdit()
        self.adv_int_rate = QLineEdit()

        # Campos para TIR Modificada
        self.tirm_initial = QLineEdit()
        self.tirm_periods = QLineEdit()
        self.tirm_return = QLineEdit()
        self.tirm_cap_rate = QLineEdit()

        # Campos para TMA vs Rentabilidade
        self.tma_capital = QLineEdit()
        self.tma_monthly_rate = QLineEdit()
        self.tma_rate = QLineEdit()
        self.tma_periods = QLineEdit()

        # Campos para Juros Reais
        self.real_int_capital = QLineEdit()
        self.real_int_global_rate = QLineEdit()
        self.real_int_inflation = QLineEdit()

        # Validadores
        all_fields = [
            self.eff_rate_nominal, self.eff_rate_period_nominal, self.eff_rate_period_cap,
            self.eff_rate_period_target, self.tir_initial, self.tir_periods, self.tir_return,
            self.tax_global_real, self.tax_global_inf_m1, self.tax_global_inf_m2, self.tax_global_inf_m3,
            self.adv_int_nominal, self.adv_int_rate,
            self.tirm_initial, self.tirm_periods, self.tirm_return, self.tirm_cap_rate,
            self.tma_capital, self.tma_monthly_rate, self.tma_rate, self.tma_periods,
            self.real_int_capital, self.real_int_global_rate, self.real_int_inflation
        ]
        for field in all_fields:
            field.setValidator(QDoubleValidator())

        self.eff_rate_result = HistoryContainer(self)
        self.eff_rate_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.eff_rate_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular"))
        calc_button.clicked.connect(self.calculate_effective_rate)

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

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.eff_rate_result, "taxa_efetiva_tir.pdf"))
        btn_delete.clicked.connect(lambda: self.eff_rate_result.delete_selected())

        def toggle_edit():
            if self.eff_rate_result.is_editing():
                self.eff_rate_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.eff_rate_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit)

        layout.addRow(tr("App", "Modo de Cálculo:"), self.eff_rate_calc_mode)

        # Dicionário para armazenar labels e campos por modo
        self.eff_rate_fields = {}

        # Campos para Taxa Efetiva (mode 0)
        self.eff_rate_fields[0] = []
        lbl = QLabel(tr("App", "Taxa Nominal (%):"))
        layout.addRow(lbl, self.eff_rate_nominal)
        self.eff_rate_fields[0].append((lbl, self.eff_rate_nominal))

        lbl = QLabel(tr("App", "Período da Taxa Nominal:"))
        layout.addRow(lbl, self.eff_rate_period_nominal)
        self.eff_rate_fields[0].append((lbl, self.eff_rate_period_nominal))

        lbl = QLabel(tr("App", "Período de Capitalização:"))
        layout.addRow(lbl, self.eff_rate_period_cap)
        self.eff_rate_fields[0].append((lbl, self.eff_rate_period_cap))

        lbl = QLabel(tr("App", "Período Desejado:"))
        layout.addRow(lbl, self.eff_rate_period_target)
        self.eff_rate_fields[0].append((lbl, self.eff_rate_period_target))

        # Campos para TIR (mode 1)
        self.eff_rate_fields[1] = []
        lbl = QLabel(tr("App", "Investimento Inicial (R$):"))
        layout.addRow(lbl, self.tir_initial)
        self.eff_rate_fields[1].append((lbl, self.tir_initial))

        lbl = QLabel(tr("App", "Número de Períodos:"))
        layout.addRow(lbl, self.tir_periods)
        self.eff_rate_fields[1].append((lbl, self.tir_periods))

        lbl = QLabel(tr("App", "Retorno por Período (R$):"))
        layout.addRow(lbl, self.tir_return)
        self.eff_rate_fields[1].append((lbl, self.tir_return))

        # Campos para Taxa Global (mode 2)
        self.eff_rate_fields[2] = []
        lbl = QLabel(tr("App", "Taxa Real Mensal (%):"))
        layout.addRow(lbl, self.tax_global_real)
        self.eff_rate_fields[2].append((lbl, self.tax_global_real))

        lbl = QLabel(tr("App", "Inflação Mês 1 (%):"))
        layout.addRow(lbl, self.tax_global_inf_m1)
        self.eff_rate_fields[2].append((lbl, self.tax_global_inf_m1))

        lbl = QLabel(tr("App", "Inflação Mês 2 (%):"))
        layout.addRow(lbl, self.tax_global_inf_m2)
        self.eff_rate_fields[2].append((lbl, self.tax_global_inf_m2))

        lbl = QLabel(tr("App", "Inflação Mês 3 (%):"))
        layout.addRow(lbl, self.tax_global_inf_m3)
        self.eff_rate_fields[2].append((lbl, self.tax_global_inf_m3))

        # Campos para Cobrança Antecipada (mode 3)
        self.eff_rate_fields[3] = []
        lbl = QLabel(tr("App", "Valor Nominal do Empréstimo (R$):"))
        layout.addRow(lbl, self.adv_int_nominal)
        self.eff_rate_fields[3].append((lbl, self.adv_int_nominal))

        lbl = QLabel(tr("App", "Taxa de Cobrança Antecipada (%):"))
        layout.addRow(lbl, self.adv_int_rate)
        self.eff_rate_fields[3].append((lbl, self.adv_int_rate))

        # Campos para TIR Modificada (mode 4)
        self.eff_rate_fields[4] = []
        lbl = QLabel(tr("App", "Investimento Inicial (R$):"))
        layout.addRow(lbl, self.tirm_initial)
        self.eff_rate_fields[4].append((lbl, self.tirm_initial))

        lbl = QLabel(tr("App", "Número de Períodos:"))
        layout.addRow(lbl, self.tirm_periods)
        self.eff_rate_fields[4].append((lbl, self.tirm_periods))

        lbl = QLabel(tr("App", "Retorno por Período (R$):"))
        layout.addRow(lbl, self.tirm_return)
        self.eff_rate_fields[4].append((lbl, self.tirm_return))

        lbl = QLabel(tr("App", "Taxa de Capitalização (%):"))
        layout.addRow(lbl, self.tirm_cap_rate)
        self.eff_rate_fields[4].append((lbl, self.tirm_cap_rate))

        # Campos para TMA vs Rentabilidade (mode 5)
        self.eff_rate_fields[5] = []
        lbl = QLabel(tr("App", "Capital (R$):"))
        layout.addRow(lbl, self.tma_capital)
        self.eff_rate_fields[5].append((lbl, self.tma_capital))

        lbl = QLabel(tr("App", "Taxa da Oportunidade (% ao mês):"))
        layout.addRow(lbl, self.tma_monthly_rate)
        self.eff_rate_fields[5].append((lbl, self.tma_monthly_rate))

        lbl = QLabel(tr("App", "TMA (% ao ano):"))
        layout.addRow(lbl, self.tma_rate)
        self.eff_rate_fields[5].append((lbl, self.tma_rate))

        lbl = QLabel(tr("App", "Número de Períodos (meses):"))
        layout.addRow(lbl, self.tma_periods)
        self.eff_rate_fields[5].append((lbl, self.tma_periods))

        # Campos para Juros Reais (mode 6)
        self.eff_rate_fields[6] = []
        lbl = QLabel(tr("App", "Capital (R$):"))
        layout.addRow(lbl, self.real_int_capital)
        self.eff_rate_fields[6].append((lbl, self.real_int_capital))

        lbl = QLabel(tr("App", "Taxa Global (% ao ano):"))
        layout.addRow(lbl, self.real_int_global_rate)
        self.eff_rate_fields[6].append((lbl, self.real_int_global_rate))

        lbl = QLabel(tr("App", "Inflação (% ao ano):"))
        layout.addRow(lbl, self.real_int_inflation)
        self.eff_rate_fields[6].append((lbl, self.real_int_inflation))

        layout.addRow(calc_button)
        layout.addRow(btn_widget)
        right_layout.addWidget(self.eff_rate_result)

        def toggle_fields():
            mode = self.eff_rate_calc_mode.currentIndex()

            # Ocultar todos os campos primeiro
            for mode_idx in range(7):
                if mode_idx in self.eff_rate_fields:
                    for lbl, field in self.eff_rate_fields[mode_idx]:
                        lbl.setVisible(False)
                        field.setVisible(False)

            # Mostrar apenas os campos do modo selecionado
            if mode in self.eff_rate_fields:
                for lbl, field in self.eff_rate_fields[mode]:
                    lbl.setVisible(True)
                    field.setVisible(True)

        self.eff_rate_calc_mode.currentIndexChanged.connect(toggle_fields)
        toggle_fields()

        def clear_inputs():
            self.eff_rate_nominal.clear()
            self.eff_rate_period_nominal.clear()
            self.eff_rate_period_cap.clear()
            self.eff_rate_period_target.clear()
            self.tir_initial.clear()
            self.tir_periods.clear()
            self.tir_return.clear()
            self.tax_global_real.clear()
            self.tax_global_inf_m1.clear()
            self.tax_global_inf_m2.clear()
            self.tax_global_inf_m3.clear()
            self.adv_int_nominal.clear()
            self.adv_int_rate.clear()
            self.tirm_initial.clear()
            self.tirm_periods.clear()
            self.tirm_return.clear()
            self.tirm_cap_rate.clear()
            self.tma_capital.clear()
            self.tma_monthly_rate.clear()
            self.tma_rate.clear()
            self.tma_periods.clear()
            self.real_int_capital.clear()
            self.real_int_global_rate.clear()
            self.real_int_inflation.clear()

        def clear_output():
            self.eff_rate_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

    except Exception as e:
        logger.error(f"Erro ao criar aba de taxa efetiva/TIR: {e}", exc_info=True)
        raise
