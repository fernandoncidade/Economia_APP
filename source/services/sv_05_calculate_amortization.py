from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_amortization(self):
    try:
        tr = QCoreApplication.translate
        p = self.get_float_from_line_edit(self.amort_p)
        i = self.get_float_from_line_edit(self.amort_i, is_percentage=True)
        n = int(self.get_float_from_line_edit(self.amort_n))

        # Normalização da formatação numérica/monetária
        def format_currency(value, decimals=2):
            s = f"{value:,.{decimals}f}"
            s = s.replace(",", "T")
            s = s.replace(".", ",")
            s = s.replace("T", ".")
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
                '-': '₋', '+': '₊', '=': '₌'
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

        self.amort_table.setRowCount(n + 1)

        self.amort_table.setItem(0, 0, QTableWidgetItem("0"))
        for col in range(1, 4): self.amort_table.setItem(0, col, QTableWidgetItem("-"))
        self.amort_table.setItem(0, 4, QTableWidgetItem(format_currency(p, 2)))

        # Corrigido: usar índice ao invés de comparação de texto
        # 0 = Price, 1 = SAC, 2 = SAM, 3 = Americano, 4 = Hamburguês
        system_index = self.amort_system.currentIndex()

        steps = []

        if system_index == 1:  # SAC
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA SAC - AMORTIZAÇÃO CONSTANTE") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmulas:") + "\n")
            f1, f2, f3 = format_fraction("P", "n", prefix=f"  {tr('App', 'Amortização (constante)')}: A{to_subscript('k')} = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n")
            steps.append(f"  {tr('App', 'Juros')}:                   J{to_subscript('k')} = SD{to_subscript('k-1')} × i\n")
            steps.append(f"  {tr('App', 'Prestação')}:               PMT{to_subscript('k')} = A{to_subscript('k')} + J{to_subscript('k')}\n")
            steps.append(f"  {tr('App', 'Saldo Devedor')}:           SD{to_subscript('k')} = SD{to_subscript('k-1')} - A{to_subscript('k')}\n\n")

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

        elif system_index == 0:  # Sistema Francês (Price)
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA FRANCÊS (PRICE) - PRESTAÇÃO CONSTANTE") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmulas:") + "\n")
            f1, f2, f3 = format_fraction("i × (1 + i)ⁿ", "(1 + i)ⁿ - 1", prefix=f"  {tr('App', 'Fator (A/P)')} = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n")
            steps.append(f"  {tr('App', 'Prestação')}:       PMT = P × Fator(A/P)\n")
            steps.append(f"  {tr('App', 'Juros')}:           J{to_subscript('k')} = SD{to_subscript('k-1')} × i\n")
            steps.append(f"  {tr('App', 'Amortização')}:     A{to_subscript('k')} = PMT - J{to_subscript('k')}\n")
            steps.append(f"  {tr('App', 'Saldo Devedor')}:   SD{to_subscript('k')} = SD{to_subscript('k-1')} - A{to_subscript('k')}\n\n")

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

        elif system_index == 2:  # SAM
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

        elif system_index == 3:  # Sistema Americano
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA AMERICANO") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Características:") + "\n")
            steps.append(f"  • {tr('App', 'Períodos intermediários (k < n): Pagamento apenas de juros')}\n")
            steps.append(f"  • {tr('App', 'Amortização: Zero para k < n')}\n")
            steps.append(f"  • {tr('App', 'Saldo Devedor: Permanece igual a P até o último período')}\n")
            steps.append(f"  • {tr('App', 'Período final (k = n): Pagamento de juros + amortização total')}\n\n")

            steps.append(tr("App", "Fórmulas:") + "\n")
            steps.append(f"  {tr('App', 'Para k < n:')}\n")
            steps.append(f"    J{to_subscript('k')} = P × i\n")
            steps.append(f"    A{to_subscript('k')} = 0\n")
            steps.append(f"    PMT{to_subscript('k')} = J{to_subscript('k')}\n")
            steps.append(f"    SD{to_subscript('k')} = P\n\n")
            steps.append(f"  {tr('App', 'Para k = n:')}\n")
            steps.append(f"    J{to_subscript('n')} = P × i\n")
            steps.append(f"    A{to_subscript('n')} = P\n")
            steps.append(f"    PMT{to_subscript('n')} = J{to_subscript('n')} + A{to_subscript('n')} = P × (1 + i)\n")
            steps.append(f"    SD{to_subscript('n')} = 0\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Principal')})      = R$ {format_currency(p)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

            juros_periodo = p * i
            prest_intermediaria = juros_periodo
            prest_final = p * (1 + i)

            steps.append(tr("App", "Cálculos:") + "\n")
            steps.append(f"  {tr('App', 'Juros por período')}: J = P × i = {format_currency(p)} × {format_currency(i,6)}\n")
            steps.append(f"  {tr('App', 'Juros por período')}: J = R$ {format_currency(juros_periodo)}\n\n")

            steps.append(f"  {tr('App', 'Prestação intermediária')} (k < n): PMT = R$ {format_currency(prest_intermediaria)}\n")
            steps.append(f"  {tr('App', 'Prestação final')} (k = n): PMT = P + J = {format_currency(p)} + {format_currency(juros_periodo)}\n")
            steps.append(f"  {tr('App', 'Prestação final')}: PMT = R$ {format_currency(prest_final)}\n\n")

            # Exemplo do período 6
            if n >= 6:
                steps.append(tr("App", "Exemplo - Saldo Devedor após Período 6:") + "\n")
                steps.append(f"  {tr('App', 'Como k=6 < n=')}{n}, {tr('App', 'o saldo devedor permanece inalterado')}\n")
                steps.append(f"  SD₆ = P = R$ {format_currency(p)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "Tabela completa gerada abaixo") + "\n")
            steps.append("─" * 60 + "\n")

            self.amort_result.append("".join(steps))
            self.generate_american_table(p, i, n)

        elif system_index == 4:  # Sistema Hamburguês
            carencia_text = self.amort_carencia.text().strip()
            carencia = int(float(carencia_text)) if carencia_text else 0
            capitalizar = self.amort_juros_capitalizados.isChecked()

            # VALIDAÇÃO: Verificar se carência não é maior ou igual ao prazo total
            if carencia >= n:
                error_msg = tr("App", "Erro: O período de carência deve ser menor que o prazo total.")
                self.amort_result.append(error_msg)
                self.amort_table.setRowCount(1)
                self.amort_table.setSpan(0, 0, 1, 5)
                self.amort_table.setItem(0, 0, QTableWidgetItem(error_msg))
                return

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA HAMBURGUÊS (SAC COM CARÊNCIA)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Características:") + "\n")
            steps.append(f"  • {tr('App', 'Período de Carência: Sem amortização do principal')}\n")
            if capitalizar:
                steps.append(f"  • {tr('App', 'Juros na Carência: Capitalizados (incorporados ao saldo)')}\n")

            else:
                steps.append(f"  • {tr('App', 'Juros na Carência: Pagos mensalmente')}\n")

            steps.append(f"  • {tr('App', 'Período de Amortização: SAC sobre o saldo devedor')}\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Principal')})         = R$ {format_currency(p)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})              = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  n ({tr('App', 'Prazo total')})       = {format_currency(n,0)} {tr('App', 'períodos')}\n")
            steps.append(f"  {tr('App', 'Carência')}              = {format_currency(carencia,0)} {tr('App', 'períodos')}\n")
            steps.append(f"  {tr('App', 'Amortização')}           = {format_currency(n - carencia,0)} {tr('App', 'períodos')}\n\n")

            # Cálculo do saldo ao final da carência
            if capitalizar:
                pow_carencia = (1 + i) ** carencia
                saldo_pos_carencia = p * pow_carencia

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "FASE 1: PERÍODO DE CARÊNCIA (JUROS CAPITALIZADOS)") + "\n")
                steps.append("─" * 60 + "\n\n")

                car_super = to_superscript(int(carencia))
                steps.append(tr("App", "Saldo ao final da carência:") + "\n")
                steps.append(f"  SD{to_subscript(carencia)} = P × (1 + i){car_super}\n")
                steps.append(f"  SD{to_subscript(carencia)} = {format_currency(p)} × (1 + {format_currency(i,6)}){car_super}\n")
                steps.append(f"  SD{to_subscript(carencia)} = {format_currency(p)} × {format_currency(pow_carencia,6)}\n")
                steps.append(f"  SD{to_subscript(carencia)} = R$ {format_currency(saldo_pos_carencia)}\n\n")

            else:
                saldo_pos_carencia = p
                juros_carencia = p * i

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "FASE 1: PERÍODO DE CARÊNCIA (JUROS PAGOS)") + "\n")
                steps.append("─" * 60 + "\n\n")

                steps.append(tr("App", "Juros pagos mensalmente:") + "\n")
                steps.append(f"  J = P × i = {format_currency(p)} × {format_currency(i,6)}\n")
                steps.append(f"  J = R$ {format_currency(juros_carencia)}\n\n")
                steps.append(f"  {tr('App', 'Saldo devedor permanece constante')}: SD = R$ {format_currency(saldo_pos_carencia)}\n\n")

            # Fase de amortização
            n_amort = n - carencia
            amort_const = saldo_pos_carencia / n_amort

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "FASE 2: PERÍODO DE AMORTIZAÇÃO (SAC)") + "\n")
            steps.append("─" * 60 + "\n\n")

            steps.append(tr("App", "Amortização constante:") + "\n")
            a1, a2, a3 = format_fraction(format_currency(saldo_pos_carencia), format_currency(n_amort,0), prefix="  A = ")
            steps.append(a1 + "\n")
            steps.append(a2 + "\n")
            steps.append(a3 + "\n")
            steps.append(f"  A = R$ {format_currency(amort_const)}\n\n")

            # Exemplo do período 6 (primeiro período de amortização)
            periodo_6 = carencia + 1
            if n >= periodo_6:
                juros_6 = saldo_pos_carencia * i
                prest_6 = amort_const + juros_6

                steps.append(f"{tr('App', 'Exemplo - Período')} {periodo_6} ({tr('App', 'primeiro da amortização')}):\n")
                steps.append(f"  SD{to_subscript(carencia)} = R$ {format_currency(saldo_pos_carencia)}\n")
                steps.append(f"  J{to_subscript(periodo_6)} = SD{to_subscript(carencia)} × i = {format_currency(saldo_pos_carencia)} × {format_currency(i,6)}\n")
                steps.append(f"  J{to_subscript(periodo_6)} = R$ {format_currency(juros_6)}\n")
                steps.append(f"  PMT{to_subscript(periodo_6)} = A + J{to_subscript(periodo_6)} = {format_currency(amort_const)} + {format_currency(juros_6)}\n")
                steps.append(f"  PMT{to_subscript(periodo_6)} = R$ {format_currency(prest_6)}\n\n")

            # Comparação quando aplicável
            if carencia == 5 and n == 10:
                # Calcular cenário alternativo (juros não capitalizados)
                saldo_alt = p
                amort_alt = saldo_alt / n_amort
                juros_alt = saldo_alt * i
                prest_alt = amort_alt + juros_alt

                diferenca = prest_6 - prest_alt

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "COMPARAÇÃO DE CENÁRIOS") + "\n")
                steps.append("─" * 60 + "\n\n")

                steps.append(f"{tr('App', 'Prestação no período 6 (juros capitalizados)')}: R$ {format_currency(prest_6)}\n")
                steps.append(f"{tr('App', 'Prestação no período 6 (juros pagos)')}: R$ {format_currency(prest_alt)}\n")
                steps.append(f"{tr('App', 'Diferença')}: R$ {format_currency(diferenca)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "Tabela completa gerada abaixo") + "\n")
            steps.append("─" * 60 + "\n")

            self.amort_result.append("".join(steps))
            self.generate_hamburgues_table(p, i, n, carencia, capitalizar)

    except Exception as e:
        logger.error(f"Erro ao gerar tabela de amortização: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.amort_table.setRowCount(1)
            self.amort_table.setSpan(0,0,1,5)
            self.amort_table.setItem(0,0, QTableWidgetItem(f"{tr('App', 'Erro ao gerar tabela')}: {e}"))
            self.amort_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
