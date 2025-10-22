from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_depreciation(self):
    try:
        tr = QCoreApplication.translate
        p = self.get_float_from_line_edit(self.deprec_p)
        vre = self.get_float_from_line_edit(self.deprec_vre)
        n = int(self.get_float_from_line_edit(self.deprec_n))
        if n <= 0: raise ValueError(tr("App", "Vida útil deve ser positiva."))

        # Corrigido: usar índice ao invés de comparação de texto
        is_linear = self.deprec_method.currentIndex() == 0  # 0 = Método Linear, 1 = Soma dos Dígitos
        result_text = ""

        k_text = self.deprec_k.text().strip()
        k = int(k_text) if k_text else None

        if k is not None and (k < 1 or k > n):
                raise ValueError(tr("App", "O ano 'k' deve estar entre 1 e a Vida Útil (N)."))

        # Normalização da formatação numérica/monetária
        def format_currency(value, decimals=2):
            s = f"{value:,.{decimals}f}"         # ex: "15,000.00"
            s = s.replace(",", "T")             # "15T000.00"
            s = s.replace(".", ",")             # "15T000,00"
            s = s.replace("T", ".")             # "15.000,00"
            return s

        # Função auxiliar para formatar frações com numerador centralizado sobre o traço
        def format_fraction(numer_str, denom_str, prefix=""):
            # prefix é aplicado somente na linha do traço
            numer = str(numer_str)
            denom = str(denom_str)
            width = max(len(numer), len(denom), 3)
            pad = " " * len(prefix)
            numer_line = pad + numer.center(width)
            divider_line = prefix + "─" * width
            denom_line = pad + denom.center(width)
            return numer_line, divider_line, denom_line

        steps = []

        if is_linear:
            dr_anual = (p - vre) / n

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "DEPRECIAÇÃO - MÉTODO LINEAR") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            f1, f2, f3 = format_fraction("(P - VRE)", "N", prefix="  DR = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Valor inicial')})      = R$ {format_currency(p)}\n")
            steps.append(f"  VRE ({tr('App', 'Valor residual')})   = R$ {format_currency(vre)}\n")
            steps.append(f"  N ({tr('App', 'Vida útil')})          = {format_currency(n,0)} {tr('App', 'anos')}\n\n")

            steps.append(tr("App", "Cálculo da depreciação anual:") + "\n")
            cf1, cf2, cf3 = format_fraction(f"({format_currency(p)} - {format_currency(vre)})", format_currency(n,0), prefix="  DR = ")
            steps.append(cf1 + "\n")
            steps.append(cf2 + "\n")
            steps.append(cf3 + f" = R$ {format_currency(dr_anual)}\n\n")

            if k is not None:
                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "CÁLCULO PARA O ANO") + f" {k}\n")
                steps.append("─" * 60 + "\n\n")

                vc_k = p - (k * dr_anual)
                dep_acumulada = k * dr_anual

                steps.append(tr("App", "Fórmula do Valor Contábil:") + "\n")
                steps.append("  VC_k = P - (k × DR)\n\n")

                steps.append(tr("App", "Cálculo:") + "\n")
                steps.append(f"  {tr('App', 'Depreciação acumulada até o ano')} {format_currency(k,0)}:\n")
                steps.append(f"    {tr('App', 'Dep. Acum.')} = {format_currency(k,0)} × {format_currency(dr_anual)} = R$ {format_currency(dep_acumulada)}\n\n")

                steps.append(f"  {tr('App', 'Valor Contábil ao final do ano')} {format_currency(k,0)}:\n")
                steps.append(f"    VC_{k} = P - {tr('App', 'Dep. Acum.')}\n")
                steps.append(f"    VC_{k} = {format_currency(p)} - {format_currency(dep_acumulada)}\n")
                steps.append(f"    VC_{k} = R$ {format_currency(vc_k)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA: Depreciação anual =") + f" R$ {format_currency(dr_anual)}\n")
            if k is not None:
                steps.append(f"          {tr('App', 'Valor contábil')} ({tr('App', 'ano')} {k}) = R$ {format_currency(vc_k)}\n")

            steps.append("─" * 60 + "\n")

        else: # Soma dos Dígitos
            soma_digitos = (n * (n + 1)) / 2

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "DEPRECIAÇÃO - SOMA DOS DÍGITOS DOS ANOS") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula:") + "\n")
            f1, f2, f3 = format_fraction("(N - k + 1)", tr("App", "Soma"), prefix="  DR_k = ")
            steps.append(f1 + "\n")
            steps.append(f2 + " × (P - VRE)\n")
            steps.append(f3 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Valor inicial')})      = R$ {format_currency(p)}\n")
            steps.append(f"  VRE ({tr('App', 'Valor residual')})   = R$ {format_currency(vre)}\n")
            steps.append(f"  N ({tr('App', 'Vida útil')})          = {format_currency(n,0)} {tr('App', 'anos')}\n\n")

            steps.append(tr("App", "Cálculo da Soma dos Dígitos:") + "\n")
            s1, s2, s3 = format_fraction("N × (N + 1)", "2", prefix=f"  {tr('App', 'Soma')} = ")
            steps.append(f"  {tr('App', 'Soma')} = 1 + 2 + 3 + ... + N\n")
            steps.append(s1 + "\n")
            steps.append(s2 + "\n")
            steps.append(s3 + "\n")
            sn1, sn2, sn3 = format_fraction(f"{format_currency(n,0)} × ({format_currency(n,0)} + 1)", "2", prefix=f"  {tr('App', 'Soma')} = ")
            steps.append(sn1 + "\n")
            steps.append(sn2 + "\n")
            steps.append(sn3 + f" = {format_currency(soma_digitos,0)}\n\n")

            steps.append(tr("App", "Total a depreciar:") + "\n")
            steps.append(f"  P - VRE = {format_currency(p)} - {format_currency(vre)} = R$ {format_currency(p - vre)}\n\n")

            if k is not None:
                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "CÁLCULO PARA O ANO") + f" {k}\n")
                steps.append("─" * 60 + "\n\n")

                fator_k = (n - k + 1) / soma_digitos
                dr_k = fator_k * (p - vre)

                steps.append(tr("App", "Quota de depreciação no ano") + f" {format_currency(k,0)}:\n")
                ftk1, ftk2, ftk3 = format_fraction("(N - k + 1)", tr("App", "Soma"), prefix=f"  {tr('App', 'Fator')} = ")
                steps.append(ftk1 + "\n")
                steps.append(ftk2 + "\n")
                steps.append(ftk3 + "\n")
                ftn1, ftn2, ftn3 = format_fraction(f"({format_currency(n,0)} - {format_currency(k,0)} + 1)", format_currency(soma_digitos,0), prefix=f"  {tr('App', 'Fator')} = ")
                steps.append(ftn1 + "\n")
                steps.append(ftn2 + "\n")
                steps.append(ftn3 + f" = {format_currency(fator_k,6)}\n\n")

                steps.append(f"  DR_{k} = {tr('App', 'Fator')} × (P - VRE)\n")
                steps.append(f"  DR_{k} = {format_currency(fator_k,6)} × {format_currency(p - vre)}\n")
                steps.append(f"  DR_{k} = R$ {format_currency(dr_k)}\n\n")

                # Calcular depreciação acumulada
                dep_acumulada = 0
                for j in range(1, k + 1):
                    dep_acumulada += ((n - j + 1) / soma_digitos) * (p - vre)

                vc_k = p - dep_acumulada

                steps.append(tr("App", "Depreciação acumulada até o ano") + f" {format_currency(k,0)}:\n")
                for j in range(1, k + 1):
                    dr_j = ((n - j + 1) / soma_digitos) * (p - vre)
                    steps.append(f"  {tr('App', 'Ano')} {format_currency(j,0)}: DR_{j} = R$ {format_currency(dr_j)}\n")

                steps.append(f"  {tr('App', 'Total acumulado')} = R$ {format_currency(dep_acumulada)}\n\n")

                steps.append(tr("App", "Valor Contábil ao final do ano") + f" {format_currency(k,0)}:\n")
                steps.append(f"  VC_{k} = P - {tr('App', 'Dep. Acum.')}\n")
                steps.append(f"  VC_{k} = {format_currency(p)} - {format_currency(dep_acumulada)}\n")
                steps.append(f"  VC_{k} = R$ {format_currency(vc_k)}\n\n")

            steps.append("─" * 60 + "\n")
            if k is not None:
                steps.append(tr("App", "RESPOSTA: Depreciação no ano") + f" {format_currency(k,0)} = R$ {format_currency(dr_k)}\n")
                steps.append(f"          {tr('App', 'Valor contábil')} ({tr('App', 'ano')} {format_currency(k,0)}) = R$ {format_currency(vc_k)}\n")

            else:
                steps.append(tr("App", "RESPOSTA: Soma dos dígitos =") + f" {format_currency(soma_digitos,0)}\n")

            steps.append("─" * 60 + "\n")

        result_text = "".join(steps)

        if result_text:
            self.deprec_result.append(result_text)

    except Exception as e:
        logger.error(f"Erro ao calcular depreciação: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.deprec_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
