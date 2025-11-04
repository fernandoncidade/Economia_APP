from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QSizePolicy
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_17_history_container import HistoryContainer
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
            tr("App", "Taxa Global de Juros")
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

        # Validadores
        for field in [self.eff_rate_nominal, self.eff_rate_period_nominal, self.eff_rate_period_cap,
                      self.eff_rate_period_target, self.tir_initial, self.tir_periods, self.tir_return,
                      self.tax_global_real, self.tax_global_inf_m1, self.tax_global_inf_m2, self.tax_global_inf_m3]:
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

        # Campos para Taxa Efetiva
        layout.addRow(tr("App", "Taxa Nominal (%):"), self.eff_rate_nominal)
        layout.addRow(tr("App", "Período da Taxa Nominal:"), self.eff_rate_period_nominal)
        layout.addRow(tr("App", "Período de Capitalização:"), self.eff_rate_period_cap)
        layout.addRow(tr("App", "Período Desejado:"), self.eff_rate_period_target)

        # Campos para TIR
        layout.addRow(tr("App", "Investimento Inicial:"), self.tir_initial)
        layout.addRow(tr("App", "Número de Períodos:"), self.tir_periods)
        layout.addRow(tr("App", "Retorno por Período:"), self.tir_return)

        # Campos para Taxa Global
        layout.addRow(tr("App", "Taxa Real Mensal (%):"), self.tax_global_real)
        layout.addRow(tr("App", "Inflação Mês 1 (%):"), self.tax_global_inf_m1)
        layout.addRow(tr("App", "Inflação Mês 2 (%):"), self.tax_global_inf_m2)
        layout.addRow(tr("App", "Inflação Mês 3 (%):"), self.tax_global_inf_m3)

        layout.addRow(calc_button)
        layout.addRow(btn_widget)
        right_layout.addWidget(self.eff_rate_result)

        def toggle_fields():
            mode = self.eff_rate_calc_mode.currentIndex()

            # Taxa Efetiva
            show_effective = (mode == 0)
            self.eff_rate_nominal.setVisible(show_effective)
            self.eff_rate_period_nominal.setVisible(show_effective)
            self.eff_rate_period_cap.setVisible(show_effective)
            self.eff_rate_period_target.setVisible(show_effective)

            # TIR
            show_tir = (mode == 1)
            self.tir_initial.setVisible(show_tir)
            self.tir_periods.setVisible(show_tir)
            self.tir_return.setVisible(show_tir)

            # Taxa Global
            show_global = (mode == 2)
            self.tax_global_real.setVisible(show_global)
            self.tax_global_inf_m1.setVisible(show_global)
            self.tax_global_inf_m2.setVisible(show_global)
            self.tax_global_inf_m3.setVisible(show_global)

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
