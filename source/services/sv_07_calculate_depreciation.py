def calculate_depreciation(self):
    try:
        p = self.get_float_from_line_edit(self.deprec_p)
        vre = self.get_float_from_line_edit(self.deprec_vre)
        n = int(self.get_float_from_line_edit(self.deprec_n))
        if n <= 0: raise ValueError("Vida útil deve ser positiva.")

        is_linear = self.deprec_method.currentText() == "Método Linear"
        result_text = ""

        k_text = self.deprec_k.text().strip()
        k = int(k_text) if k_text else None

        if k is not None and (k < 1 or k > n):
                raise ValueError("O ano 'k' deve estar entre 1 e a Vida Útil (N).")

        if is_linear:
            dr_anual = (p - vre) / n
            steps = []
            steps.append("Depreciação - Método Linear\n")
            steps.append("Fórmula: DR = (P - VRE) / N\n")
            steps.append(f"Substituindo: DR = ({p:.2f} - {vre:.2f}) / {n} = R$ {dr_anual:.2f} por ano\n")
            if k is not None:
                vc_k = p - (k * dr_anual)
                steps.append(f"Valor contábil ao final do ano {k}: VC_{k} = P - k*DR = {p:.2f} - {k}*{dr_anual:.2f} = R$ {vc_k:.2f}\n")

            result_text = "".join(steps)

        else: # Soma dos Dígitos
            soma_digitos = (n * (n + 1)) / 2
            steps = []
            steps.append("Depreciação - Soma dos Dígitos dos Anos\n")
            steps.append(f"Soma dos dígitos = 1 + 2 + ... + N = N*(N+1)/2 = {soma_digitos:.0f}\n")
            steps.append(f"Total a depreciar = P - VRE = {p:.2f} - {vre:.2f} = R$ {p - vre:.2f}\n")

            if k is not None:
                dr_k = ((n - k + 1) / soma_digitos) * (p - vre)
                steps.append(f"Quota do ano {k}: DR_{k} = (N - k + 1)/Soma * (P - VRE)\n")
                steps.append(f"DR_{k} = ({n} - {k} + 1) / {soma_digitos:.0f} * {p - vre:.2f} = R$ {dr_k:.2f}\n")
                dep_acumulada = 0
                for j in range(1, k + 1):
                    dep_acumulada += ((n - j + 1) / soma_digitos) * (p - vre)

                vc_k = p - dep_acumulada
                steps.append(f"Depreciação acumulada até o ano {k} = R$ {dep_acumulada:.2f}\n")
                steps.append(f"Valor contábil ao final do ano {k}: VC_{k} = P - Dep Acumulada = {p:.2f} - {dep_acumulada:.2f} = R$ {vc_k:.2f}\n")

            result_text = "".join(steps)

        self.deprec_result.setText(result_text)

    except Exception as e:
        self.deprec_result.setText(f"Erro: {e}")
