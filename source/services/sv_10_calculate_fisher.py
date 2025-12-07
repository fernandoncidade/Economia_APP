from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_fisher(self):
    try:
        tr = QCoreApplication.translate

        calc_type = self.fisher_calc_type.currentIndex()

        if not self.fisher_inflation.text().strip():
            self.fisher_result.append(tr("App", "Erro: Taxa de Inflação é obrigatória"))
            return

        if calc_type == 0:
            if not self.fisher_tma_real.text().strip():
                self.fisher_result.append(tr("App", "Erro: TMA Real é obrigatória"))
                return

            _calculate_nominal_rate(self)

        else:  # Calcular Real
            if not self.fisher_tma_nominal.text().strip():
                self.fisher_result.append(tr("App", "Erro: TMA Nominal é obrigatória"))
                return

            _calculate_real_rate_fisher(self)

    except Exception as e:
        logger.error(f"Erro ao calcular Fisher: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.fisher_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass


def _calculate_nominal_rate(self):
    tr = QCoreApplication.translate
    r = self.get_float_from_line_edit(self.fisher_tma_real, is_percentage=True)
    theta = self.get_float_from_line_edit(self.fisher_inflation, is_percentage=True)

    def format_currency(value, decimals=2):
        s = f"{value:,.{decimals}f}"
        s = s.replace(",", "T")
        s = s.replace(".", ",")
        s = s.replace("T", ".")
        return s

    # Relação de Fisher: (1 + i) = (1 + r) × (1 + θ)
    factor_r = 1 + r
    factor_theta = 1 + theta
    factor_i = factor_r * factor_theta
    i = factor_i - 1

    steps = []
    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "CÁLCULO DA TMA NOMINAL (RELAÇÃO DE FISHER)") + "\n")
    steps.append("═" * 60 + "\n\n")

    steps.append(tr("App", "Dados do problema:") + "\n")
    steps.append(f"  TMA Real (r):       {format_currency(r * 100, 4)}% {tr('App', 'ao ano')}\n")
    steps.append(f"  {tr('App', 'Taxa de Inflação')} (θ): {format_currency(theta * 100, 4)}% {tr('App', 'ao ano')}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(tr("App", "RELAÇÃO DE FISHER") + "\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    steps.append("  1 + i = (1 + r) × (1 + θ)\n\n")

    steps.append(f"  {tr('App', 'Onde')}:\n")
    steps.append(f"    i = {tr('App', 'Taxa Nominal (ou Aparente)')}\n")
    steps.append(f"    r = {tr('App', 'Taxa Real')}\n")
    steps.append(f"    θ = {tr('App', 'Taxa de Inflação')}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(tr("App", "CÁLCULO:") + "\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(f"  1 + r = 1 + {format_currency(r, 6)}\n")
    steps.append(f"  1 + r = {format_currency(factor_r, 6)}\n\n")

    steps.append(f"  1 + θ = 1 + {format_currency(theta, 6)}\n")
    steps.append(f"  1 + θ = {format_currency(factor_theta, 6)}\n\n")

    steps.append(f"  1 + i = (1 + r) × (1 + θ)\n")
    steps.append(f"  1 + i = {format_currency(factor_r, 6)} × {format_currency(factor_theta, 6)}\n")
    steps.append(f"  1 + i = {format_currency(factor_i, 6)}\n\n")

    steps.append(f"  i = {format_currency(factor_i, 6)} - 1\n")
    steps.append(f"  i = {format_currency(i, 6)}\n")
    steps.append(f"  i = {format_currency(i * 100, 4)}%\n\n")

    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "RESPOSTA:") + "\n")
    steps.append(f"  {tr('App', 'A TMA Nominal para esse ano é de')} {format_currency(i * 100, 2)}%\n")
    steps.append("═" * 60 + "\n")

    self.fisher_result.append("".join(steps))


def _calculate_real_rate_fisher(self):
    tr = QCoreApplication.translate
    i = self.get_float_from_line_edit(self.fisher_tma_nominal, is_percentage=True)
    theta = self.get_float_from_line_edit(self.fisher_inflation, is_percentage=True)

    def format_currency(value, decimals=2):
        s = f"{value:,.{decimals}f}"
        s = s.replace(",", "T")
        s = s.replace(".", ",")
        s = s.replace("T", ".")
        return s

    def format_fraction(numer_str, denom_str, prefix=""):
        numer = str(numer_str)
        denom = str(denom_str)
        width = max(len(numer), len(denom), 3)
        pad = " " * len(prefix)
        numer_line = pad + numer.center(width)
        divider_line = prefix + "─" * width
        denom_line = pad + denom.center(width)
        return numer_line, divider_line, denom_line

    # Relação de Fisher rearranjada: (1 + r) = (1 + i) / (1 + θ)
    factor_i = 1 + i
    factor_theta = 1 + theta
    factor_r = factor_i / factor_theta
    r = factor_r - 1

    steps = []
    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "CÁLCULO DA TMA REAL (RELAÇÃO DE FISHER)") + "\n")
    steps.append("═" * 60 + "\n\n")

    steps.append(tr("App", "Dados do problema:") + "\n")
    steps.append(f"  TMA Nominal (i):    {format_currency(i * 100, 4)}% {tr('App', 'ao ano')}\n")
    steps.append(f"  {tr('App', 'Taxa de Inflação')} (θ): {format_currency(theta * 100, 4)}% {tr('App', 'ao ano')}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(tr("App", "RELAÇÃO DE FISHER (REARRANJADA)") + "\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(tr("App", "Fórmula original:") + "\n")
    steps.append("  1 + i = (1 + r) × (1 + θ)\n\n")

    steps.append(tr("App", "Rearranjando para isolar a taxa real:") + "\n")
    f1, f2, f3 = format_fraction("1 + i", "1 + θ", prefix="  1 + r = ")
    steps.append(f1 + "\n")
    steps.append(f2 + "\n")
    steps.append(f3 + "\n\n")

    steps.append(f"  {tr('App', 'Onde')}:\n")
    steps.append(f"    r = {tr('App', 'Taxa Real')}\n")
    steps.append(f"    i = {tr('App', 'Taxa Nominal (ou Aparente)')}\n")
    steps.append(f"    θ = {tr('App', 'Taxa de Inflação')}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(tr("App", "CÁLCULO:") + "\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(f"  1 + i = 1 + {format_currency(i, 6)}\n")
    steps.append(f"  1 + i = {format_currency(factor_i, 6)}\n\n")

    steps.append(f"  1 + θ = 1 + {format_currency(theta, 6)}\n")
    steps.append(f"  1 + θ = {format_currency(factor_theta, 6)}\n\n")

    nf1, nf2, nf3 = format_fraction(format_currency(factor_i, 6), format_currency(factor_theta, 6), prefix="  1 + r = ")
    steps.append(nf1 + "\n")
    steps.append(nf2 + "\n")
    steps.append(nf3 + f" = {format_currency(factor_r, 6)}\n\n")

    steps.append(f"  r = {format_currency(factor_r, 6)} - 1\n")
    steps.append(f"  r = {format_currency(r, 6)}\n")
    steps.append(f"  r = {format_currency(r * 100, 4)}%\n\n")

    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "RESPOSTA:") + "\n")
    steps.append(f"  {tr('App', 'A TMA Real para esse ano é de')} {format_currency(r * 100, 4)}%\n")
    steps.append("═" * 60 + "\n")

    self.fisher_result.append("".join(steps))
