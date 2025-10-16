def calculate_rate_equivalence(self):
    try:
        i = self.get_float_from_line_edit(self.rate_equiv_i, is_percentage=True)
        n1 = self.get_float_from_line_edit(self.rate_equiv_current_n)
        n2 = self.get_float_from_line_edit(self.rate_equiv_target_n)

        # (1+i_eq) = (1+i)^(n2/n1)
        i_eq = (1 + i) ** (n2 / n1) - 1

        steps = []
        steps.append("Equivalência de Taxas Efetivas\n")
        steps.append("Fórmula: (1 + i_eq) = (1 + i)^(n2 / n1)\n")
        steps.append(f"Substituindo: (1 + i_eq) = (1 + {i:.6f})^({n2} / {n1})\n")
        pow_val = (1 + i) ** (n2 / n1)
        steps.append(f"Cálculo intermediário: (1 + i)^(n2/n1) = {pow_val:.6f}\n")
        steps.append(f"i_eq = {pow_val:.6f} - 1 = {i_eq * 100:.6f} %\n")

        self.rate_equiv_result.append("".join(steps))

    except Exception as e:
        self.rate_equiv_result.append(f"Erro: {e}")

def calculate_real_rate(self):
    try:
        calc_apparent = self.rate_real_calc_type.currentText() == "Calcular Taxa Aparente (i)"

        if calc_apparent:
            r = self.get_float_from_line_edit(self.rate_real_r, is_percentage=True)
            inflation = self.get_float_from_line_edit(self.rate_real_inflation, is_percentage=True)
            # 1+i = (1+r)*(1+inflation)
            i = (1 + r) * (1 + inflation) - 1
            steps = []
            steps.append("Cálculo da Taxa Aparente (i)\n")
            steps.append("Fórmula: 1 + i = (1 + r) * (1 + θ)\n")
            steps.append(f"Substituindo: 1 + i = (1 + {r:.6f}) * (1 + {inflation:.6f})\n")
            prod = (1 + r) * (1 + inflation)
            steps.append(f"Cálculo intermediário: (1 + r)*(1 + θ) = {prod:.6f}\n")
            steps.append(f"i = {prod:.6f} - 1 = {i * 100:.6f} %\n")
            self.rate_real_result.append("".join(steps))

        else: # Calcular Taxa Real
            i = self.get_float_from_line_edit(self.rate_real_i, is_percentage=True)
            inflation = self.get_float_from_line_edit(self.rate_real_inflation, is_percentage=True)
            # 1+r = (1+i)/(1+inflation)
            r = (1 + i) / (1 + inflation) - 1
            steps = []
            steps.append("Cálculo da Taxa Real (r)\n")
            steps.append("Fórmula: 1 + r = (1 + i) / (1 + θ)\n")
            steps.append(f"Substituindo: 1 + r = (1 + {i:.6f}) / (1 + {inflation:.6f})\n")
            div = (1 + i) / (1 + inflation)
            steps.append(f"Cálculo intermediário: (1 + i)/(1 + θ) = {div:.6f}\n")
            steps.append(f"r = {div:.6f} - 1 = {r * 100:.6f} %\n")
            self.rate_real_result.append("".join(steps))

    except Exception as e:
        self.rate_real_result.append(f"Erro: {e}")
