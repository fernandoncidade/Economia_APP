from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager
from utils.TextFormat import format_currency, to_superscript, to_subscript, format_fraction

logger = LogManager.get_logger()

def calculate_amortization(self):
    try:
        tr = QCoreApplication.translate
        p = self.get_float_from_line_edit(self.amort_p)
        i = self.get_float_from_line_edit(self.amort_i, is_percentage=True)
        n = int(self.get_float_from_line_edit(self.amort_n))

        # Função auxiliar para criar variáveis com subscrito usando sintaxe _{idx}
        def var_with_sub(var_name: str, idx: str) -> str:
            return f"{var_name}_{{{idx}}}"

        self.amort_table.setRowCount(n + 1)

        self.amort_table.setItem(0, 0, QTableWidgetItem("0"))
        for col in range(1, 4): self.amort_table.setItem(0, col, QTableWidgetItem("-"))
        self.amort_table.setItem(0, 4, QTableWidgetItem(format_currency(p, 2)))

        # Corrigido: usar índice ao invés de comparação de texto
        # 0 = Price, 1 = SAC, 2 = SAM, 3 = Americano, 4 = Hamburguês
        system_index = self.amort_system.currentIndex()

        # Labels com subscrito para uso consistente
        J_k = var_with_sub("J", "k")
        A_k = var_with_sub("A", "k")
        SD_k = var_with_sub("SD", "k")
        SD_k_1 = var_with_sub("SD", "k-1")
        PMT_k = var_with_sub("PMT", "k")

        steps = []

        if system_index == 1:  # SAC
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "SISTEMA SAC - AMORTIZAÇÃO CONSTANTE") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmulas:") + "\n")
            f1, f2, f3 = format_fraction("P", "n", prefix=f"  {tr('App', 'Amortização (constante)')}: {A_k} = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n")
            steps.append(f"  {tr('App', 'Juros')}:                   {J_k} = {SD_k_1} × i\n")
            steps.append(f"  {tr('App', 'Prestação')}:               {PMT_k} = {A_k} + {J_k}\n")
            steps.append(f"  {tr('App', 'Saldo Devedor')}:           {SD_k} = {SD_k_1} - {A_k}\n\n")

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

            J_1 = var_with_sub("J", "1")
            PMT_1 = var_with_sub("PMT", "1")
            SD_0 = var_with_sub("SD", "0")
            SD_1 = var_with_sub("SD", "1")

            steps.append(tr("App", "Exemplo - Período 1:") + "\n")
            steps.append(f"  {SD_0} = R$ {format_currency(p)}\n")
            steps.append(f"  {J_1} = {SD_0} × i = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(juros1)}\n")
            steps.append(f"  {PMT_1} = A + {J_1} = {format_currency(amort_const)} + {format_currency(juros1)} = R$ {format_currency(prest1)}\n")
            steps.append(f"  {SD_1} = {SD_0} - A = {format_currency(p)} - {format_currency(amort_const)} = R$ {format_currency(saldo1)}\n\n")

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
            n_super = to_superscript("n")
            f1, f2, f3 = format_fraction(f"i × (1 + i){n_super}", f"(1 + i){n_super} - 1", prefix=f"  {tr('App', 'Fator (A/P)')} = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n")
            steps.append(f"  {tr('App', 'Prestação')}:       PMT = P × Fator(A/P)\n")
            steps.append(f"  {tr('App', 'Juros')}:           {J_k} = {SD_k_1} × i\n")
            steps.append(f"  {tr('App', 'Amortização')}:     {A_k} = PMT - {J_k}\n")
            steps.append(f"  {tr('App', 'Saldo Devedor')}:   {SD_k} = {SD_k_1} - {A_k}\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Principal')})      = R$ {format_currency(p)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})           = {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
            steps.append(f"  n ({tr('App', 'Períodos')})       = {format_currency(n,0)}\n\n")

            n_super_val = to_superscript(int(n))
            pow_val = (1 + i)**n
            num = i * pow_val
            den = pow_val - 1
            factor = num / den
            prest = p * factor

            steps.append(tr("App", "Cálculo do fator (A/P):") + "\n")
            steps.append(f"  (1 + i){n_super} = (1 + {format_currency(i,6)}){n_super_val}\n")
            steps.append(f"  (1 + i){n_super} = {format_currency(pow_val,6)}\n\n")

            steps.append("  " + tr("App", "Numerador:") + "\n")
            steps.append(f"    i × (1+i){n_super} = {format_currency(i,6)} × {format_currency(pow_val,6)}\n")
            steps.append(f"                = {format_currency(num,6)}\n\n")
            steps.append("  " + tr("App", "Denominador:") + "\n")
            steps.append(f"    (1+i){n_super} - 1 = {format_currency(pow_val,6)} - 1\n")
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

            J_1 = var_with_sub("J", "1")
            A_1 = var_with_sub("A", "1")
            SD_0 = var_with_sub("SD", "0")
            SD_1 = var_with_sub("SD", "1")

            steps.append(tr("App", "Exemplo - Período 1:") + "\n")
            steps.append(f"  {SD_0} = R$ {format_currency(p)}\n")
            steps.append(f"  {J_1} = {SD_0} × i = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(juros1)}\n")
            steps.append(f"  {A_1} = PMT - {J_1} = {format_currency(prest)} - {format_currency(juros1)} = R$ {format_currency(amort1)}\n")
            steps.append(f"  {SD_1} = {SD_0} - {A_1} = {format_currency(p)} - {format_currency(amort1)} = R$ {format_currency(saldo1)}\n\n")

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
            PMT_SAC = var_with_sub("PMT", "SAC")
            J_SAC = var_with_sub("J", "SAC")
            A_SAC = var_with_sub("A", "SAC")
            SD_SAC = var_with_sub("SD", "SAC")
            PMT_PRICE = var_with_sub("PMT", "PRICE")
            J_PRICE = var_with_sub("J", "PRICE")
            A_PRICE = var_with_sub("A", "PRICE")
            SD_PRICE = var_with_sub("SD", "PRICE")

            steps.append(f"  1) {tr('App', 'Calcular valores do SAC')}: {PMT_SAC}, {J_SAC}, {A_SAC}, {SD_SAC}\n")
            steps.append(f"  2) {tr('App', 'Calcular valores do PRICE')}: {PMT_PRICE}, {J_PRICE}, {A_PRICE}, {SD_PRICE}\n")
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
            n_super = to_superscript("n")
            n_super_val = to_superscript(int(n))
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

            J_1 = var_with_sub("J", "1")
            PMT_1 = var_with_sub("PMT", "1")
            A_1 = var_with_sub("A", "1")
            SD_1 = var_with_sub("SD", "1")

            steps.append(tr("App", "Exemplo - Período 1:") + "\n\n")

            steps.append("  SAC:\n")
            a1, a2, a3 = format_fraction(format_currency(p), format_currency(n,0), prefix="    A = ")
            steps.append(a1 + "\n")
            steps.append(a2 + "\n")
            steps.append(a3 + f" = R$ {format_currency(amort_const)}\n")
            steps.append(f"    {J_1} = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(sac_juros1)}\n")
            steps.append(f"    {PMT_1} = {format_currency(amort_const)} + {format_currency(sac_juros1)} = R$ {format_currency(sac_prest1)}\n")
            steps.append(f"    {SD_1} = R$ {format_currency(sac_saldo1)}\n\n")

            steps.append("  PRICE:\n")
            f1, f2, f3 = format_fraction(format_currency(num,6), format_currency(den,6), prefix=f"    {tr('App', 'Fator')} = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + f" = {format_currency(factor,6)}\n")
            steps.append(f"    PMT = {format_currency(p)} × {format_currency(factor,6)} = R$ {format_currency(price_prest)}\n")
            steps.append(f"    {J_1} = {format_currency(p)} × {format_currency(i,6)} = R$ {format_currency(price_juros1)}\n")
            steps.append(f"    {A_1} = {format_currency(price_prest)} - {format_currency(price_juros1)} = R$ {format_currency(price_amort1)}\n")
            steps.append(f"    {SD_1} = R$ {format_currency(price_saldo1)}\n\n")

            steps.append(f"  SAM ({tr('App', 'Médias')}):\n")
            steps.append(f"    {PMT_1} = ({format_currency(sac_prest1)} + {format_currency(price_prest)}) / 2 = R$ {format_currency(sam_prest1)}\n")
            steps.append(f"    {J_1}   = ({format_currency(sac_juros1)} + {format_currency(price_juros1)}) / 2 = R$ {format_currency(sam_juros1)}\n")
            steps.append(f"    {A_1}   = ({format_currency(amort_const)} + {format_currency(price_amort1)}) / 2 = R$ {format_currency(sam_amort1)}\n")
            steps.append(f"    {SD_1}  = ({format_currency(sac_saldo1)} + {format_currency(price_saldo1)}) / 2 = R$ {format_currency(sam_saldo1)}\n\n")

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

            J_n = var_with_sub("J", "n")
            A_n = var_with_sub("A", "n")
            PMT_n = var_with_sub("PMT", "n")
            SD_n = var_with_sub("SD", "n")

            steps.append(tr("App", "Fórmulas:") + "\n")
            steps.append(f"  {tr('App', 'Para k < n:')}\n")
            steps.append(f"    {J_k} = P × i\n")
            steps.append(f"    {A_k} = 0\n")
            steps.append(f"    {PMT_k} = {J_k}\n")
            steps.append(f"    {SD_k} = P\n\n")
            steps.append(f"  {tr('App', 'Para k = n:')}\n")
            steps.append(f"    {J_n} = P × i\n")
            steps.append(f"    {A_n} = P\n")
            steps.append(f"    {PMT_n} = {J_n} + {A_n} = P × (1 + i)\n")
            steps.append(f"    {SD_n} = 0\n\n")

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
                SD_6 = var_with_sub("SD", "6")
                steps.append(tr("App", "Exemplo - Saldo Devedor após Período 6:") + "\n")
                steps.append(f"  {tr('App', 'Como k=6 < n=')}{n}, {tr('App', 'o saldo devedor permanece inalterado')}\n")
                steps.append(f"  {SD_6} = P = R$ {format_currency(p)}\n\n")

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

            SD_carencia = var_with_sub("SD", str(carencia))

            # Cálculo do saldo ao final da carência
            if capitalizar:
                pow_carencia = (1 + i) ** carencia
                saldo_pos_carencia = p * pow_carencia

                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "FASE 1: PERÍODO DE CARÊNCIA (JUROS CAPITALIZADOS)") + "\n")
                steps.append("─" * 60 + "\n\n")

                car_super = to_superscript(int(carencia))
                steps.append(tr("App", "Saldo ao final da carência:") + "\n")
                steps.append(f"  {SD_carencia} = P × (1 + i){car_super}\n")
                steps.append(f"  {SD_carencia} = {format_currency(p)} × (1 + {format_currency(i,6)}){car_super}\n")
                steps.append(f"  {SD_carencia} = {format_currency(p)} × {format_currency(pow_carencia,6)}\n")
                steps.append(f"  {SD_carencia} = R$ {format_currency(saldo_pos_carencia)}\n\n")

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

                J_6 = var_with_sub("J", str(periodo_6))
                PMT_6 = var_with_sub("PMT", str(periodo_6))

                steps.append(f"{tr('App', 'Exemplo - Período')} {periodo_6} ({tr('App', 'primeiro da amortização')}):\n")
                steps.append(f"  {SD_carencia} = R$ {format_currency(saldo_pos_carencia)}\n")
                steps.append(f"  {J_6} = {SD_carencia} × i = {format_currency(saldo_pos_carencia)} × {format_currency(i,6)}\n")
                steps.append(f"  {J_6} = R$ {format_currency(juros_6)}\n")
                steps.append(f"  {PMT_6} = A + {J_6} = {format_currency(amort_const)} + {format_currency(juros_6)}\n")
                steps.append(f"  {PMT_6} = R$ {format_currency(prest_6)}\n\n")

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
