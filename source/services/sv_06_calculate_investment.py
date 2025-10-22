from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_investment(self):
    try:
        tr = QCoreApplication.translate
        inv_inicial = self.get_float_from_line_edit(self.invest_initial)
        a = self.get_float_from_line_edit(self.invest_cashflow)
        n = self.get_float_from_line_edit(self.invest_n)
        tma = self.get_float_from_line_edit(self.invest_tma, is_percentage=True)

        # Normalização da formatação numérica/monetária
        def format_currency(value):
            s = f"{value:,.2f}"         # ex: "15,000.00"
            s = s.replace(",", "T")     # "15T000.00"
            s = s.replace(".", ",")     # "15T000,00"
            s = s.replace("T", ".")     # "15.000,00"
            return s

        # Função auxiliar para converter número em sobrescrito
        def to_superscript(num):
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                '.': '·', '-': '⁻'
            }
            return ''.join(superscript_map.get(c, c) for c in str(num))

        # Função auxiliar para formatar frações com numerador centralizado sobre o traço
        def format_fraction(numer_str, denom_str, prefix=""):
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

        # VPL = VPB - VPC
        pow_val = (1 + tma) ** n
        num_pa = pow_val - 1
        den_pa = tma * pow_val
        factor_pa = num_pa / den_pa
        vpb = a * factor_pa
        vpl = vpb - inv_inicial

        # VAUE = VPL * (A/P, tma, n)
        num_ap = tma * pow_val
        den_ap = pow_val - 1
        factor_ap = num_ap / den_ap
        vaue = vpl * factor_ap

        steps = []
        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "ANÁLISE DE INVESTIMENTOS - VPL E VAUE") + "\n")
        steps.append("═" * 60 + "\n\n")

        steps.append(tr("App", "Dados do problema:") + "\n")
        steps.append(f"  {tr('App', 'Investimento Inicial')}   = R$ {format_currency(inv_inicial)}\n")
        steps.append(f"  {tr('App', 'Fluxo de Caixa')} (A)     = R$ {format_currency(a)} {tr('App', 'por período')}\n")
        steps.append(f"  {tr('App', 'Períodos')} (n)           = {format_currency(n)}\n")
        steps.append(f"  TMA                    = {format_currency(tma*100)}% {tr('App', 'ao período')}\n\n")

        n_super = to_superscript(int(n))

        steps.append("─" * 60 + "\n")
        steps.append(f"1. {tr('App', 'CÁLCULO DO VPB (Valor Presente dos Benefícios)')}\n")
        steps.append("─" * 60 + "\n\n")

        steps.append(tr("App", "Fórmula:") + "\n")
        f1, f2, f3 = format_fraction("(1 + TMA)ⁿ - 1", "TMA × (1 + TMA)ⁿ", prefix="  VPB = A × ")
        steps.append(f1 + "\n")
        steps.append(f2 + "\n")
        steps.append(f3 + "\n\n")

        steps.append(tr("App", "Cálculo do fator (P/A):") + "\n")
        steps.append(f"  (1 + TMA)ⁿ = (1 + {format_currency(tma)}){n_super}\n")
        steps.append(f"  (1 + TMA)ⁿ = {format_currency(pow_val)}\n\n")

        steps.append(f"  {tr('App', 'Numerador')}   = (1+TMA)ⁿ - 1 = {format_currency(pow_val)} - 1 = {format_currency(num_pa)}\n")
        steps.append(f"  {tr('App', 'Denominador')} = TMA × (1+TMA)ⁿ = {format_currency(tma)} × {format_currency(pow_val)} = {format_currency(den_pa)}\n")
        nf1, nf2, nf3 = format_fraction(format_currency(num_pa), format_currency(den_pa), prefix=f"  {tr('App', 'Fator')} (P/A) = ")
        steps.append(nf1 + "\n")
        steps.append(nf2 + "\n")
        steps.append(nf3 + f" = {format_currency(factor_pa)}\n\n")

        steps.append(tr("App", "Cálculo do VPB:") + "\n")
        steps.append(f"  VPB = A × {tr('App', 'Fator')}(P/A)\n")
        steps.append(f"  VPB = {format_currency(a)} × {format_currency(factor_pa)}\n")
        steps.append(f"  VPB = R$ {format_currency(vpb)}\n\n")

        steps.append("─" * 60 + "\n")
        steps.append(f"2. {tr('App', 'CÁLCULO DO VPL (Valor Presente Líquido)')}\n")
        steps.append("─" * 60 + "\n\n")

        steps.append(tr("App", "Fórmula:") + "\n")
        steps.append("  VPL = VPB - VPC\n")
        steps.append(f"  VPC = {tr('App', 'Investimento Inicial')}\n\n")

        steps.append(tr("App", "Cálculo:") + "\n")
        steps.append(f"  VPC = R$ {format_currency(inv_inicial)}\n")
        steps.append(f"  VPL = {format_currency(vpb)} - {format_currency(inv_inicial)}\n")
        steps.append(f"  VPL = R$ {format_currency(vpl)}\n\n")

        steps.append("─" * 60 + "\n")
        steps.append(f"3. {tr('App', 'CÁLCULO DA VAUE (Valor Anual Uniforme Equivalente)')}\n")
        steps.append("─" * 60 + "\n\n")

        steps.append(tr("App", "Fórmula:") + "\n")
        steps.append(f"  VAUE = VPL × {tr('App', 'Fator')}(A/P)\n\n")

        steps.append(tr("App", "Cálculo do fator (A/P):") + "\n")
        steps.append(f"  {tr('App', 'Numerador')}   = TMA × (1+TMA)ⁿ = {format_currency(tma)} × {format_currency(pow_val)} = {format_currency(num_ap)}\n")
        steps.append(f"  {tr('App', 'Denominador')} = (1+TMA)ⁿ - 1 = {format_currency(pow_val)} - 1 = {format_currency(den_ap)}\n")
        af1, af2, af3 = format_fraction(format_currency(num_ap), format_currency(den_ap), prefix=f"  {tr('App', 'Fator')} (A/P) = ")
        steps.append(af1 + "\n")
        steps.append(af2 + "\n")
        steps.append(af3 + f" = {format_currency(factor_ap)}\n\n")

        steps.append(tr("App", "Cálculo da VAUE:") + "\n")
        steps.append(f"  VAUE = {format_currency(vpl)} × {format_currency(factor_ap)}\n")
        steps.append(f"  VAUE = R$ {format_currency(vaue)}\n\n")

        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "CONCLUSÃO") + "\n")
        steps.append("═" * 60 + "\n\n")

        if vpl > 0:
            steps.append(f"  VPL = R$ {format_currency(vpl)} > 0\n")
            steps.append(f"  VAUE = R$ {format_currency(vaue)} > 0\n\n")
            steps.append(f"  ✓ {tr('App', 'O projeto é VIÁVEL economicamente')}\n")
            steps.append(f"  ✓ {tr('App', 'O investimento proporciona retorno acima da TMA')}\n")

        elif vpl < 0:
            steps.append(f"  VPL = R$ {format_currency(vpl)} < 0\n")
            steps.append(f"  VAUE = R$ {format_currency(vaue)} < 0\n\n")
            steps.append(f"  ✗ {tr('App', 'O projeto é INVIÁVEL economicamente')}\n")
            steps.append(f"  ✗ {tr('App', 'O investimento não atinge a TMA desejada')}\n")

        else:
            steps.append(f"  VPL = R$ {format_currency(vpl)} = 0\n")
            steps.append(f"  VAUE = R$ {format_currency(vaue)} = 0\n\n")
            steps.append(f"  ~ {tr('App', 'O projeto está no limite de viabilidade')}\n")
            steps.append(f"  ~ {tr('App', 'O investimento retorna exatamente a TMA')}\n")

        steps.append("\n" + "─" * 60 + "\n")

        self.invest_result.append("".join(steps))

    except Exception as e:
        logger.error(f"Erro ao calcular investimento (VPL/VAUE): {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.invest_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
