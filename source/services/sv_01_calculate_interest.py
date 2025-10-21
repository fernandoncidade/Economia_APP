from PySide6.QtCore import QCoreApplication

def calculate_interest(self):
    try:
        tr = QCoreApplication.translate
        i = self.get_float_from_line_edit(self.interest_i, is_percentage=True)
        n = self.get_float_from_line_edit(self.interest_n)

        # Corrigido: usar índice ao invés de comparação de texto
        is_compound = self.interest_regime.currentIndex() == 0  # 0 = Juros Compostos, 1 = Juros Simples
        calc_f = self.interest_calc_type.currentIndex() == 0   # 0 = Calcular Montante (F), 1 = Calcular Principal (P)

        result_text = ""

        # Função auxiliar para converter número em sobrescrito
        def to_superscript(num):
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                '.': '·', '-': '⁻'
            }
            return ''.join(superscript_map.get(c, c) for c in str(num))

        # Normalização da formatação numérica/monetária
        def format_currency(value):
            s = f"{value:,.2f}"         # ex: "15,000.00"
            s = s.replace(",", "T")     # "15T000.00"
            s = s.replace(".", ",")     # "15T000,00"
            s = s.replace("T", ".")     # "15.000,00"
            return s

        # Função auxiliar para formatar frações com numerador centralizado sobre o traço
        def format_fraction(numer_str, denom_str, prefix=""):
            # prefix é aplicado somente na linha do traço (ex.: "  P = ")
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

        if calc_f:
            p = self.get_float_from_line_edit(self.interest_p)
            if is_compound:
                f = p * (1 + i) ** n
                # Formatação didática
                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "JUROS COMPOSTOS - CÁLCULO DO MONTANTE (F)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                steps.append("  F = P × (1 + i)ⁿ\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  P ({tr('App', 'Principal')})      = R$ {format_currency(p)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {int(n)}\n\n")

                steps.append(tr("App", "Desenvolvimento:") + "\n")
                n_super = to_superscript(int(n))
                steps.append(f"  F = {format_currency(p)} × (1 + {format_currency(i)}){n_super}\n\n")

                pow_val = (1 + i) ** n
                steps.append(tr("App", "Cálculo do fator:") + "\n")
                steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i)}){n_super}\n")
                steps.append(f"  (1 + i)ⁿ = {format_currency(pow_val)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  F = {format_currency(p)} × {format_currency(pow_val)}\n")
                steps.append(f"  F = R$ {format_currency(f)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: O montante final é R$") + f" {format_currency(f)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

            else: # Juros Simples
                f = p * (1 + n * i)
                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "JUROS SIMPLES - CÁLCULO DO MONTANTE (F)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                steps.append("  F = P × (1 + n × i)\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  P ({tr('App', 'Principal')})      = R$ {format_currency(p)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {int(n)}\n\n")

                steps.append(tr("App", "Desenvolvimento:") + "\n")
                steps.append(f"  F = {format_currency(p)} × (1 + {int(n)} × {format_currency(i)})\n\n")

                interp = 1 + n * i
                steps.append(tr("App", "Cálculo do fator:") + "\n")
                steps.append(f"  1 + n × i = 1 + {int(n)} × {format_currency(i)}\n")
                steps.append(f"  1 + n × i = 1 + {format_currency(n*i)}\n")
                steps.append(f"  1 + n × i = {format_currency(interp)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  F = {format_currency(p)} × {format_currency(interp)}\n")
                steps.append(f"  F = R$ {format_currency(f)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: O montante final é R$") + f" {format_currency(f)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

        else: # Calcular Principal (P)
            f = self.get_float_from_line_edit(self.interest_f)
            if is_compound:
                p = f / (1 + i) ** n
                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "JUROS COMPOSTOS - CÁLCULO DO PRINCIPAL (P)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                # P = F / (1 + i)^n como fração alinhada
                n1, n2, n3 = format_fraction("F", "(1 + i)ⁿ", prefix="  P = ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  F ({tr('App', 'Montante')})       = R$ {format_currency(f)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {int(n)}\n\n")

                steps.append(tr("App", "Desenvolvimento:") + "\n")
                n_super = to_superscript(int(n))
                steps.append(f"  P = {format_currency(f)} / (1 + {format_currency(i)}){n_super}\n\n")

                denom = (1 + i) ** n
                steps.append(tr("App", "Cálculo do fator:") + "\n")
                steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i)}){n_super}\n")
                steps.append(f"  (1 + i)ⁿ = {format_currency(denom)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  P = {format_currency(f)} / {format_currency(denom)}\n")
                steps.append(f"  P = R$ {format_currency(p)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: O principal necessário é R$") + f" {format_currency(p)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

            else: # Juros Simples
                p = f / (1 + n * i)
                steps = []
                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "JUROS SIMPLES - CÁLCULO DO PRINCIPAL (P)") + "\n")
                steps.append("═" * 60 + "\n\n")

                steps.append(tr("App", "Fórmula:") + "\n")
                # P = F / (1 + n × i) como fração alinhada
                n1, n2, n3 = format_fraction("F", "1 + n × i", prefix="  P = ")
                steps.append(n1 + "\n")
                steps.append(n2 + "\n")
                steps.append(n3 + "\n\n")

                steps.append(tr("App", "Dados do problema:") + "\n")
                steps.append(f"  F ({tr('App', 'Montante')})       = R$ {format_currency(f)}\n")
                steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100)}% {tr('App', 'ao período')}\n")
                steps.append(f"  n ({tr('App', 'Períodos')})       = {int(n)}\n\n")

                steps.append(tr("App", "Desenvolvimento:") + "\n")
                steps.append(f"  P = {format_currency(f)} / (1 + {int(n)} × {format_currency(i)})\n\n")

                denom = 1 + n * i
                steps.append(tr("App", "Cálculo do fator:") + "\n")
                steps.append(f"  1 + n × i = 1 + {int(n)} × {format_currency(i)}\n")
                steps.append(f"  1 + n × i = 1 + {format_currency(n*i)}\n")
                steps.append(f"  1 + n × i = {format_currency(denom)}\n\n")

                steps.append(tr("App", "Cálculo final:") + "\n")
                steps.append(f"  P = {format_currency(f)} / {format_currency(denom)}\n")
                steps.append(f"  P = R$ {format_currency(p)}\n\n")

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA: O principal necessário é R$") + f" {format_currency(p)}\n")
                steps.append("─" * 60 + "\n")

                result_text = "".join(steps)

        # Anexa o resultado preservando o anterior
        if result_text:
            self.interest_result.append(result_text)

    except Exception as e:
        tr = QCoreApplication.translate
        self.interest_result.append(f"{tr('App', 'Erro')}: {e}")
