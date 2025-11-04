from PySide6.QtCore import QCoreApplication

def calculate_rate_equivalence(self):
    try:
        tr = QCoreApplication.translate
        i = self.get_float_from_line_edit(self.rate_equiv_i, is_percentage=True)
        n1 = self.get_float_from_line_edit(self.rate_equiv_current_n)
        n2 = self.get_float_from_line_edit(self.rate_equiv_target_n)

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
                '.': '·', '-': '⁻', '/': '⸍'
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

        # (1+i_eq) = (1+i)^(n2/n1)
        exponent = n2 / n1
        i_eq = (1 + i) ** exponent - 1

        steps = []
        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "EQUIVALÊNCIA DE TAXAS EFETIVAS") + "\n")
        steps.append("═" * 60 + "\n\n")

        steps.append(tr("App", "Fórmula:") + "\n")
        n1l, n2l, n3l = format_fraction("n₂", "n₁", prefix="  (1 + i_eq) = (1 + i)^")
        steps.append(n1l + "\n")
        steps.append(n2l + "\n")
        steps.append(n3l + "\n\n")

        steps.append(tr("App", "Dados do problema:") + "\n")
        steps.append(f"  i ({tr('App', 'Taxa conhecida')})     = {format_currency(i*100)}% {tr('App', 'ao período')} (n₁)\n")
        steps.append(f"  n₁ ({tr('App', 'Período atual')})     = {format_currency(n1)}\n")
        steps.append(f"  n₂ ({tr('App', 'Período desejado')})  = {format_currency(n2)}\n\n")

        steps.append(tr("App", "Desenvolvimento:") + "\n")
        n1e, n2e, n3e = format_fraction(format_currency(n2), format_currency(n1), prefix=f"  {tr('App', 'Expoente')}: ")
        steps.append(n1e + "\n")
        steps.append(n2e + "\n")
        steps.append(n3e + "\n")
        steps.append(f"  {tr('App', 'Expoente')} = {format_currency(exponent)}\n\n")

        exp_super = to_superscript(format_currency(exponent))
        steps.append(f"  (1 + i_eq) = (1 + {format_currency(i)}){exp_super}\n\n")

        pow_val = (1 + i) ** exponent
        steps.append(tr("App", "Cálculo do fator:") + "\n")
        steps.append(f"  (1 + i)^(n₂/n₁) = (1 + {format_currency(i)})^{format_currency(exponent)}\n")
        steps.append(f"  (1 + i)^(n₂/n₁) = {format_currency(pow_val)}\n\n")

        steps.append(tr("App", "Cálculo final:") + "\n")
        steps.append(f"  i_eq = {format_currency(pow_val)} - 1\n")
        steps.append(f"  i_eq = {format_currency(i_eq)}\n")
        steps.append(f"  i_eq = {format_currency(i_eq*100)}%\n\n")

        steps.append("─" * 60 + "\n")
        steps.append(tr("App", "RESPOSTA: A taxa equivalente é") + f" {format_currency(i_eq*100)}% {tr('App', 'ao período')} (n₂)\n")
        steps.append("─" * 60 + "\n")

        self.rate_equiv_result.append("".join(steps))

    except Exception as e:
        tr = QCoreApplication.translate
        self.rate_equiv_result.append(f"{tr('App', 'Erro')}: {e}")

def calculate_real_rate(self):
    try:
        tr = QCoreApplication.translate
        
        # Corrigido: usar índice ao invés de comparação de texto
        calc_apparent = self.rate_real_calc_type.currentIndex() == 0  # 0 = Calcular Taxa Aparente (i), 1 = Calcular Taxa Real (r)

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

        if calc_apparent:
            r = self.get_float_from_line_edit(self.rate_real_r, is_percentage=True)
            inflation = self.get_float_from_line_edit(self.rate_real_inflation, is_percentage=True)
            # 1+i = (1+r)*(1+inflation)
            i = (1 + r) * (1 + inflation) - 1

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "CÁLCULO DA TAXA APARENTE (i)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            steps.append("  1 + i = (1 + r) × (1 + θ)\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  r ({tr('App', 'Taxa real')})      = {format_currency(r*100)}%\n")
            steps.append(f"  θ ({tr('App', 'Inflação')})       = {format_currency(inflation*100)}%\n\n")

            steps.append(tr("App", "Desenvolvimento:") + "\n")
            steps.append(f"  1 + i = (1 + {format_currency(r)}) × (1 + {format_currency(inflation)})\n")
            steps.append(f"  1 + i = {format_currency(1 + r)} × {format_currency(1 + inflation)}\n\n")

            prod = (1 + r) * (1 + inflation)
            steps.append(tr("App", "Cálculo intermediário:") + "\n")
            steps.append(f"  (1 + r) × (1 + θ) = {format_currency(prod)}\n\n")

            steps.append(tr("App", "Cálculo final:") + "\n")
            steps.append(f"  i = {format_currency(prod)} - 1\n")
            steps.append(f"  i = {format_currency(i)}\n")
            steps.append(f"  i = {format_currency(i*100)}%\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA: A taxa aparente é") + f" {format_currency(i*100)}%\n")
            steps.append("─" * 60 + "\n")

            self.rate_real_result.append("".join(steps))

        else: # Calcular Taxa Real
            i = self.get_float_from_line_edit(self.rate_real_i, is_percentage=True)
            inflation = self.get_float_from_line_edit(self.rate_real_inflation, is_percentage=True)
            # 1+r = (1+i)/(1+inflation)
            r = (1 + i) / (1 + inflation) - 1

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "CÁLCULO DA TAXA REAL (r)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            f1, f2, f3 = format_fraction("(1 + i)", "(1 + θ)", prefix="  1 + r = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  i ({tr('App', 'Taxa aparente')})  = {format_currency(i*100)}%\n")
            steps.append(f"  θ ({tr('App', 'Inflação')})       = {format_currency(inflation*100)}%\n\n")

            steps.append(tr("App", "Desenvolvimento:") + "\n")
            steps.append(f"  1 + r = (1 + {format_currency(i)}) / (1 + {format_currency(inflation)})\n")
            steps.append(f"  1 + r = {format_currency(1 + i)} / {format_currency(1 + inflation)}\n\n")

            div = (1 + i) / (1 + inflation)
            steps.append(tr("App", "Cálculo intermediário:") + "\n")
            steps.append(f"  (1 + i) / (1 + θ) = {format_currency(div)}\n\n")

            steps.append(tr("App", "Cálculo final:") + "\n")
            steps.append(f"  r = {format_currency(div)} - 1\n")
            steps.append(f"  r = {format_currency(r)}\n")
            steps.append(f"  r = {format_currency(r*100)}%\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA: A taxa real é") + f" {format_currency(r*100)}%\n")
            steps.append("─" * 60 + "\n")

            self.rate_real_result.append("".join(steps))

    except Exception as e:
        tr = QCoreApplication.translate
        self.rate_real_result.append(f"{tr('App', 'Erro')}: {e}")
