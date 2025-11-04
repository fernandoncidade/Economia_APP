from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_minimum_return(self):
    try:
        tr = QCoreApplication.translate
        
        aporte = self.get_float_from_line_edit(self.min_return_investment)
        tma_anual = self.get_float_from_line_edit(self.min_return_tma, is_percentage=True)
        periodos_ano = int(self.get_float_from_line_edit(self.min_return_periods))

        def format_currency(value, decimals=2):
            s = f"{value:,.{decimals}f}"
            s = s.replace(",", "T")
            s = s.replace(".", ",")
            s = s.replace("T", ".")
            return s

        def to_superscript(num):
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                '.': '·', '-': '⁻', '/': '⸍'
            }
            return ''.join(superscript_map.get(c, c) for c in str(num))

        def format_fraction(numer_str, denom_str, prefix=""):
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

        # Converter TMA anual para TMA do período
        expoente = 1 / periodos_ano
        tma_periodo = (1 + tma_anual) ** expoente - 1

        # Calcular juros mínimos
        juros_minimos = aporte * tma_periodo

        steps = []
        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "CÁLCULO DE RETORNO MÍNIMO BASEADO EM TMA") + "\n")
        steps.append("═" * 60 + "\n\n")

        steps.append(tr("App", "Dados do problema:") + "\n")
        steps.append(f"  {tr('App', 'Aporte (Investimento)')}: R$ {format_currency(aporte)}\n")
        steps.append(f"  {tr('App', 'TMA anual')}: {format_currency(tma_anual*100, 2)}%\n")
        steps.append(f"  {tr('App', 'Períodos por ano')}: {format_currency(periodos_ano, 0)}\n\n")

        steps.append("─" * 60 + "\n")
        steps.append(f"1. {tr('App', 'CONVERSÃO DA TMA ANUAL PARA TMA DO PERÍODO')}\n")
        steps.append("─" * 60 + "\n\n")

        steps.append(tr("App", "Fórmula de equivalência:") + "\n")
        n1, n2, n3 = format_fraction("1", "m", prefix="  i_período = (1 + i_anual)")
        steps.append(n1 + " - 1\n")
        steps.append(n2 + "\n")
        steps.append(n3 + "\n\n")

        exp_super = to_superscript(format_currency(expoente, 6))
        steps.append(tr("App", "Cálculo:") + "\n")
        steps.append(f"  i{to_superscript('período')} = (1 + {format_currency(tma_anual, 6)}){exp_super} - 1\n")
        pow_val = (1 + tma_anual) ** expoente
        steps.append(f"  i{to_superscript('período')} = {format_currency(pow_val, 6)} - 1\n")
        steps.append(f"  i{to_superscript('período')} = {format_currency(tma_periodo, 6)}\n")
        steps.append(f"  i{to_superscript('período')} = {format_currency(tma_periodo*100, 4)}%\n\n")

        steps.append("─" * 60 + "\n")
        steps.append(f"2. {tr('App', 'CÁLCULO DO RETORNO MÍNIMO POR PERÍODO')}\n")
        steps.append("─" * 60 + "\n\n")

        steps.append(tr("App", "Fórmula:") + "\n")
        steps.append(f"  {tr('App', 'Juros')} = {tr('App', 'Aporte')} × i{to_superscript('período')}\n\n")

        steps.append(tr("App", "Cálculo:") + "\n")
        steps.append(f"  {tr('App', 'Juros')} = {format_currency(aporte)} × {format_currency(tma_periodo, 6)}\n")
        steps.append(f"  {tr('App', 'Juros')} = R$ {format_currency(juros_minimos)}\n\n")

        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "RESPOSTA:") + "\n")
        steps.append(f"  {tr('App', 'Retorno mínimo por período')}: R$ {format_currency(juros_minimos, 2)}\n")
        steps.append("═" * 60 + "\n")

        result_text = "".join(steps)
        self.min_return_result.append(result_text)

    except Exception as e:
        logger.error(f"Erro ao calcular retorno mínimo: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.min_return_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
