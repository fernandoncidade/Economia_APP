from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QCoreApplication

def calculate_amortization(self):
    try:
        tr = QCoreApplication.translate
        p = self.get_float_from_line_edit(self.amort_p)
        i = self.get_float_from_line_edit(self.amort_i, is_percentage=True)
        n = int(self.get_float_from_line_edit(self.amort_n))

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
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

        self.amort_table.setRowCount(n + 1)

        self.amort_table.setItem(0, 0, QTableWidgetItem("0"))
        for col in range(1, 4): self.amort_table.setItem(0, col, QTableWidgetItem("-"))
        self.amort_table.setItem(0, 4, QTableWidgetItem(format_currency(p, 2)))

        # Corrigido: usar índice ao invés de comparação de texto
        system_index = self.amort_system.currentIndex()  # 0 = SAC, 1 = Francês, 2 = SAM

        steps = []

        if system_index == 0:  # SAC
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA SAC - AMORTIZAÇÃO CONSTANTE") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmulas:") + "\n")
            f1, f2, f3 = format_fraction("P", "n", prefix=f"  {tr('App', 'Amortização (constante)')}: A_k = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n")
            steps.append(f"  {tr('App', 'Juros')}:                   J_k = SD_{{k-1}} × i\n")
            steps.append(f"  {tr('App', 'Prestação')}:               PMT_k = A_k + J_k\n")
            steps.append(f"  {tr('App', 'Saldo Devedor')}:           SD_k = SD_{{k-1}} - A_k\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Principal')})      = R$ {format_currency(p)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

            amort_const = p / n
            steps.append(tr("App", "Cálculo da amortização constante:") + "\n")
            a1, a2, a3 = format_fraction(format_currency(p), format_currency(n,0), prefix="  A = ")
            steps.append(a1 + "\n")
            steps.append(a2 + "\n")
            steps.append(a3 + "\n")
            steps.append(f"  A = R$ {format_currency(amort_const)}\n\n")

            juros1 = p * i
            prest1 = amort_const + juros1
            saldo1 = p - amort_const

            steps.append(tr("App", "Exemplo - Período 1:") + "\n")
            steps.append(f"  SD₀ = R$ {format_currency(p)}\n")
            steps.append(f"  J₁ = SD₀ × i = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(juros1)}\n")
            steps.append(f"  PMT₁ = A + J₁ = {format_currency(amort_const)} + {format_currency(juros1)} = R$ {format_currency(prest1)}\n")
            steps.append(f"  SD₁ = SD₀ - A = {format_currency(p)} - {format_currency(amort_const)} = R$ {format_currency(saldo1)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "Tabela completa gerada abaixo") + "\n")
            steps.append("─" * 60 + "\n")

            self.amort_result.append("".join(steps))
            self.generate_sac_table(p, i, n)

        elif system_index == 1:  # Sistema Francês
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA FRANCÊS (PRICE) - PRESTAÇÃO CONSTANTE") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmulas:") + "\n")
            f1, f2, f3 = format_fraction("i × (1 + i)ⁿ", "(1 + i)ⁿ - 1", prefix=f"  {tr('App', 'Fator (A/P)')} = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n")
            steps.append(f"  {tr('App', 'Prestação')}:       PMT = P × Fator(A/P)\n")
            steps.append(f"  {tr('App', 'Juros')}:           J_k = SD_{{k-1}} × i\n")
            steps.append(f"  {tr('App', 'Amortização')}:     A_k = PMT - J_k\n")
            steps.append(f"  {tr('App', 'Saldo Devedor')}:   SD_k = SD_{{k-1}} - A_k\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Principal')})      = R$ {format_currency(p)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

            n_super = to_superscript(int(n))
            pow_val = (1 + i)**n
            num = i * pow_val
            den = pow_val - 1
            factor = num / den
            prest = p * factor

            steps.append(tr("App", "Cálculo do fator (A/P):") + "\n")
            steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(i,6)}){n_super}\n")
            steps.append(f"  (1 + i)ⁿ = {format_currency(pow_val,6)}\n\n")

            steps.append("  " + tr("App", "Numerador:") + "\n")
            steps.append(f"    i × (1+i)ⁿ = {format_currency(i,6)} × {format_currency(pow_val,6)}\n")
            steps.append(f"                = {format_currency(num,6)}\n\n")
            steps.append("  " + tr("App", "Denominador:") + "\n")
            steps.append(f"    (1+i)ⁿ - 1 = {format_currency(pow_val,6)} - 1\n")
            steps.append(f"                = {format_currency(den,6)}\n\n")

            nf1, nf2, nf3 = format_fraction(format_currency(num,6), format_currency(den,6), prefix=f"  {tr('App', 'Fator (A/P)')} = ")
            steps.append(nf1 + "\n")
            steps.append(nf2 + "\n")
            steps.append(nf3 + f" = {format_currency(factor,6)}\n\n")

            steps.append(tr("App", "Cálculo da prestação constante:") + "\n")
            steps.append(f"  PMT = P × Fator(A/P)\n")
            steps.append(f"  PMT = {format_currency(p)} × {format_currency(factor,6)}\n")
            steps.append(f"  PMT = R$ {format_currency(prest)}\n\n")

            juros1 = p * i
            amort1 = prest - juros1
            saldo1 = p - amort1

            steps.append(tr("App", "Exemplo - Período 1:") + "\n")
            steps.append(f"  SD₀ = R$ {format_currency(p)}\n")
            steps.append(f"  J₁ = SD₀ × i = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(juros1)}\n")
            steps.append(f"  A₁ = PMT - J₁ = {format_currency(prest)} - {format_currency(juros1)} = R$ {format_currency(amort1)}\n")
            steps.append(f"  SD₁ = SD₀ - A₁ = {format_currency(p)} - {format_currency(amort1)} = R$ {format_currency(saldo1)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "Tabela completa gerada abaixo") + "\n")
            steps.append("─" * 60 + "\n")

            self.amort_result.append("".join(steps))
            self.generate_price_table(p, i, n)

        else:  # SAM (system_index == 2)
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA MISTO (SAM) - MÉDIA ENTRE SAC E PRICE") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Procedimento:") + "\n")
            steps.append(f"  {tr('App', 'Para cada período k:')}\n")
            steps.append(f"  1) {tr('App', 'Calcular valores do SAC:   PMT_SAC, J_SAC, A_SAC, SD_SAC')}\n")
            steps.append(f"  2) {tr('App', 'Calcular valores do PRICE: PMT_PRICE, J_PRICE, A_PRICE, SD_PRICE')}\n")
            steps.append(f"  3) {tr('App', 'Tirar a média aritmética de cada componente')}\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Principal')})      = R$ {format_currency(p)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

            # SAC
            amort_const = p / n
            sac_juros1 = p * i
            sac_prest1 = amort_const + sac_juros1
            sac_saldo1 = p - amort_const

            # PRICE
            n_super = to_superscript(int(n))
            pow_val = (1 + i)**n
            num = i * pow_val
            den = pow_val - 1
            factor = num / den
            price_prest = p * factor
            price_juros1 = p * i
            price_amort1 = price_prest - price_juros1
            price_saldo1 = p - price_amort1

            # SAM
            sam_prest1 = (sac_prest1 + price_prest) / 2
            sam_juros1 = (sac_juros1 + price_juros1) / 2
            sam_amort1 = (amort_const + price_amort1) / 2
            sam_saldo1 = (sac_saldo1 + price_saldo1) / 2

            steps.append(tr("App", "Exemplo - Período 1:") + "\n\n")

            steps.append("  SAC:\n")
            a1, a2, a3 = format_fraction(format_currency(p), format_currency(n,0), prefix="    A = ")
            steps.append(a1 + "\n")
            steps.append(a2 + "\n")
            steps.append(a3 + f" = R$ {format_currency(amort_const)}\n")
            steps.append(f"    J₁ = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(sac_juros1)}\n")
            steps.append(f"    PMT₁ = {format_currency(amort_const)} + {format_currency(sac_juros1)} = R$ {format_currency(sac_prest1)}\n")
            steps.append(f"    SD₁ = R$ {format_currency(sac_saldo1)}\n\n")

            steps.append("  PRICE:\n")
            f1, f2, f3 = format_fraction(format_currency(num,6), format_currency(den,6), prefix=f"    {tr('App', 'Fator')} = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + f" = {format_currency(factor,6)}\n")
            steps.append(f"    PMT = {format_currency(p)} × {format_currency(factor,6)} = R$ {format_currency(price_prest)}\n")
            steps.append(f"    J₁ = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(price_juros1)}\n")
            steps.append(f"    A₁ = {format_currency(price_prest)} - {format_currency(price_juros1)} = R$ {format_currency(price_amort1)}\n")
            steps.append(f"    SD₁ = R$ {format_currency(price_saldo1)}\n\n")

            steps.append(f"  SAM ({tr('App', 'Médias')}):\n")
            steps.append(f"    PMT₁ = ({format_currency(sac_prest1)} + {format_currency(price_prest)}) / 2 = R$ {format_currency(sam_prest1)}\n")
            steps.append(f"    J₁   = ({format_currency(sac_juros1)} + {format_currency(price_juros1)}) / 2 = R$ {format_currency(sam_juros1)}\n")
            steps.append(f"    A₁   = ({format_currency(amort_const)} + {format_currency(price_amort1)}) / 2 = R$ {format_currency(sam_amort1)}\n")
            steps.append(f"    SD₁  = ({format_currency(sac_saldo1)} + {format_currency(price_saldo1)}) / 2 = R$ {format_currency(sam_saldo1)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "Tabela completa gerada abaixo") + "\n")
            steps.append("─" * 60 + "\n")

            self.amort_result.append("".join(steps))
            self.generate_sam_table(p, i, n)

    except Exception as e:
        tr = QCoreApplication.translate
        self.amort_table.setRowCount(1)
        self.amort_table.setSpan(0,0,1,5)
        self.amort_table.setItem(0,0, QTableWidgetItem(f"{tr('App', 'Erro ao gerar tabela')}: {e}"))
        self.amort_result.append(f"{tr('App', 'Erro')}: {e}")
