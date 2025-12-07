from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
from source.utils.TextFormat import format_currency, format_fraction, to_subscript

logger = LogManager.get_logger()

def calculate_depreciation(self):
    try:
        tr = QCoreApplication.translate
        p = self.get_float_from_line_edit(self.deprec_p)
        vre = self.get_float_from_line_edit(self.deprec_vre)
        n = int(self.get_float_from_line_edit(self.deprec_n))
        if n <= 0: raise ValueError(tr("App", "Vida útil deve ser positiva."))

        # 0 = Linear, 1 = Soma Decrescente, 2 = Soma Crescente
        method_index = self.deprec_method.currentIndex()
        result_text = ""

        k_text = self.deprec_k.text().strip()
        k = int(k_text) if k_text else None

        if k is not None and (k < 1 or k > n):
            raise ValueError(tr("App", "O ano 'k' deve estar entre 1 e a Vida Útil (N)."))

        steps = []

        # ============================================================
        # MÉTODO LINEAR
        # ============================================================
        if method_index == 0:
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
                deprec_acum = dr_anual * k
                vc_k = p - deprec_acum

                steps.append("─" * 60 + "\n")
                steps.append(f"{tr('App', 'Análise no ano')} k = {k}\n")
                steps.append("─" * 60 + "\n\n")

                steps.append(f"  {tr('App', 'Depreciação anual')}:      DR = R$ {format_currency(dr_anual)}\n")
                steps.append(f"  {tr('App', 'Depreciação acumulada')}: DR{to_subscript('acum')} = {k} × {format_currency(dr_anual)} = R$ {format_currency(deprec_acum)}\n")
                steps.append(f"  {tr('App', 'Valor Contábil')}: VC{to_subscript(k)} = P - DR{to_subscript('acum')} = {format_currency(p)} - {format_currency(deprec_acum)} = R$ {format_currency(vc_k)}\n\n")

            steps.append("─" * 60 + "\n")
            steps.append(tr("App", "RESPOSTA: Depreciação anual =") + f" R$ {format_currency(dr_anual)}\n")
            if k is not None:
                steps.append(f"          {tr('App', 'Valor Contábil no ano')} {k} = R$ {format_currency(vc_k)}\n")
            steps.append("─" * 60 + "\n")

        # ============================================================
        # SOMA DOS DÍGITOS - DECRESCENTE
        # ============================================================
        elif method_index == 1:
            soma_digitos = (n * (n + 1)) / 2

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "DEPRECIAÇÃO - SOMA DOS DÍGITOS (DECRESCENTE)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula da depreciação no ano n:") + "\n")
            f1, f2, f3 = format_fraction("(N - n + 1)", "S", prefix=f"  DR{to_subscript('n')} = ")
            steps.append(f1 + " × (P - VRE)\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Valor inicial')})      = R$ {format_currency(p)}\n")
            steps.append(f"  VRE ({tr('App', 'Valor residual')})   = R$ {format_currency(vre)}\n")
            steps.append(f"  N ({tr('App', 'Vida útil')})          = {format_currency(n,0)} {tr('App', 'anos')}\n\n")

            steps.append(tr("App", "Cálculo da Soma dos Dígitos:") + "\n")
            s1, s2, s3 = format_fraction("N × (N + 1)", "2", prefix=f"  S = ")
            steps.append(s1 + "\n")
            steps.append(s2 + "\n")
            steps.append(s3 + "\n")
            steps.append(f"  S = {format_currency(n,0)} × {format_currency(n+1,0)} / 2\n")
            steps.append(f"  S = {format_currency(soma_digitos,0)}\n\n")

            depreciavel = p - vre

            if k is not None:
                # Cálculo para ano específico k
                steps.append("─" * 60 + "\n")
                steps.append(f"{tr('App', 'Análise no ano')} k = {k}\n")
                steps.append("─" * 60 + "\n\n")

                # DR_k
                dr_k = ((n - k + 1) / soma_digitos) * depreciavel
                steps.append(f"{tr('App', 'Depreciação no ano')} {k}:\n")
                f1, f2, f3 = format_fraction(f"({n} - {k} + 1)", format_currency(soma_digitos,0), prefix=f"  DR{to_subscript(k)} = ")
                steps.append(f1 + f" × {format_currency(depreciavel)}\n")
                steps.append(f2 + "\n")
                steps.append(f3 + "\n")
                steps.append(f"  DR{to_subscript(k)} = R$ {format_currency(dr_k)}\n\n")

                # Depreciação acumulada até k
                soma_parcial = sum(n - j + 1 for j in range(1, k + 1))
                deprec_acum = (soma_parcial / soma_digitos) * depreciavel

                steps.append(f"{tr('App', 'Depreciação acumulada até o ano')} {k}:\n")
                formula_str = " + ".join([f"({n}-{j}+1)" for j in range(1, k + 1)])
                steps.append(f"  {tr('App', 'Soma dos fatores')}: {formula_str} = {format_currency(soma_parcial,0)}\n")
                
                f1, f2, f3 = format_fraction(format_currency(soma_parcial,0), format_currency(soma_digitos,0), prefix=f"  DR{to_subscript('acum')} = ")
                steps.append(f1 + f" × {format_currency(depreciavel)}\n")
                steps.append(f2 + "\n")
                steps.append(f3 + "\n")
                steps.append(f"  DR{to_subscript('acum')} = R$ {format_currency(deprec_acum)}\n\n")

                # Valor Contábil (Valor Real)
                vc_k = p - deprec_acum
                steps.append(f"{tr('App', 'Valor Contábil (Valor Real) ao final do ano')} {k}:\n")
                steps.append(f"  VR{to_subscript(k)} = P - DR{to_subscript('acum')}\n")
                steps.append(f"  VR{to_subscript(k)} = {format_currency(p)} - {format_currency(deprec_acum)}\n")
                steps.append(f"  VR{to_subscript(k)} = R$ {format_currency(vc_k)}\n\n")

                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA:") + "\n")
                steps.append(f"  {tr('App', 'Depreciação no ano')} {k}: R$ {format_currency(dr_k)}\n")
                steps.append(f"  {tr('App', 'Depreciação acumulada')}: R$ {format_currency(deprec_acum)}\n")
                steps.append(f"  {tr('App', 'Valor Real ao final do ano')} {k}: R$ {format_currency(vc_k)}\n")
                steps.append("═" * 60 + "\n")

            else:
                # Tabela completa
                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "Tabela de Depreciação Completa") + "\n")
                steps.append("─" * 60 + "\n\n")

                steps.append(f"{'Ano':>4} | {'Fator':>10} | {'DR (R$)':>15} | {'DR Acum (R$)':>15} | {'VC (R$)':>15}\n")
                steps.append("─" * 80 + "\n")

                deprec_acum = 0
                for j in range(1, n + 1):
                    fator = n - j + 1
                    dr_j = (fator / soma_digitos) * depreciavel
                    deprec_acum += dr_j
                    vc_j = p - deprec_acum

                    steps.append(f"{j:4} | {fator:10} | {format_currency(dr_j):>15} | {format_currency(deprec_acum):>15} | {format_currency(vc_j):>15}\n")

                steps.append("─" * 80 + "\n")

        # ============================================================
        # SOMA DOS DÍGITOS - CRESCENTE
        # ============================================================
        elif method_index == 2:
            soma_digitos = (n * (n + 1)) / 2

            steps.append("═" * 60 + "\n")
            steps.append(tr("App", "DEPRECIAÇÃO - SOMA DOS DÍGITOS (CRESCENTE)") + "\n")
            steps.append("═" * 60 + "\n\n")

            steps.append(tr("App", "Fórmula da depreciação no ano n:") + "\n")
            f1, f2, f3 = format_fraction("n", "S", prefix=f"  DR{to_subscript('n')} = ")
            steps.append(f1 + " × (P - VRE)\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n\n")

            steps.append(tr("App", "Dados do problema:") + "\n")
            steps.append(f"  P ({tr('App', 'Valor inicial')})      = R$ {format_currency(p)}\n")
            steps.append(f"  VRE ({tr('App', 'Valor residual')})   = R$ {format_currency(vre)}\n")
            steps.append(f"  N ({tr('App', 'Vida útil')})          = {format_currency(n,0)} {tr('App', 'anos')}\n\n")

            steps.append(tr("App", "Cálculo da Soma dos Dígitos:") + "\n")
            s1, s2, s3 = format_fraction("N × (N + 1)", "2", prefix=f"  S = ")
            steps.append(s1 + "\n")
            steps.append(s2 + "\n")
            steps.append(s3 + "\n")
            steps.append(f"  S = {format_currency(n,0)} × {format_currency(n+1,0)} / 2\n")
            steps.append(f"  S = {format_currency(soma_digitos,0)}\n\n")

            depreciavel = p - vre

            if k is not None:
                # Cálculo para ano específico k
                steps.append("─" * 60 + "\n")
                steps.append(f"{tr('App', 'Análise no ano')} k = {k}\n")
                steps.append("─" * 60 + "\n\n")

                # DR_k
                dr_k = (k / soma_digitos) * depreciavel
                steps.append(f"{tr('App', 'Depreciação no ano')} {k}:\n")
                f1, f2, f3 = format_fraction(str(k), format_currency(soma_digitos,0), prefix=f"  DR{to_subscript(k)} = ")
                steps.append(f1 + f" × {format_currency(depreciavel)}\n")
                steps.append(f2 + "\n")
                steps.append(f3 + "\n")
                steps.append(f"  DR{to_subscript(k)} = {k} / {format_currency(soma_digitos,0)} × {format_currency(depreciavel)}\n")
                steps.append(f"  DR{to_subscript(k)} = R$ {format_currency(dr_k)}\n\n")

                # Depreciação acumulada até k
                soma_parcial = sum(j for j in range(1, k + 1))
                deprec_acum = (soma_parcial / soma_digitos) * depreciavel

                steps.append(f"{tr('App', 'Depreciação acumulada até o ano')} {k}:\n")
                formula_str = " + ".join([str(j) for j in range(1, k + 1)])
                steps.append(f"  {tr('App', 'Soma dos fatores')}: {formula_str} = {format_currency(soma_parcial,0)}\n")
                
                f1, f2, f3 = format_fraction(format_currency(soma_parcial,0), format_currency(soma_digitos,0), prefix=f"  DR{to_subscript('acum')} = ")
                steps.append(f1 + f" × {format_currency(depreciavel)}\n")
                steps.append(f2 + "\n")
                steps.append(f3 + "\n")
                steps.append(f"  DR{to_subscript('acum')} = R$ {format_currency(deprec_acum)}\n\n")

                # Valor Contábil (Valor Real)
                vc_k = p - deprec_acum
                steps.append(f"{tr('App', 'Valor Contábil (Valor Real) ao final do ano')} {k}:\n")
                steps.append(f"  VR{to_subscript(k)} = P - DR{to_subscript('acum')}\n")
                steps.append(f"  VR{to_subscript(k)} = {format_currency(p)} - {format_currency(deprec_acum)}\n")
                steps.append(f"  VR{to_subscript(k)} = R$ {format_currency(vc_k)}\n\n")

                steps.append("═" * 60 + "\n")
                steps.append(tr("App", "RESPOSTA:") + "\n")
                steps.append(f"  {tr('App', 'Depreciação no ano')} {k}: R$ {format_currency(dr_k)}\n")
                steps.append(f"  {tr('App', 'Depreciação acumulada')}: R$ {format_currency(deprec_acum)}\n")
                steps.append(f"  {tr('App', 'Valor Real ao final do ano')} {k}: R$ {format_currency(vc_k)}\n")
                steps.append("═" * 60 + "\n")

            else:
                # Tabela completa
                steps.append("─" * 60 + "\n")
                steps.append(tr("App", "Tabela de Depreciação Completa") + "\n")
                steps.append("─" * 60 + "\n\n")

                steps.append(f"{'Ano':>4} | {'Fator':>10} | {'DR (R$)':>15} | {'DR Acum (R$)':>15} | {'VC (R$)':>15}\n")
                steps.append("─" * 80 + "\n")

                deprec_acum = 0
                for j in range(1, n + 1):
                    fator = j
                    dr_j = (fator / soma_digitos) * depreciavel
                    deprec_acum += dr_j
                    vc_j = p - deprec_acum

                    steps.append(f"{j:4} | {fator:10} | {format_currency(dr_j):>15} | {format_currency(deprec_acum):>15} | {format_currency(vc_j):>15}\n")

                steps.append("─" * 80 + "\n")

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
