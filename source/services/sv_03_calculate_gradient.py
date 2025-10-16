def calculate_gradient(self):
    try:
        i = self.get_float_from_line_edit(self.grad_i, is_percentage=True)
        n = self.get_float_from_line_edit(self.grad_n)
        is_arithmetic = self.grad_type.currentText().startswith("Gradiente Aritmético")
        result_text = ""

        if is_arithmetic:
            g = self.get_float_from_line_edit(self.grad_g)
            # P = G/i * [(P/A, i, n) - n*(P/F, i, n)]
            pow_val = (1 + i)**n
            num_pa = pow_val - 1
            den_pa = i * pow_val
            factor_pa = num_pa / den_pa
            factor_pf = 1 / pow_val
            p = (g / i) * (factor_pa - n * factor_pf)
            steps = []
            steps.append("Gradiente Aritmético - cálculo do Valor Presente (P)\n")
            steps.append("Fórmula usada: P = G/i * [ (P/A,i,n) - n*(P/F,i,n) ]\n")
            steps.append(f"(1+i)^n = {pow_val:.6f}\n")
            steps.append(f"(P/A) = [ (1+i)^n - 1 ] / [ i*(1+i)^n ] = ({num_pa:.6f}) / ({den_pa:.6f}) = {factor_pa:.6f}\n")
            steps.append(f"(P/F) = 1 / (1+i)^n = 1 / {pow_val:.6f} = {factor_pf:.6f}\n")
            steps.append(f"G = {g:.2f}, i = {i:.6f}, n = {n}\n")
            steps.append(f"P = ({g:.2f} / {i:.6f}) * ({factor_pa:.6f} - {n} * {factor_pf:.6f}) = R$ {p:.2f}\n")
            result_text = "".join(steps)

        else: # Geométrico
            g = self.get_float_from_line_edit(self.grad_g, is_percentage=True)
            x1_placeholder = 1
            r = (1 + g) / (1 + i)
            rn = r ** n
            num = 1 - rn
            den = i - g
            steps = []
            steps.append("Gradiente Geométrico - cálculo do Valor Presente (P)\n")
            steps.append("Fórmula: P = X1 * [1 - ((1+g)/(1+i))^n] / (i - g)\n")
            steps.append(f"Assumindo X1 = {x1_placeholder}, g = {g*100:.6f} %, i = {i*100:.6f} %\n")

            if i == g:
                p = x1_placeholder * n / (1 + i)
                steps.append("Caso i = g: P = X1 * n / (1+i)\n")
                steps.append(f"P = {x1_placeholder} * {n} / (1 + {i:.6f}) = R$ {p:.2f}\n")

            else:
                steps.append(f"r = (1+g)/(1+i) = (1+{g:.6f})/(1+{i:.6f}) = {r:.6f}\n")
                steps.append(f"r^n = {r:.6f}^{int(n)} = {rn:.6f}\n")
                steps.append(f"Numerador = 1 - r^n = 1 - {rn:.6f} = {num:.6f}\n")
                steps.append(f"Denominador = i - g = {i:.6f} - {g:.6f} = {den:.6f}\n")
                p = x1_placeholder * num / den
                steps.append(f"P = {x1_placeholder} * {num:.6f} / {den:.6f} = R$ {p:.2f}\n")

            result_text = "".join(steps)

        self.grad_result.setText(result_text)

    except Exception as e:
        self.grad_result.setText(f"Erro: {e}")
