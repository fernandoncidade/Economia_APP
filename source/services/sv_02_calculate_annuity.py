from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_annuity(self):
    try:
        tr = QCoreApplication.translate
        i = self.get_float_from_line_edit(self.annuity_i, is_percentage=True)
        n = self.get_float_from_line_edit(self.annuity_n)

        # Corrigido: usar índice ao invés de comparação de texto
        is_postecipada = self.annuity_type.currentIndex() == 0  # 0 = Postecipada, 1 = Antecipada
        calc_a = self.annuity_calc_type.currentIndex() == 0   # 0 = Calcular Prestação (A), 1 = Calcular P

        result_text = ""

        # Normalização da formatação numérica/monetária
        def format_currency(value, decimals=2):
            s = f"{value:,.{decimals}f}"     # ex: "15,000.00" ou "0.010000"
            s = s.replace(",", "T")         # "15T000.00"
            s = s.replace(".", ",")         # "15T000,00"
            s = s.replace("T", ".")         # "15.000,00"
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
            # prefix será colocado somente na linha do traço (ex.: "  A = P × ")
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

        if calc_a:
            p = self.get_float_from_line_edit(self.annuity_p)
            if is_postecipada:
                # Fator A/P
                pow_val = (1 + i) ** n
                num = i * pow_val
                den = pow_val - 1
                factor = num / den
                a = p * factor

                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "SÉRIE UNIFORME POSTECIPADA - CÁLCULO DA PRESTAÇÃO (A)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                n1, n2, n3 = format_fraction("i × (1 + i)ⁿ", "(1 + i)ⁿ - 1", prefix="  A = P × ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  P ({tr('App', 'Valor Presente')}) = R$ {format_currency(p)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n, 0)}\n\n")

                n_super = to_superscript(int(n))
                steps.append(tr("App", "Cálculo do fator (A/P):") + "\n")
                steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i,6)}){n_super}\n")
                steps.append(f"  (1 + i)ⁿ = {format_currency(pow_val,6)}\n\n")

                steps.append("  " + tr("App", "Numerador:") + "\n")
                steps.append(f"    i × (1 + i)ⁿ = {format_currency(i,6)} × {format_currency(pow_val,6)}\n")
                steps.append(f"    i × (1 + i)ⁿ = {format_currency(num,6)}\n\n")

                steps.append("  " + tr("App", "Denominador:") + "\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(pow_val,6)} - 1\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(den,6)}\n\n")

                steps.append("  " + tr("App", "Fator A/P:") + "\n")
                steps.append(f"    {format_currency(num,6)} / {format_currency(den,6)} = {format_currency(factor,6)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  A = {format_currency(p)} × {format_currency(factor,6)}\n")
                steps.append(f"  A = R$ {format_currency(a)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: A prestação é R$") + f" {format_currency(a)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

            else: # Antecipada
                pow_n = (1 + i) ** n
                pow_nm1 = (1 + i) ** (n - 1) if n > 0 else 1.0
                num = i * pow_nm1
                den = pow_n - 1
                factor = num / den if den != 0 else 0
                a = p * factor

                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "SÉRIE UNIFORME ANTECIPADA - CÁLCULO DA PRESTAÇÃO (A')") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                n1, n2, n3 = format_fraction("i × (1 + i)ⁿ⁻¹", "(1 + i)ⁿ - 1", prefix="  A' = P × ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  P ({tr('App', 'Valor Presente')}) = R$ {format_currency(p)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

                n_super = to_superscript(int(n))
                nm1_super = to_superscript(int(n - 1))

                steps.append(tr("App", "Cálculo do fator (A'/P):") + "\n")
                steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i,6)}){n_super}\n")
                steps.append(f"  (1 + i)ⁿ = {format_currency(pow_n,6)}\n\n")

                steps.append(f"  (1 + i)ⁿ⁻¹ = (1 + {format_currency(i,6)}){nm1_super}\n")
                steps.append(f"  (1 + i)ⁿ⁻¹ = {format_currency(pow_nm1,6)}\n\n")

                steps.append("  " + tr("App", "Numerador:") + "\n")
                steps.append(f"    i × (1 + i)ⁿ⁻¹ = {format_currency(i,6)} × {format_currency(pow_nm1,6)}\n")
                steps.append(f"    i × (1 + i)ⁿ⁻¹ = {format_currency(num,6)}\n\n")

                steps.append("  " + tr("App", "Denominador:") + "\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(pow_n,6)} - 1\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(den,6)}\n\n")

                steps.append("  " + tr("App", "Fator A'/P:") + "\n")
                steps.append(f"    {format_currency(num,6)} / {format_currency(den,6)} = {format_currency(factor,6)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  A' = {format_currency(p)} × {format_currency(factor,6)}\n")
                steps.append(f"  A' = R$ {format_currency(a)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: A prestação antecipada é R$") + f" {format_currency(a)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

            if result_text:
                self.annuity_result.append(result_text)

        else: # Calcular P
            a = self.get_float_from_line_edit(self.annuity_a)
            if is_postecipada:
                pow_val = (1 + i) ** n
                num = pow_val - 1
                den = i * pow_val
                factor = num / den
                p = a * factor

                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "SÉRIE UNIFORME POSTECIPADA - CÁLCULO DO VALOR PRESENTE (P)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                n1, n2, n3 = format_fraction("(1 + i)ⁿ - 1", "i × (1 + i)ⁿ", prefix="  P = A × ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  A ({tr('App', 'Prestação')})      = R$ {format_currency(a)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

                n_super = to_superscript(int(n))

                steps.append(tr("App", "Cálculo do fator (P/A):") + "\n")
                steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i,6)}){n_super}\n")
                steps.append(f"  (1 + i)ⁿ = {format_currency(pow_val,6)}\n\n")

                steps.append("  " + tr("App", "Numerador:") + "\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(pow_val,6)} - 1\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(num,6)}\n\n")

                steps.append("  " + tr("App", "Denominador:") + "\n")
                steps.append(f"    i × (1 + i)ⁿ = {format_currency(i,6)} × {format_currency(pow_val,6)}\n")
                steps.append(f"    i × (1 + i)ⁿ = {format_currency(den,6)}\n\n")

                steps.append("  " + tr("App", "Fator P/A:") + "\n")
                steps.append(f"    {format_currency(num,6)} / {format_currency(den,6)} = {format_currency(factor,6)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  P = {format_currency(a)} × {format_currency(factor,6)}\n")
                steps.append(f"  P = R$ {format_currency(p)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: O valor presente é R$") + f" {format_currency(p)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

            else: # Antecipada
                pow_n = (1 + i) ** n
                pow_nm1 = (1 + i) ** (n - 1) if n > 0 else 1.0
                num = pow_n - 1
                den = i * pow_nm1
                factor = num / den if den != 0 else 0
                p = a * factor

                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "SÉRIE UNIFORME ANTECIPADA - CÁLCULO DO VALOR PRESENTE (P)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                n1, n2, n3 = format_fraction("(1 + i)ⁿ - 1", "i × (1 + i)ⁿ⁻¹", prefix="  P = A' × ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  A' ({tr('App', 'Prestação')})     = R$ {format_currency(a)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

                n_super = to_superscript(int(n))
                nm1_super = to_superscript(int(n - 1))

                steps.append(tr("App", "Cálculo do fator (P/A'):") + "\n")
                steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i,6)}){n_super}\n")
                steps.append(f"  (1 + i)ⁿ = {format_currency(pow_n,6)}\n\n")

                steps.append(f"  (1 + i)ⁿ⁻¹ = (1 + {format_currency(i,6)}){nm1_super}\n")
                steps.append(f"  (1 + i)ⁿ⁻¹ = {format_currency(pow_nm1,6)}\n\n")

                steps.append("  " + tr("App", "Numerador:") + "\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(pow_n,6)} - 1\n")
                steps.append(f"    (1 + i)ⁿ - 1 = {format_currency(num,6)}\n\n")

                steps.append("  " + tr("App", "Denominador:") + "\n")
                steps.append(f"    i × (1 + i)ⁿ⁻¹ = {format_currency(i,6)} × {format_currency(pow_nm1,6)}\n")
                steps.append(f"    i × (1 + i)ⁿ⁻¹ = {format_currency(den,6)}\n\n")

                steps.append("  " + tr("App", "Fator P/A':") + "\n")
                steps.append(f"    {format_currency(num,6)} / {format_currency(den,6)} = {format_currency(factor,6)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  P = {format_currency(a)} × {format_currency(factor,6)}\n")
                steps.append(f"  P = R$ {format_currency(p)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: O valor presente é R$") + f" {format_currency(p)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

            if result_text:
                self.annuity_result.append(result_text)

    except Exception as e:
        logger.error(f"Erro ao calcular anuidades: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.annuity_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
