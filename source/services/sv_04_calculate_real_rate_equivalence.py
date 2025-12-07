from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
from source.utils.TextFormat import to_unicode_subscripts, to_superscript, format_currency, format_fraction, to_subscript

logger = LogManager.get_logger()

def calculate_rate_equivalence(self):
    try:
        tr = QCoreApplication.translate
        i = self.get_float_from_line_edit(self.rate_equiv_i, is_percentage=True)
        n1 = self.get_float_from_line_edit(self.rate_equiv_current_n)
        n2 = self.get_float_from_line_edit(self.rate_equiv_target_n)

        # (1+i_eq) = (1+i)^(n2/n1)
        exponent = n2 / n1
        i_eq = (1 + i) ** exponent - 1

        # Representações com subíndices/superscritos para exibição
        txt1 = to_subscript("1")
        txt2 = to_subscript("2")
        n1_txt = to_unicode_subscripts("n_1")
        n2_txt = to_unicode_subscripts("n_2")

        steps = []
        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "EQUIVALÊNCIA DE TAXAS EFETIVAS") + "\n")
        steps.append("═" * 60 + "\n\n")

        steps.append(tr("App", "Fórmula:") + "\n")
        # Criar expoente com fração vertical
        exp_super = to_superscript(f"({n2_txt}/{n1_txt})")
        steps.append(f"  (1 + i_eq) = (1 + i){exp_super}\n\n")

        steps.append(tr("App", "Dados do problema:") + "\n")
        steps.append(f"  i ({tr('App', 'Taxa conhecida')}) = {format_currency(i*100)}% {tr('App', 'ao período')} (n_1)\n")
        steps.append(f"  n_1 ({tr('App', 'Período atual')}) = {format_currency(n1, 0)}\n")
        steps.append(f"  n_2 ({tr('App', 'Período desejado')}) = {format_currency(n2, 0)}\n\n")

        # steps.append(tr("App", "Dados do problema:") + "\n")
        # steps.append(f"  i ({tr('App', 'Taxa conhecida')}) = {format_currency(i*100)}% {tr('App', 'ao período')} (n{txt1})\n")
        # steps.append(f"  n{txt1} ({tr('App', 'Período atual')}) = {format_currency(n1, 0)}\n")
        # steps.append(f"  n{txt2} ({tr('App', 'Período desejado')}) = {format_currency(n2, 0)}\n\n")

        steps.append(tr("App", "Desenvolvimento:") + "\n")
        n1e, n2e, n3e = format_fraction(format_currency(n2, 0), format_currency(n1, 0), prefix=f"  {tr('App', 'Expoente')}: ")
        steps.append(n1e + "\n")
        steps.append(n2e + "\n")
        steps.append(n3e + "\n")
        steps.append(f"  {tr('App', 'Expoente')} = {format_currency(exponent)}\n\n")

        exp_value_super = to_superscript(format_currency(exponent))
        steps.append(f"  (1 + i_eq) = (1 + {format_currency(i)}){exp_value_super}\n\n")

        pow_val = (1 + i) ** exponent
        steps.append(tr("App", "Cálculo do fator:") + "\n")
        exp_frac_values = to_superscript(f"({format_currency(n2, 0)}/{format_currency(n1, 0)})")
        steps.append(f"  (1 + i){exp_frac_values} = (1 + {format_currency(i)}){exp_value_super}\n")
        steps.append(f"  (1 + i){exp_frac_values} = {format_currency(pow_val)}\n\n")

        steps.append(tr("App", "Cálculo final:") + "\n")
        steps.append(f"  i_eq = {format_currency(pow_val)} - 1\n")
        steps.append(f"  i_eq = {format_currency(i_eq)}\n")
        steps.append(f"  i_eq = {format_currency(i_eq*100)}%\n\n")

        steps.append("─" * 60 + "\n")
        steps.append(tr("App", "RESPOSTA: A taxa equivalente é") + f" {format_currency(i_eq*100)}% {tr('App', 'ao período')} (n_2)\n")
        steps.append("─" * 60 + "\n")

        # steps.append("─" * 60 + "\n")
        # steps.append(tr("App", "RESPOSTA: A taxa equivalente é") + f" {format_currency(i_eq*100)}% {tr('App', 'ao período')} (n{txt2})\n")
        # steps.append("─" * 60 + "\n")

        self.rate_equiv_result.append("".join(steps))

    except Exception as e:
        logger.error(f"Erro ao calcular equivalência de taxas: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.rate_equiv_result.append(f"{tr('App', 'Erro')}: {e}")
        except Exception:
            pass

def calculate_real_rate(self):
    try:
        tr = QCoreApplication.translate

        calc_apparent = self.rate_real_calc_type.currentIndex() == 0  # 0 = Calcular Taxa Aparente (i), 1 = Calcular Taxa Real (r)

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
        logger.error(f"Erro ao calcular taxa aparente/real: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.rate_real_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
