from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_effective_rate(self):
    try:
        tr = QCoreApplication.translate

        # Corrigido: usar índice ao invés de comparação de texto
        calc_mode = self.eff_rate_calc_mode.currentIndex()  # 0 = Taxa Efetiva, 1 = TIR, 2 = Taxa Global

        result_text = ""

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
                '.': '·', '-': '⁻', '/': '⸍'
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

        # Função auxiliar para formatar frações
        def format_fraction(numer_str, denom_str, prefix=""):
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

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
            steps.append(f"  T ({tr('App', 'Taxa Nominal')})           = {format_currency(nominal_rate*100, 2)}%\n")
            steps.append(f"  Período da Taxa Nominal              = {format_currency(period_nominal, 0)}\n")
            steps.append(f"  Período de Capitalização            = {format_currency(period_capitalization, 0)}\n")
            steps.append(f"  Período Desejado                    = {format_currency(period_target, 0)}\n\n")

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
            steps.append(f"  r ({tr('App', 'Taxa real mensal')})     = {format_currency(real_rate*100, 2)}% ao mês\n")
            steps.append(f"  θ₁ ({tr('App', 'Inflação mês 1')})      = {format_currency(inflation_m1*100, 2)}%\n")
            steps.append(f"  θ₂ ({tr('App', 'Inflação mês 2')})      = {format_currency(inflation_m2*100, 2)}%\n")
            steps.append(f"  θ₃ ({tr('App', 'Inflação mês 3')})      = {format_currency(inflation_m3*100, 2)}%\n\n")

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
