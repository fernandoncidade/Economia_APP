from PySide6.QtCore import QCoreApplication

def calculate_gradient(self):
    try:
        tr = QCoreApplication.translate
        i = self.get_float_from_line_edit(self.grad_i, is_percentage=True)
        n = self.get_float_from_line_edit(self.grad_n)
        
        # Corrigido: usar índice ao invés de comparação de texto
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

        # Função auxiliar para formatar frações com numerador centralizado sobre o traço
        def format_fraction(numer_str, denom_str, prefix=""):
            # prefix será colocado somente na linha do traço
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

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

        else: # Geométrico
            g = self.get_float_from_line_edit(self.grad_g, is_percentage=True)
            x1_placeholder = 1

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "GRADIENTE GEOMÉTRICO - CÁLCULO DO VALOR PRESENTE (P)") + "\n")
            steps.append("═" * 60 + "\n\n")

            if abs(i - g) < 1e-10:  # i == g
                p = x1_placeholder * n / (1 + i)

                steps.append(tr("App", "Fórmula (caso especial i = g):") + "\n")
                n1, n2, n3 = format_fraction("n", "1 + i", prefix="  P = X₁ × ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  X₁ ({tr('App', '1ª parcela')})    = R$ {format_currency(x1_placeholder,2)}\n")
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
                n1, n2, n3 = format_fraction(num_str, "i - g", prefix="  P = X₁ × ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  X₁ ({tr('App', '1ª parcela')})    = R$ {format_currency(x1_placeholder,2)}\n")
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
        tr = QCoreApplication.translate
        self.grad_result.append(f"{tr('App', 'Erro')}: {e}")
