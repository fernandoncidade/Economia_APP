from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_gradient(self):
    try:
        tr = QCoreApplication.translate

        # Corrigido: usar índice ao invés de comparação de texto
        calc_mode_index = self.grad_calc_mode.currentIndex()  # 0 = Calcular P, 1 = Calcular X_k, 2 = Renda Perpétua
        is_arithmetic = self.grad_type.currentIndex() == 0  # 0 = Gradiente Aritmético, 1 = Gradiente Geométrico

        result_text = ""

        # Normalização da formatação numérica/monetária
        def format_currency(value, decimals=2):
            s = f"{value:,.{decimals}f}"         # ex: "15,000.00"
            s = s.replace(",", "T")             # "15T000.00"
            s = s.replace(".", ",")             # "15T000,00"
            s = s.replace("T", ".")             # "15.000,00"
            return s

        # Função auxiliar para converter número em sobrescrito
        def to_superscript(num):
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                '.': '·', '-': '⁻'
            }
            return ''.join(superscript_map.get(c, c) for c in str(num))

        # Função auxiliar para converter número em subscrito
        def to_subscript(num):
            subscript_map = {
                '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
                '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
                '-': '₋', '+': '₊', '=': '₌', '(': '₍', ')': '₎'
            }
            return ''.join(subscript_map.get(c, c) for c in str(num))

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

        # Renda Perpétua (Série Perpétua)
        if calc_mode_index == 2:
            # Ler apenas os campos necessários para Renda Perpétua
            a = self.get_float_from_line_edit(self.grad_a)
            i = self.get_float_from_line_edit(self.grad_i, is_percentage=True)
            
            p = a / i

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "RENDA PERPÉTUA (SÉRIE PERPÉTUA)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            f1, f2, f3 = format_fraction("A", "i", prefix="  P = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  A ({tr('App', 'Renda mensal')})   = R$ {format_currency(a,2)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n\n")

            steps.append(tr("App", "Desenvolvimento:") + "\n")
            steps.append(f"  {tr('App', 'Para gerar juros perpétuos de')} R$ {format_currency(a,2)} {tr('App', 'por período,')}\n")
            steps.append(f"  {tr('App', 'o principal P deve ser tal que:')} P × i = A\n\n")

            steps.append(tr("App", "Cálculo:") + "\n")
            c1, c2, c3 = format_fraction(format_currency(a,2), format_currency(i,6), prefix="  P = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n")
            steps.append(f"  P = R$ {format_currency(p,2)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA: O capital necessário é R$") + f" {format_currency(p,2)}\n")
            steps.append("─" * 60 + "\n")

            result_text = "".join(steps)

        # Calcular X_k (k-ésimo termo do gradiente geométrico)
        elif calc_mode_index == 1 and not is_arithmetic:
            # Ler campos necessários para calcular X_k
            p = self.get_float_from_line_edit(self.grad_p)
            i = self.get_float_from_line_edit(self.grad_i, is_percentage=True)
            g = self.get_float_from_line_edit(self.grad_g, is_percentage=True)
            n = self.get_float_from_line_edit(self.grad_n)
            k = int(self.get_float_from_line_edit(self.grad_k))

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "GRADIENTE GEOMÉTRICO - CÁLCULO DO k-ÉSIMO TERMO") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Valor Presente')}) = R$ {format_currency(p,2)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  g ({tr('App', 'Crescimento')})    = {format_currency(g*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n, 0)}\n")
            steps.append(f"  k ({tr('App', 'Termo desejado')}) = {format_currency(k, 0)}\n\n")

            # Passo 1: Calcular X_1
            if abs(i - g) < 1e-10:  # i == g
                x1 = (p * (1 + i)) / n

                steps.append("─" * 60 + "\n")
                steps.append(f"1. {tr('App', 'CÁLCULO DO PRIMEIRO TERMO')} (X{to_subscript(1)})\n")
                steps.append("─" * 60 + "\n\n")

                steps.append(tr("App", "Como g = i, usa-se a fórmula simplificada:") + "\n")
                steps.append(f"  P = X{to_subscript(1)} × n / (1 + i)\n\n")

                steps.append(tr("App", "Isolando") + f" X{to_subscript(1)}:\n")
                steps.append(f"  X{to_subscript(1)} = P × (1 + i) / n\n\n")

                steps.append(tr("App", "Cálculo:") + "\n")
                steps.append(f"  X{to_subscript(1)} = {format_currency(p,2)} × {format_currency(1+i,6)} / {format_currency(n,0)}\n")
                steps.append(f"  X{to_subscript(1)} = {format_currency(p*(1+i),2)} / {format_currency(n,0)}\n")
                steps.append(f"  X{to_subscript(1)} = R$ {format_currency(x1,2)}\n\n")

            else:  # i ≠ g
                num = g - i
                r = (1 + g) / (1 + i)
                rn = r ** n
                den = rn - 1
                x1 = p * (num / den)

                steps.append("─" * 60 + "\n")
                steps.append(f"1. {tr('App', 'CÁLCULO DO PRIMEIRO TERMO')} (X{to_subscript(1)})\n")
                steps.append("─" * 60 + "\n\n")

                steps.append(tr("App", "Como g ≠ i, usa-se a fórmula:") + "\n")
                n1, n2, n3 = format_fraction("g - i", "((1+g)/(1+i))ⁿ - 1", prefix=f"  X{to_subscript(1)} = P × ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                n_super = to_superscript(int(n))

                steps.append(tr("App", "Cálculo da razão r:") + "\n")
                steps.append(f"  r = (1 + g) / (1 + i)\n")
                steps.append(f"  r = {format_currency(1+g,6)} / {format_currency(1+i,6)}\n")
                steps.append(f"  r = {format_currency(r,6)}\n\n")

                steps.append(tr("App", "Cálculo de rⁿ:") + "\n")
                steps.append(f"  rⁿ = {format_currency(r,6)}{n_super}\n")
                steps.append(f"  rⁿ = {format_currency(rn,6)}\n\n")

                steps.append("  " + tr("App", "Numerador:") + "\n")
                steps.append(f"    g - i = {format_currency(g,6)} - {format_currency(i,6)}\n")
                steps.append(f"    g - i = {format_currency(num,6)}\n\n")

                steps.append("  " + tr("App", "Denominador:") + "\n")
                steps.append(f"    rⁿ - 1 = {format_currency(rn,6)} - 1\n")
                steps.append(f"    rⁿ - 1 = {format_currency(den,6)}\n\n")

                steps.append(f"{tr('App', 'Cálculo de')} X{to_subscript(1)}:\n")
                c1, c2, c3 = format_fraction(format_currency(num,6), format_currency(den,6), prefix=f"  X{to_subscript(1)} = P × ")
                steps.append(c1 + "\n")
                steps.append(c2 + "\n")
                steps.append(c3 + "\n")
                steps.append(f"  X{to_subscript(1)} = {format_currency(p,2)} × {format_currency(num/den,6)}\n")
                steps.append(f"  X{to_subscript(1)} = R$ {format_currency(x1,2)}\n\n")

            # Passo 2: Calcular X_k
            xk = x1 * ((1 + g) ** (k - 1))

            steps.append("─" * 60 + "\n")
            steps.append(f"2. {tr('App', 'CÁLCULO DO TERMO')} X{to_subscript(k)}\n")
            steps.append("─" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            steps.append(f"  X{to_subscript('k')} = X{to_subscript(1)} × (1 + g){to_superscript('(k-1)')}\n\n")

            k_minus_1_super = to_superscript(k - 1)
            pow_g = (1 + g) ** (k - 1)

            steps.append(tr("App", "Cálculo:") + "\n")
            steps.append(f"  X{to_subscript(k)} = {format_currency(x1,2)} × (1 + {format_currency(g,6)}){k_minus_1_super}\n")
            steps.append(f"  X{to_subscript(k)} = {format_currency(x1,2)} × {format_currency(pow_g,6)}\n")
            steps.append(f"  X{to_subscript(k)} = R$ {format_currency(xk,2)}\n\n")

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA:") + "\n")
            steps.append(f"  X{to_subscript(1)} = R$ {format_currency(x1,2)}\n")
            steps.append(f"  X{to_subscript(k)} = R$ {format_currency(xk,2)}\n")
            steps.append("═" * 60 + "\n")

            result_text = "".join(steps)

        # Cálculo original de P (mantido para compatibilidade)
        elif calc_mode_index == 0:
            # Ler campos comuns para cálculo de P
            i = self.get_float_from_line_edit(self.grad_i, is_percentage=True)
            n = self.get_float_from_line_edit(self.grad_n)
            
            if is_arithmetic:
                g = self.get_float_from_line_edit(self.grad_g)
                # P = G/i * [(P/A, i, n) - n*(P/F, i, n)]
                pow_val = (1 + i) ** n
                num_pa = pow_val - 1
                den_pa = i * pow_val
                factor_pa = num_pa / den_pa
                factor_pf = 1 / pow_val
                p = (g / i) * (factor_pa - n * factor_pf)

                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "GRADIENTE ARITMÉTICO - CÁLCULO DO VALOR PRESENTE (P)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                n1, n2, n3 = format_fraction("G", "i", prefix="  P = ")
                steps.append(n1 + "\n")
                steps.append(n2 + " × [(P/A, i, n) - n × (P/F, i, n)]\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  G ({tr('App', 'Gradiente')})      = R$ {format_currency(g, 2)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n, 0)}\n\n")

                n_super = to_superscript(int(n))

                steps.append(tr("App", "Cálculo dos fatores:") + "\n")
                steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i,6)}){n_super}\n")
                steps.append(f"  (1 + i)ⁿ = {format_currency(pow_val,6)}\n\n")

                steps.append("  " + tr("App", "Fator (P/A, i, n):") + "\n")
                steps.append(f"    {tr('App', 'Numerador')}   = (1 + i)ⁿ - 1 = {format_currency(pow_val,6)} - 1\n")
                steps.append(f"                = {format_currency(num_pa,6)}\n")
                steps.append(f"    {tr('App', 'Denominador')} = i × (1 + i)ⁿ = {format_currency(i,6)} × {format_currency(pow_val,6)}\n")
                steps.append(f"                = {format_currency(den_pa,6)}\n")
                steps.append(f"    (P/A) = {format_currency(num_pa,6)} / {format_currency(den_pa,6)} = {format_currency(factor_pa,6)}\n\n")

                steps.append("  " + tr("App", "Fator (P/F, i, n):") + "\n")
                steps.append(f"    (P/F) = 1 / (1 + i)ⁿ\n")
                steps.append(f"    (P/F) = 1 / {format_currency(pow_val,6)}\n")
                steps.append(f"    (P/F) = {format_currency(factor_pf,6)}\n\n")

                steps.append(tr("App", "Desenvolvimento:") + "\n")
                steps.append(f"  G/i = {format_currency(g,2)} / {format_currency(i,6)}\n")
                steps.append(f"  G/i = {format_currency(g/i,2)}\n\n")

                term = factor_pa - n * factor_pf
                steps.append(f"  [(P/A) - n × (P/F)] = {format_currency(factor_pa,6)} - {format_currency(n,0)} × {format_currency(factor_pf,6)}\n")
                steps.append(f"                      = {format_currency(factor_pa - n*factor_pf,6)}\n")
                steps.append(f"                      = {format_currency(term,6)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  P = {format_currency(g/i,2)} × {format_currency(term,6)}\n")
                steps.append(f"  P = R$ {format_currency(p,2)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: O valor presente é R$") + f" {format_currency(p,2)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

            else: # Geométrico - cálculo de P
                g = self.get_float_from_line_edit(self.grad_g, is_percentage=True)
                x1_placeholder = 1

                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "GRADIENTE GEOMÉTRICO - CÁLCULO DO VALOR PRESENTE (P)") + "\n")
                steps.append("═" * 60 + "\n\n")

                if abs(i - g) < 1e-10:  # i == g
                    p = x1_placeholder * n / (1 + i)

                    steps.append(tr("App", "Fórmula (caso especial i = g):") + "\n")
                    n1, n2, n3 = format_fraction("n", "1 + i", prefix=f"  P = X{to_subscript(1)} × ")
                    steps.append(n1 + "\n")
                    steps.append(n2 + "\n")
                    steps.append(n3 + "\n\n")

                    steps.append(tr("App", "Dados do problema:") + "\n")
                    steps.append(f"  X{to_subscript(1)} ({tr('App', '1ª parcela')})    = R$ {format_currency(x1_placeholder,2)}\n")
                    steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
                    steps.append(f"  g ({tr('App', 'Crescimento')})    = {format_currency(g*100, 2)}% {tr('App', 'ao período')}\n")
                    steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n, 0)}\n\n")

                    steps.append(tr("App", "Observação: Como i = g, usa-se a fórmula simplificada.") + "\n\n")

                    steps.append(tr("App", "Desenvolvimento:") + "\n")
                    steps.append(f"  P = {format_currency(x1_placeholder,2)} × {format_currency(n,0)} / (1 + {format_currency(i,6)})\n")
                    steps.append(f"  P = {format_currency(x1_placeholder * n,2)} / {format_currency(1 + i,6)}\n\n")

                    steps.append(tr("App", "Cálculo final:") + "\n")
                    steps.append(f"  P = R$ {format_currency(p,2)}\n\n")

                    steps.append("─" * 60 + "\n")
                    steps.append(tr("App", "RESPOSTA: O valor presente é R$") + f" {format_currency(p,2)}\n")
                    steps.append("─" * 60 + "\n")

                else:  # i ≠ g
                    r = (1 + g) / (1 + i)
                    rn = r ** n
                    num = 1 - rn
                    den = i - g
                    p = x1_placeholder * num / den

                    steps.append(tr("App", "Fórmula:") + "\n")
                    num_str = f"1 - ((1 + g)/(1 + i)){to_superscript(int(n))}"
                    n1, n2, n3 = format_fraction(num_str, "i - g", prefix=f"  P = X{to_subscript(1)} × ")
                    steps.append(n1 + "\n")
                    steps.append(n2 + "\n")
                    steps.append(n3 + "\n\n")

                    steps.append(tr("App", "Dados do problema:") + "\n")
                    steps.append(f"  X{to_subscript(1)} ({tr('App', '1ª parcela')})    = R$ {format_currency(x1_placeholder,2)}\n")
                    steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
                    steps.append(f"  g ({tr('App', 'Crescimento')})    = {format_currency(g*100, 2)}% {tr('App', 'ao período')}\n")
                    steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n, 0)}\n\n")

                    n_super = to_superscript(int(n))

                    steps.append(tr("App", "Cálculo da razão r:") + "\n")
                    steps.append(f"  r = (1 + g) / (1 + i)\n")
                    steps.append(f"  r = (1 + {format_currency(g,6)}) / (1 + {format_currency(i,6)})\n")
                    steps.append(f"  r = {format_currency(1 + g,6)} / {format_currency(1 + i,6)}\n")
                    steps.append(f"  r = {format_currency(r,6)}\n\n")

                    steps.append(tr("App", "Cálculo de rⁿ:") + "\n")
                    steps.append(f"  rⁿ = {format_currency(r,6)}{n_super}\n")
                    steps.append(f"  rⁿ = {format_currency(rn,6)}\n\n")

                    steps.append("  " + tr("App", "Numerador:") + "\n")
                    steps.append(f"    1 - rⁿ = 1 - {format_currency(rn,6)}\n")
                    steps.append(f"    1 - rⁿ = {format_currency(num,6)}\n\n")

                    steps.append("  " + tr("App", "Denominador:") + "\n")
                    steps.append(f"    i - g = {format_currency(i,6)} - {format_currency(g,6)}\n")
                    steps.append(f"    i - g = {format_currency(den,6)}\n\n")

                    steps.append(tr("App", "Cálculo final:") + "\n")
                    steps.append(f"  P = {format_currency(x1_placeholder,2)} × {format_currency(num,6)} / {format_currency(den,6)}\n")
                    steps.append(f"  P = {format_currency(x1_placeholder,2)} × {format_currency(num/den,6)}\n")
                    steps.append(f"  P = R$ {format_currency(p,2)}\n\n")

                    steps.append("─" * 60 + "\n")
                    steps.append(tr("App", "RESPOSTA: O valor presente é R$") + f" {format_currency(p,2)}\n")
                    steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

        if result_text:
            self.grad_result.append(result_text)

    except Exception as e:
        logger.error(f"Erro ao calcular gradiente: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.grad_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
