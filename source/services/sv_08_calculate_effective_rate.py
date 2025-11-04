from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager
from utils.TextFormat import to_subscript, to_superscript, format_currency, format_fraction

logger = LogManager.get_logger()

def calculate_effective_rate(self):
    try:
        tr = QCoreApplication.translate

        # Índices: 0=Taxa Efetiva, 1=TIR, 2=Taxa Global, 3=Cobrança Antecipada, 4=TIR Modificada, 5=TMA vs Rentabilidade, 6=Juros Reais
        calc_mode = self.eff_rate_calc_mode.currentIndex()

        result_text = ""

        # Taxa Efetiva Anual
        if calc_mode == 0:
            nominal_rate = self.get_float_from_line_edit(self.eff_rate_nominal, is_percentage=True)
            period_nominal = self.get_float_from_line_edit(self.eff_rate_period_nominal)
            period_capitalization = self.get_float_from_line_edit(self.eff_rate_period_cap)
            period_target = self.get_float_from_line_edit(self.eff_rate_period_target)

            # Passo 1: Calcular taxa efetiva do período de capitalização
            m = period_nominal / period_capitalization
            i_cap = nominal_rate / m

            # Passo 2: Converter para período alvo
            ratio = period_target / period_capitalization
            i_target = (1 + i_cap) ** ratio - 1

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "CÁLCULO DE TAXA EFETIVA") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  T ({tr('App', 'Taxa Nominal')}) = {format_currency(nominal_rate*100, 2)}%\n")
            steps.append(f"  Período da Taxa Nominal = {format_currency(period_nominal, 0)}\n")
            steps.append(f"  Período de Capitalização = {format_currency(period_capitalization, 0)}\n")
            steps.append(f"  Período Desejado = {format_currency(period_target, 0)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(f"1. {tr('App', 'CÁLCULO DA TAXA EFETIVA DO PERÍODO DE CAPITALIZAÇÃO')}\n")
            steps.append("─" * 60 + "\n\n")

            steps.append(f"  M ({tr('App', 'Número de períodos de capitalização')})\n")
            c1, c2, c3 = format_fraction(format_currency(period_nominal, 0), format_currency(period_capitalization, 0), prefix="  M = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n")
            steps.append(f"  M = {format_currency(m, 0)}\n\n")

            steps.append(f"  i ({tr('App', 'Taxa efetiva por período de capitalização')})\n")
            c1, c2, c3 = format_fraction("T", "M", prefix="  i = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n")
            steps.append(f"  i = {format_currency(nominal_rate*100, 2)}% / {format_currency(m, 0)}\n")
            steps.append(f"  i = {format_currency(i_cap*100, 2)}% {tr('App', 'por período de capitalização')}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(f"2. {tr('App', 'CONVERSÃO PARA O PERÍODO DESEJADO')}\n")
            steps.append("─" * 60 + "\n\n")

            steps.append(f"  {tr('App', 'Razão de períodos')}\n")
            c1, c2, c3 = format_fraction(format_currency(period_target, 0), format_currency(period_capitalization, 0), prefix="  m = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n")
            steps.append(f"  m = {format_currency(ratio, 2)}\n\n")

            ratio_super = to_superscript(format_currency(ratio, 2))
            steps.append(f"  1 + i{to_subscript('alvo')} = (1 + i{to_subscript('cap')}){to_superscript(format_currency(ratio, 2))}\n")
            steps.append(f"  1 + i{to_subscript('alvo')} = (1 + {format_currency(i_cap, 6)}){to_superscript(format_currency(ratio, 2))}\n")
            pow_val = (1 + i_cap) ** ratio
            steps.append(f"  1 + i{to_subscript('alvo')} = {format_currency(pow_val, 6)}\n")
            steps.append(f"  i{to_subscript('alvo')} = {format_currency(i_target, 6)}\n")
            steps.append(f"  i{to_subscript('alvo')} = {format_currency(i_target*100, 2)}%\n\n")

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA:") + "\n")
            steps.append(f"  {tr('App', 'Taxa Efetiva do Período Desejado')} = {format_currency(i_target*100, 4)}%\n")
            steps.append("═" * 60 + "\n")

            result_text = "".join(steps)

        # Taxa Interna de Retorno (TIR)
        elif calc_mode == 1:
            initial_investment = self.get_float_from_line_edit(self.tir_initial)
            num_periods = int(self.get_float_from_line_edit(self.tir_periods))
            periodic_return = self.get_float_from_line_edit(self.tir_return)

            # Resolver: -P + A/(1+TIR) + A/(1+TIR)^2 + ... = 0
            # Para o caso específico com 2 períodos:
            # 0 = -P + A(1 + 1/(1+TIR)) / (1+TIR)
            # Ou resolvendo: x^2 + x - 1 = 0, onde x = 1/(1+TIR)

            if num_periods == 2 and abs(periodic_return - initial_investment) < 0.01:
                # Caso especial: raiz da equação x^2 + x - 1 = 0
                import math
                discriminant = 1 + 4
                x = (-1 + math.sqrt(discriminant)) / 2
                tir = (1 / x) - 1

            else:
                # Método de Newton-Raphson para casos gerais
                tir = self._calculate_tir_newton(initial_investment, periodic_return, num_periods)

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "CÁLCULO DA TAXA INTERNA DE RETORNO (TIR)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fluxo de Caixa:") + "\n")
            steps.append(f"  t₀ = -{format_currency(initial_investment, 2)} (Desembolso)\n")
            for t in range(1, int(num_periods) + 1):
                steps.append(f"  t{to_subscript(t)} = +{format_currency(periodic_return, 2)}\n")

            steps.append("\n")

            steps.append(tr("App", "Equação de VPL = 0:") + "\n")
            vpl_formula = f"0 = -{format_currency(initial_investment, 2)}"
            for t in range(1, int(num_periods) + 1):
                vpl_formula += f" + {format_currency(periodic_return, 2)}/(1+TIR){to_superscript(t)}"

            steps.append(f"  {vpl_formula}\n\n")

            if num_periods == 2:
                steps.append(tr("App", "Dividindo por") + f" {format_currency(initial_investment, 2)}:\n")
                steps.append(f"  0 = -1 + 1/(1+TIR) + 1/(1+TIR)²\n\n")

                steps.append(tr("App", "Substituindo x = 1/(1+TIR):") + "\n")
                steps.append(f"  0 = -1 + x + x²\n")
                steps.append(f"  x² + x - 1 = 0\n\n")

                steps.append(tr("App", "Usando Fórmula de Bhaskara:") + "\n")
                steps.append(f"  x = (-1 ± √(1 + 4)) / 2\n")
                steps.append(f"  x = (-1 ± √5) / 2\n")
                import math
                sqrt5 = math.sqrt(5)
                steps.append(f"  x = (-1 ± {format_currency(sqrt5, 6)}) / 2\n\n")

                steps.append(tr("App", "Usando a raiz positiva:") + "\n")
                x = (-1 + sqrt5) / 2
                steps.append(f"  x = (-1 + {format_currency(sqrt5, 6)}) / 2\n")
                steps.append(f"  x = {format_currency(x, 6)}\n\n")

                steps.append(tr("App", "Revertendo a substituição:") + "\n")
                steps.append(f"  {format_currency(x, 6)} = 1 / (1 + TIR)\n")
                steps.append(f"  1 + TIR = {format_currency(1/x, 6)}\n")
                steps.append(f"  TIR = {format_currency(tir, 6)}\n")
                steps.append(f"  TIR = {format_currency(tir*100, 4)}%\n\n")

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA:") + "\n")
            steps.append(f"  {tr('App', 'Taxa Interna de Retorno')} = {format_currency(tir*100, 4)}%\n")
            steps.append("═" * 60 + "\n")

            result_text = "".join(steps)

        # Taxa Global de Juros (com inflação acumulada)
        elif calc_mode == 2:
            real_rate = self.get_float_from_line_edit(self.tax_global_real, is_percentage=True)
            inflation_m1 = self.get_float_from_line_edit(self.tax_global_inf_m1, is_percentage=True)
            inflation_m2 = self.get_float_from_line_edit(self.tax_global_inf_m2, is_percentage=True)
            inflation_m3 = self.get_float_from_line_edit(self.tax_global_inf_m3, is_percentage=True)

            # Passo 1: Taxa real do trimestre
            r_trim = (1 + real_rate) ** 3 - 1

            # Passo 2: Inflação acumulada do trimestre
            theta_trim = (1 + inflation_m1) * (1 + inflation_m2) * (1 + inflation_m3) - 1

            # Passo 3: Taxa global (aparente) do trimestre
            i_global = (1 + theta_trim) * (1 + r_trim) - 1

            steps = []
            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "CÁLCULO DA TAXA GLOBAL DE JUROS (APARENTE)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  r ({tr('App', 'Taxa real mensal')}) = {format_currency(real_rate*100, 2)}% ao mês\n")
            steps.append(f"  θ₁ ({tr('App', 'Inflação mês 1')}) = {format_currency(inflation_m1*100, 2)}%\n")
            steps.append(f"  θ₂ ({tr('App', 'Inflação mês 2')}) = {format_currency(inflation_m2*100, 2)}%\n")
            steps.append(f"  θ₃ ({tr('App', 'Inflação mês 3')}) = {format_currency(inflation_m3*100, 2)}%\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(f"1. {tr('App', 'TAXA REAL DO TRIMESTRE')}\n")
            steps.append("─" * 60 + "\n\n")

            steps.append(f"  1 + r{to_subscript('trim')} = (1 + r{to_subscript('mês')}){to_superscript(3)}\n")
            steps.append(f"  1 + r{to_subscript('trim')} = (1 + {format_currency(real_rate, 6)}){to_superscript(3)}\n")
            pow_r = (1 + real_rate) ** 3
            steps.append(f"  1 + r{to_subscript('trim')} = {format_currency(pow_r, 6)}\n")
            steps.append(f"  r{to_subscript('trim')} = {format_currency(r_trim, 6)}\n")
            steps.append(f"  r{to_subscript('trim')} = {format_currency(r_trim*100, 4)}%\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(f"2. {tr('App', 'INFLAÇÃO ACUMULADA DO TRIMESTRE')}\n")
            steps.append("─" * 60 + "\n\n")

            steps.append(f"  1 + θ{to_subscript('trim')} = (1 + θ₁) × (1 + θ₂) × (1 + θ₃)\n")
            steps.append(f"  1 + θ{to_subscript('trim')} = (1 + {format_currency(inflation_m1, 6)}) × (1 + {format_currency(inflation_m2, 6)}) × (1 + {format_currency(inflation_m3, 6)})\n")
            steps.append(f"  1 + θ{to_subscript('trim')} = {format_currency(1+inflation_m1, 6)} × {format_currency(1+inflation_m2, 6)} × {format_currency(1+inflation_m3, 6)}\n")

            mult_1_2 = (1 + inflation_m1) * (1 + inflation_m2)
            steps.append(f"  1 + θ{to_subscript('trim')} = {format_currency(mult_1_2, 6)} × {format_currency(1+inflation_m3, 6)}\n")

            pow_theta = (1 + inflation_m1) * (1 + inflation_m2) * (1 + inflation_m3)
            steps.append(f"  1 + θ{to_subscript('trim')} = {format_currency(pow_theta, 6)}\n")
            steps.append(f"  θ{to_subscript('trim')} = {format_currency(theta_trim, 6)}\n")
            steps.append(f"  θ{to_subscript('trim')} = {format_currency(theta_trim*100, 4)}%\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(f"3. {tr('App', 'TAXA GLOBAL (APARENTE) DO TRIMESTRE')}\n")
            steps.append("─" * 60 + "\n\n")

            steps.append(f"  1 + i{to_subscript('global')} = (1 + θ{to_subscript('trim')}) × (1 + r{to_subscript('trim')})\n")
            steps.append(f"  1 + i{to_subscript('global')} = (1 + {format_currency(theta_trim, 6)}) × (1 + {format_currency(r_trim, 6)})\n")
            steps.append(f"  1 + i{to_subscript('global')} = {format_currency(pow_theta, 6)} × {format_currency(pow_r, 6)}\n")
            pow_i = pow_theta * pow_r
            steps.append(f"  1 + i{to_subscript('global')} = {format_currency(pow_i, 6)}\n")
            steps.append(f"  i{to_subscript('global')} = {format_currency(i_global, 6)}\n")
            steps.append(f"  i{to_subscript('global')} = {format_currency(i_global*100, 4)}%\n\n")

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA:") + "\n")
            steps.append(f"  {tr('App', 'Taxa Global de Juros do Trimestre')} = {format_currency(i_global*100, 4)}%\n")
            steps.append("═" * 60 + "\n")

            result_text = "".join(steps)

        # Taxa Efetiva em Cobrança Antecipada (Sistema Alemão)
        elif calc_mode == 3:
            nominal_value = self.get_float_from_line_edit(self.adv_int_nominal)
            advance_rate = self.get_float_from_line_edit(self.adv_int_rate, is_percentage=True)

            # Cálculo dos valores
            advance_interest = nominal_value * advance_rate
            received_value = nominal_value - advance_interest

            steps = []
            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "CÁLCULO DE TAXA EFETIVA EM COBRANÇA ANTECIPADA") + "\n")
            steps.append(tr("App", "(SISTEMA ALEMÃO)") + "\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  F ({tr('App', 'Valor Nominal do Empréstimo')}) = R$ {format_currency(nominal_value, 2)}\n")
            steps.append(f"  i{to_subscript('a')} ({tr('App', 'Taxa de Cobrança Antecipada')}) = {format_currency(advance_rate*100, 2)}% a.a.\n")
            steps.append(f"  n ({tr('App', 'Período')}) = {tr('App', '1 ano')}\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"1. {tr('App', 'CÁLCULO DOS JUROS ANTECIPADOS')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(f"  J{to_subscript('ant')} = F × i{to_subscript('a')}\n")
            steps.append(f"  J{to_subscript('ant')} = R$ {format_currency(nominal_value, 2)} × {format_currency(advance_rate, 6)}\n")
            steps.append(f"  J{to_subscript('ant')} = R$ {format_currency(advance_interest, 2)}\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"2. {tr('App', 'CÁLCULO DO VALOR RECEBIDO (PRINCIPAL LÍQUIDO)')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(f"  P ({tr('App', 'Valor Recebido')}) = F - J{to_subscript('ant')}\n")
            steps.append(f"  P = R$ {format_currency(nominal_value, 2)} - R$ {format_currency(advance_interest, 2)}\n")
            steps.append(f"  P = R$ {format_currency(received_value, 2)}\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(f"{tr('App', 'MÉTODO 1: LÓGICA FINANCEIRA')}\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(tr("App", "Interpretação:") + "\n")
            steps.append(f"  • {tr('App', 'O tomador recebeu')} P = R$ {format_currency(received_value, 2)}\n")
            steps.append(f"  • {tr('App', 'Ao final de 1 ano, pagou')} F = R$ {format_currency(nominal_value, 2)}\n")
            steps.append(f"  • {tr('App', 'Juros efetivamente pagos')} J = R$ {format_currency(advance_interest, 2)}\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"3. {tr('App', 'CÁLCULO DA TAXA EFETIVA PELO MÉTODO 1')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "A taxa efetiva é calculada pela relação:") + "\n\n")

            c1, c2, c3 = format_fraction("J", "P", prefix="  i = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            c1, c2, c3 = format_fraction(f"R$ {format_currency(advance_interest, 2)}", f"R$ {format_currency(received_value, 2)}", prefix="  i = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            effective_rate_m1 = advance_interest / received_value
            steps.append(f"  i = {format_currency(effective_rate_m1, 6)}\n")
            steps.append(f"  i = {format_currency(effective_rate_m1*100, 4)}%\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(f"{tr('App', 'MÉTODO 2: USO DA FÓRMULA DE CONVERSÃO')}\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(tr("App", "Fórmula para converter taxa antecipada em taxa efetiva:") + "\n\n")

            c1, c2, c3 = format_fraction(f"i{to_subscript('a')}", f"1 - i{to_subscript('a')}", prefix="  i = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            steps.append(tr("App", "Onde:") + "\n")
            steps.append(f"  i{to_subscript('a')} = {tr('App', 'Taxa de cobrança antecipada')} = {format_currency(advance_rate*100, 2)}% = {format_currency(advance_rate, 6)}\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"4. {tr('App', 'APLICAÇÃO DA FÓRMULA')}\n")
            steps.append("─" * 70 + "\n\n")

            c1, c2, c3 = format_fraction(f"{format_currency(advance_rate, 6)}", f"1 - {format_currency(advance_rate, 6)}", prefix="  i = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            denominator = 1 - advance_rate
            c1, c2, c3 = format_fraction(f"{format_currency(advance_rate, 6)}", 
                                        f"{format_currency(denominator, 6)}", 
                                        prefix="  i = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            effective_rate_m2 = advance_rate / denominator
            steps.append(f"  i = {format_currency(effective_rate_m2, 6)}\n")
            steps.append(f"  i = {format_currency(effective_rate_m2*100, 4)}%\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(f"{tr('App', 'VERIFICAÇÃO DOS RESULTADOS')}\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(f"  {tr('App', 'Método 1 (Lógica Financeira)')}: i = {format_currency(effective_rate_m1*100, 4)}%\n")
            steps.append(f"  {tr('App', 'Método 2 (Fórmula de Conversão)')}: i = {format_currency(effective_rate_m2*100, 4)}%\n\n")

            diff_percent = abs(effective_rate_m1 - effective_rate_m2) * 100
            if diff_percent < 0.0001:
                steps.append(f"  ✓ {tr('App', 'Os resultados são idênticos (diferença < 0,0001%)')}\n\n")

            else:
                steps.append(f"  {tr('App', 'Diferença entre métodos')}: {format_currency(diff_percent, 6)}%\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESUMO:") + "\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(f"  {tr('App', 'Valor Nominal do Empréstimo (F)')}: R$ {format_currency(nominal_value, 2)}\n")
            steps.append(f"  {tr('App', 'Taxa de Cobrança Antecipada')} (i{to_subscript('a')}): {format_currency(advance_rate*100, 2)}%\n")
            steps.append(f"  {tr('App', 'Juros Pagos Antecipadamente')} (J{to_subscript('ant')}): R$ {format_currency(advance_interest, 2)}\n")
            steps.append(f"  {tr('App', 'Valor Recebido (P)')}: R$ {format_currency(received_value, 2)}\n")
            steps.append(f"  {tr('App', 'Taxa Efetiva Anual (i)')}: {format_currency(effective_rate_m1*100, 4)}%\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESPOSTA FINAL:") + "\n")
            steps.append(f"  {tr('App', 'A taxa efetiva anual que produz os mesmos juros é de')}\n")
            steps.append(f"  {format_currency(effective_rate_m1*100, 4)}% {tr('App', 'ao ano')}\n")
            steps.append("═" * 70 + "\n")

            result_text = "".join(steps)

        # TIR Modificada (TIRm)
        elif calc_mode == 4:
            import math

            initial_investment = self.get_float_from_line_edit(self.tirm_initial)
            num_periods = int(self.get_float_from_line_edit(self.tirm_periods))
            periodic_return = self.get_float_from_line_edit(self.tirm_return)
            capitalization_rate = self.get_float_from_line_edit(self.tirm_cap_rate, is_percentage=True)

            steps = []
            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "CÁLCULO DA TAXA INTERNA DE RETORNO MODIFICADA (TIRm)") + "\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  VPC ({tr('App', 'Valor Presente dos Custos')}) = R$ {format_currency(initial_investment, 2)}\n")
            steps.append(f"  n ({tr('App', 'Número de períodos')}) = {num_periods}\n")
            steps.append(f"  Retorno por período = R$ {format_currency(periodic_return, 2)}\n")
            steps.append(f"  Taxa de capitalização = {format_currency(capitalization_rate*100, 2)}% ao período\n\n")

            # Cálculo do VFB (Valor Futuro dos Benefícios)
            steps.append("─" * 70 + "\n")
            steps.append(f"1. {tr('App', 'CÁLCULO DO VALOR FUTURO DOS BENEFÍCIOS (VFB)')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            steps.append(f"  VFB = Σ B{to_subscript('k')} × (1 + i){to_superscript('n-k')}\n\n")

            steps.append(tr("App", "Onde:") + "\n")
            steps.append(f"  B{to_subscript('k')} = {tr('App', 'Benefício no período k')}\n")
            steps.append(f"  i = {tr('App', 'Taxa de capitalização')} = {format_currency(capitalization_rate, 6)}\n")
            steps.append(f"  n = {tr('App', 'Horizonte de análise')} = {num_periods}\n\n")

            vfb = 0
            for k in range(1, num_periods + 1):
                exponent = num_periods - k
                capitalized_value = periodic_return * ((1 + capitalization_rate) ** exponent)
                vfb += capitalized_value

                steps.append(f"  Período {k}:\n")
                steps.append(f"    B{to_subscript(k)} × (1 + {format_currency(capitalization_rate, 6)}){to_superscript(exponent)}\n")
                steps.append(f"    = {format_currency(periodic_return, 2)} × {format_currency((1 + capitalization_rate) ** exponent, 6)}\n")
                steps.append(f"    = R$ {format_currency(capitalized_value, 2)}\n\n")

            steps.append(f"  VFB = ")
            for k in range(1, num_periods + 1):
                exponent = num_periods - k
                if k > 1:
                    steps.append(" + ")

                steps.append(f"{format_currency(periodic_return, 2)} × (1,{format_currency(capitalization_rate*100, 0)}){to_superscript(exponent)}")

            steps.append("\n")

            steps.append(f"  VFB = R$ {format_currency(vfb, 2)}\n\n")

            # Cálculo da TIRm
            steps.append("─" * 70 + "\n")
            steps.append(f"2. {tr('App', 'CÁLCULO DA TAXA INTERNA DE RETORNO MODIFICADA')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            c1, c2, c3 = format_fraction("VFB", "VPC", prefix=f"  TIRm = {to_superscript('n')}√")
            steps.append(c1 + " - 1\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            c1, c2, c3 = format_fraction(f"R$ {format_currency(vfb, 2)}", f"R$ {format_currency(initial_investment, 2)}", prefix=f"  TIRm = {to_superscript(num_periods)}√")
            steps.append(c1 + " - 1\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            ratio = vfb / initial_investment
            steps.append(f"  TIRm = {to_superscript(num_periods)}√{format_currency(ratio, 6)} - 1\n")

            tirm = ratio ** (1/num_periods) - 1
            root_value = ratio ** (1/num_periods)
            steps.append(f"  TIRm = {format_currency(root_value, 6)} - 1\n")
            steps.append(f"  TIRm = {format_currency(tirm, 6)}\n")
            steps.append(f"  TIRm = {format_currency(tirm*100, 4)}%\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESUMO:") + "\n")
            steps.append("═" * 70 + "\n\n")
            steps.append(f"  {tr('App', 'Valor Presente dos Custos (VPC)')}: R$ {format_currency(initial_investment, 2)}\n")
            steps.append(f"  {tr('App', 'Valor Futuro dos Benefícios (VFB)')}: R$ {format_currency(vfb, 2)}\n")
            steps.append(f"  {tr('App', 'Número de períodos (n)')}: {num_periods}\n")
            steps.append(f"  {tr('App', 'Taxa de capitalização')}: {format_currency(capitalization_rate*100, 2)}%\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESPOSTA FINAL:") + "\n")
            steps.append(f"  {tr('App', 'A Taxa Interna de Retorno Modificada é de')}\n")
            steps.append(f"  {format_currency(tirm*100, 4)}% {tr('App', 'ao mês')}\n")
            steps.append("═" * 70 + "\n")

            result_text = "".join(steps)

        # TMA vs Rentabilidade
        elif calc_mode == 5:
            import math

            capital = self.get_float_from_line_edit(self.tma_capital)
            monthly_rate = self.get_float_from_line_edit(self.tma_monthly_rate, is_percentage=True)
            tma_annual = self.get_float_from_line_edit(self.tma_rate, is_percentage=True)
            periods = int(self.get_float_from_line_edit(self.tma_periods))

            steps = []
            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "ANÁLISE DE INVESTIMENTO: TMA vs RENTABILIDADE") + "\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Capital Aplicado')}) = R$ {format_currency(capital, 2)}\n")
            steps.append(f"  i{to_subscript('mensal')} ({tr('App', 'Taxa da Oportunidade')}) = {format_currency(monthly_rate*100, 2)}% ao mês\n")
            steps.append(f"  TMA ({tr('App', 'Taxa Mínima de Atratividade')}) = {format_currency(tma_annual*100, 2)}% ao ano\n")
            steps.append(f"  n ({tr('App', 'Prazo')}) = {periods} meses\n\n")

            # Passo 1: Rendimento da Oportunidade
            steps.append("─" * 70 + "\n")
            steps.append(f"1. {tr('App', 'CÁLCULO DO RENDIMENTO DA OPORTUNIDADE')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "Primeiro, calculamos a taxa efetiva anual equivalente:") + "\n\n")
            steps.append(f"  i{to_subscript('anual')} = (1 + i{to_subscript('mensal')}){to_superscript('12')} - 1\n")
            steps.append(f"  i{to_subscript('anual')} = (1 + {format_currency(monthly_rate, 6)}){to_superscript('12')} - 1\n")
            steps.append(f"  i{to_subscript('anual')} = ({format_currency(1 + monthly_rate, 6)}){to_superscript('12')} - 1\n")

            annual_rate = (1 + monthly_rate) ** 12 - 1
            steps.append(f"  i{to_subscript('anual')} = {format_currency(1 + annual_rate, 6)} - 1\n")
            steps.append(f"  i{to_subscript('anual')} = {format_currency(annual_rate, 6)}\n")
            steps.append(f"  i{to_subscript('anual')} = {format_currency(annual_rate*100, 4)}% a.a.\n\n")

            steps.append(tr("App", "Rendimento da oportunidade:") + "\n\n")
            rendimento_real = capital * annual_rate
            steps.append(f"  Rendimento = P × i{to_subscript('anual')}\n")
            steps.append(f"  Rendimento = R$ {format_currency(capital, 2)} × {format_currency(annual_rate, 6)}\n")
            steps.append(f"  Rendimento = R$ {format_currency(rendimento_real, 2)}\n\n")

            # Passo 2: Rendimento Mínimo Aceitável
            steps.append("─" * 70 + "\n")
            steps.append(f"2. {tr('App', 'CÁLCULO DO RENDIMENTO MÍNIMO ACEITÁVEL (TMA)')}\n")
            steps.append("─" * 70 + "\n\n")

            rendimento_tma = capital * tma_annual
            steps.append(f"  Rendimento{to_subscript('TMA')} = P × TMA\n")
            steps.append(f"  Rendimento{to_subscript('TMA')} = R$ {format_currency(capital, 2)} × {format_currency(tma_annual, 6)}\n")
            steps.append(f"  Rendimento{to_subscript('TMA')} = R$ {format_currency(rendimento_tma, 2)}\n\n")

            # Passo 3: Diferença
            steps.append("─" * 70 + "\n")
            steps.append(f"3. {tr('App', 'CÁLCULO DA DIFERENÇA')}\n")
            steps.append("─" * 70 + "\n\n")

            diferenca = rendimento_real - rendimento_tma
            steps.append(f"  Diferença = Rendimento{to_subscript('Real')} - Rendimento{to_subscript('TMA')}\n")
            steps.append(f"  Diferença = R$ {format_currency(rendimento_real, 2)} - R$ {format_currency(rendimento_tma, 2)}\n")
            steps.append(f"  Diferença = R$ {format_currency(diferenca, 2)}\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESUMO:") + "\n")
            steps.append("═" * 70 + "\n\n")
            steps.append(f"  {tr('App', 'Capital Aplicado')}: R$ {format_currency(capital, 2)}\n")
            steps.append(f"  {tr('App', 'Taxa Mensal da Oportunidade')}: {format_currency(monthly_rate*100, 2)}%\n")
            steps.append(f"  {tr('App', 'Taxa Anual Equivalente')}: {format_currency(annual_rate*100, 4)}%\n")
            steps.append(f"  {tr('App', 'TMA (anual)')}: {format_currency(tma_annual*100, 2)}%\n")
            steps.append(f"  {tr('App', 'Rendimento da Oportunidade')}: R$ {format_currency(rendimento_real, 2)}\n")
            steps.append(f"  {tr('App', 'Rendimento Mínimo (TMA)')}: R$ {format_currency(rendimento_tma, 2)}\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESPOSTA FINAL:") + "\n")
            steps.append(f"  {tr('App', 'O valor da diferença é de')}\n")
            steps.append(f"  R$ {format_currency(diferenca, 2)}\n")
            steps.append("═" * 70 + "\n")

            result_text = "".join(steps)

        # Juros Reais
        elif calc_mode == 6:
            capital = self.get_float_from_line_edit(self.real_int_capital)
            global_rate = self.get_float_from_line_edit(self.real_int_global_rate, is_percentage=True)
            inflation_rate = self.get_float_from_line_edit(self.real_int_inflation, is_percentage=True)

            steps = []
            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "CÁLCULO DE JUROS REAIS (ACIMA DA INFLAÇÃO)") + "\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Capital')}) = R$ {format_currency(capital, 2)}\n")
            steps.append(f"  i ({tr('App', 'Taxa Global')}) = {format_currency(global_rate*100, 2)}% ao ano\n")
            steps.append(f"  θ ({tr('App', 'Inflação')}) = {format_currency(inflation_rate*100, 2)}% ao ano\n\n")

            # Método 1: Cálculo pela Taxa Real
            steps.append("═" * 70 + "\n")
            steps.append(f"{tr('App', 'MÉTODO 1: CÁLCULO PELA TAXA REAL')}\n")
            steps.append("═" * 70 + "\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"1. {tr('App', 'ENCONTRAR A TAXA REAL (r)')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "Fórmula de Fisher:") + "\n")
            steps.append(f"  1 + i = (1 + θ) × (1 + r)\n\n")

            steps.append(tr("App", "Isolando r:") + "\n")
            c1, c2, c3 = format_fraction("1 + i", "1 + θ", prefix="  1 + r = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            c1, c2, c3 = format_fraction(f"1 + {format_currency(global_rate, 6)}", f"1 + {format_currency(inflation_rate, 6)}", prefix="  1 + r = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            c1, c2, c3 = format_fraction(f"{format_currency(1 + global_rate, 6)}", f"{format_currency(1 + inflation_rate, 6)}", prefix="  1 + r = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            real_rate = (1 + global_rate) / (1 + inflation_rate) - 1
            steps.append(f"  1 + r = {format_currency(1 + real_rate, 6)}\n")
            steps.append(f"  r = {format_currency(real_rate, 6)}\n")
            steps.append(f"  r = {format_currency(real_rate*100, 4)}%\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"2. {tr('App', 'CALCULAR OS JUROS REAIS')}\n")
            steps.append("─" * 70 + "\n\n")

            juros_reais_m1 = capital * real_rate
            steps.append(f"  Juros Reais = P × r\n")
            steps.append(f"  Juros Reais = R$ {format_currency(capital, 2)} × {format_currency(real_rate, 6)}\n")
            steps.append(f"  Juros Reais = R$ {format_currency(juros_reais_m1, 2)}\n\n")

            # Método 2: Cálculo pelo Ganho de Poder de Compra
            steps.append("═" * 70 + "\n")
            steps.append(f"{tr('App', 'MÉTODO 2: CÁLCULO PELO GANHO DE PODER DE COMPRA')}\n")
            steps.append("═" * 70 + "\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"1. {tr('App', 'CALCULAR O MONTANTE FINAL (APARENTE)')}\n")
            steps.append("─" * 70 + "\n\n")

            montante = capital * (1 + global_rate)
            steps.append(f"  F = P × (1 + i)\n")
            steps.append(f"  F = R$ {format_currency(capital, 2)} × (1 + {format_currency(global_rate, 6)})\n")
            steps.append(f"  F = R$ {format_currency(capital, 2)} × {format_currency(1 + global_rate, 6)}\n")
            steps.append(f"  F = R$ {format_currency(montante, 2)}\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"2. {tr('App', 'CALCULAR O PODER DE COMPRA DESSE MONTANTE')}\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "(Descontando a inflação)") + "\n\n")

            valor_real = montante / (1 + inflation_rate)
            c1, c2, c3 = format_fraction("F", "1 + θ", prefix="  VP = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            c1, c2, c3 = format_fraction(f"R$ {format_currency(montante, 2)}", f"1 + {format_currency(inflation_rate, 6)}", prefix="  VP = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            c1, c2, c3 = format_fraction(f"R$ {format_currency(montante, 2)}", f"{format_currency(1 + inflation_rate, 6)}", prefix="  VP = ")
            steps.append(c1 + "\n")
            steps.append(c2 + "\n")
            steps.append(c3 + "\n\n")

            steps.append(f"  VP = R$ {format_currency(valor_real, 2)}\n\n")

            steps.append("─" * 70 + "\n")
            steps.append(f"3. {tr('App', 'CALCULAR O GANHO REAL (JUROS REAIS)')}\n")
            steps.append("─" * 70 + "\n\n")

            juros_reais_m2 = valor_real - capital
            steps.append(f"  Juros Reais = VP - P\n")
            steps.append(f"  Juros Reais = R$ {format_currency(valor_real, 2)} - R$ {format_currency(capital, 2)}\n")
            steps.append(f"  Juros Reais = R$ {format_currency(juros_reais_m2, 2)}\n\n")

            # Verificação
            steps.append("═" * 70 + "\n")
            steps.append(f"{tr('App', 'VERIFICAÇÃO DOS RESULTADOS')}\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(f"  {tr('App', 'Método 1 (Taxa Real)')}: R$ {format_currency(juros_reais_m1, 2)}\n")
            steps.append(f"  {tr('App', 'Método 2 (Poder de Compra)')}: R$ {format_currency(juros_reais_m2, 2)}\n\n")

            diff = abs(juros_reais_m1 - juros_reais_m2)
            if diff < 0.01:
                steps.append(f"  ✓ {tr('App', 'Os resultados são idênticos')}\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESUMO:") + "\n")
            steps.append("═" * 70 + "\n\n")
            steps.append(f"  {tr('App', 'Capital Aplicado')}: R$ {format_currency(capital, 2)}\n")
            steps.append(f"  {tr('App', 'Taxa Global (i)')}: {format_currency(global_rate*100, 2)}%\n")
            steps.append(f"  {tr('App', 'Inflação (θ)')}: {format_currency(inflation_rate*100, 2)}%\n")
            steps.append(f"  {tr('App', 'Taxa Real (r)')}: {format_currency(real_rate*100, 4)}%\n")
            steps.append(f"  {tr('App', 'Montante Final')}: R$ {format_currency(montante, 2)}\n")
            steps.append(f"  {tr('App', 'Poder de Compra Final')}: R$ {format_currency(valor_real, 2)}\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESPOSTA FINAL:") + "\n")
            steps.append(f"  {tr('App', 'O valor dos juros reais obtidos foi de')}\n")
            steps.append(f"  R$ {format_currency(juros_reais_m1, 2)}\n")
            steps.append("═" * 70 + "\n")

            result_text = "".join(steps)

        if result_text:
            self.eff_rate_result.append(result_text)

    except Exception as e:
        logger.error(f"Erro ao calcular taxa efetiva/TIR/global: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.eff_rate_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass

def _calculate_tir_newton(self, initial_investment, periodic_return, num_periods, initial_guess=0.1, tolerance=1e-8, max_iterations=100):
    try:
        tir = initial_guess
        for _ in range(max_iterations):
            # VPL
            vpl = -initial_investment
            for t in range(1, int(num_periods) + 1):
                vpl += periodic_return / ((1 + tir) ** t)

            # Derivada do VPL
            dvpl = 0
            for t in range(1, int(num_periods) + 1):
                dvpl -= t * periodic_return / ((1 + tir) ** (t + 1))

            # Atualização
            if abs(dvpl) < 1e-10:
                break

            tir_new = tir - vpl / dvpl

            if abs(tir_new - tir) < tolerance:
                return tir_new

            tir = tir_new

        return tir

    except Exception as e:
        logger.error(f"Erro no cálculo de TIR por Newton-Raphson: {e}", exc_info=True)
        raise
