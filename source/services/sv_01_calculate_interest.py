from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
from source.utils.TextFormat import to_superscript, format_currency, format_fraction, to_unicode_subscripts

logger = LogManager.get_logger()

def calculate_interest(self):
    try:
        tr = QCoreApplication.translate
        i = self.get_float_from_line_edit(self.interest_i, is_percentage=True)
        n = self.get_float_from_line_edit(self.interest_n)

        calc_type_index = self.interest_calc_type.currentIndex()
        is_compound = self.interest_regime.currentIndex() == 0

        result_text = ""

        # NOVA FUNCIONALIDADE: Comparar JS vs JC
        if calc_type_index == 2:  # Comparar JS vs JC
            p = self.get_float_from_line_edit(self.interest_p)
            n_base = int(n)  # Período base para cálculo de JC

            steps = []
            steps.append("═" * 70 + "\n")
            steps.append(to_unicode_subscripts(tr("App", "COMPARAÇÃO: JUROS SIMPLES vs JUROS COMPOSTOS")) + "\n")
            steps.append("═" * 70 + "\n\n")

            steps.append(tr("App", "Objetivo:") + "\n")
            steps.append(to_unicode_subscripts(tr("App", "Encontrar quantos meses (n_s) são necessários para que o montante a juros simples (F_s) supere o montante a juros compostos (F_c) calculado para {n} meses.").format(n=n_base)) + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Principal')})           = R$ {format_currency(p)}\n")
            steps.append(f"  i ({tr('App', 'Taxa')})                = {format_currency(i*100)}% {tr('App', 'ao período')}\n")
            steps.append(to_unicode_subscripts(f"  n_c ({tr('App', 'Período base JC')})   = {n_base} {tr('App', 'meses')}") + "\n\n")

            # Passo 1: Calcular F_c para n_base meses
            f_c = p * (1 + i) ** n_base
            steps.append("─" * 70 + "\n")
            steps.append(to_unicode_subscripts(tr("App", "PASSO 1: Calcular montante a juros compostos para {n} meses").format(n=n_base)) + "\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            steps.append(to_unicode_subscripts("  F_c = P × (1 + i)ⁿᶜ") + "\n\n")

            n_super = to_superscript(n_base)
            steps.append(tr("App", "Substituindo os valores:") + "\n")
            steps.append(to_unicode_subscripts(f"  F_c = {format_currency(p)} × (1 + {format_currency(i)}){n_super}") + "\n")

            fator_jc = (1 + i) ** n_base
            steps.append(to_unicode_subscripts(f"  F_c = {format_currency(p)} × {format_currency(fator_jc)}") + "\n")
            steps.append(to_unicode_subscripts(f"  F_c = R$ {format_currency(f_c)}") + "\n\n")

            # Passo 2: Estabelecer inequação e resolver
            steps.append("─" * 70 + "\n")
            steps.append(to_unicode_subscripts(tr("App", "PASSO 2: Estabelecer a inequação e resolver para n_s")) + "\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(to_unicode_subscripts(tr("App", "Queremos encontrar n_s tal que:")) + "\n")
            steps.append(to_unicode_subscripts("  F_s > F_c") + "\n\n")

            steps.append(tr("App", "Fórmula de juros simples:") + "\n")
            steps.append(to_unicode_subscripts("  F_s = P × (1 + n_s × i)") + "\n\n")

            steps.append(tr("App", "Inequação:") + "\n")
            steps.append(to_unicode_subscripts(f"  P × (1 + n_s × i) > {format_currency(f_c)}") + "\n")
            steps.append(to_unicode_subscripts(f"  {format_currency(p)} × (1 + n_s × {format_currency(i)}) > {format_currency(f_c)}") + "\n\n")

            steps.append(tr("App", "Dividindo ambos os lados por P:") + "\n")
            razao = f_c / p
            steps.append(to_unicode_subscripts(f"  1 + n_s × {format_currency(i)} > {format_currency(f_c)} / {format_currency(p)}") + "\n")
            steps.append(to_unicode_subscripts(f"  1 + n_s × {format_currency(i)} > {format_currency(razao)}") + "\n\n")

            steps.append(to_unicode_subscripts(tr("App", "Isolando n_s:")) + "\n")
            diferenca = razao - 1
            steps.append(to_unicode_subscripts(f"  n_s × {format_currency(i)} > {format_currency(razao)} - 1") + "\n")
            steps.append(to_unicode_subscripts(f"  n_s × {format_currency(i)} > {format_currency(diferenca)}") + "\n")

            n_s_real = diferenca / i
            steps.append(to_unicode_subscripts(f"  n_s > {format_currency(diferenca)} / {format_currency(i)}") + "\n")
            steps.append(to_unicode_subscripts(f"  n_s > {format_currency(n_s_real)}") + "\n\n")

            # Resposta final
            n_s_inteiro = int(n_s_real) + 1
            steps.append("─" * 70 + "\n")
            steps.append(tr("App", "RESULTADO") + "\n")
            steps.append("─" * 70 + "\n\n")

            steps.append(tr("App", "Como o número de meses deve ser inteiro, o menor valor que satisfaz a condição é {n}.").format(n=n_s_inteiro) + "\n\n")

            # Verificação
            f_s_verificacao = p * (1 + n_s_inteiro * i)
            steps.append(tr("App", "Verificação:") + "\n")
            steps.append(to_unicode_subscripts(f"  F_s({n_s_inteiro}) = {format_currency(p)} × (1 + {n_s_inteiro} × {format_currency(i)})") + "\n")
            steps.append(to_unicode_subscripts(f"  F_s({n_s_inteiro}) = {format_currency(p)} × {format_currency(1 + n_s_inteiro * i)}") + "\n")
            steps.append(to_unicode_subscripts(f"  F_s({n_s_inteiro}) = R$ {format_currency(f_s_verificacao)}") + "\n\n")

            steps.append(to_unicode_subscripts(f"  F_c({n_base}) = R$ {format_currency(f_c)}") + "\n")
            steps.append(to_unicode_subscripts(f"  F_s({n_s_inteiro}) = R$ {format_currency(f_s_verificacao)}") + "\n\n")

            if f_s_verificacao > f_c:
                steps.append(to_unicode_subscripts(f"  ✓ F_s({n_s_inteiro}) > F_c({n_base})") + "\n\n")

            steps.append("═" * 70 + "\n")
            steps.append(tr("App", "RESPOSTA: São necessários {n} meses consecutivos.").format(n=n_s_inteiro) + "\n")
            steps.append("═" * 70 + "\n")

            result_text = "".join(steps)

        elif calc_type_index == 0:  # Calcular Montante (F)
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
        logger.error(f"Erro ao calcular juros: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.interest_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
