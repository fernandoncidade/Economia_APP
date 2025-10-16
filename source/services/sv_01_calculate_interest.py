def calculate_interest(self):
    try:
        i = self.get_float_from_line_edit(self.interest_i, is_percentage=True)
        n = self.get_float_from_line_edit(self.interest_n)

        is_compound = self.interest_regime.currentText() == "Juros Compostos"
        calc_f = self.interest_calc_type.currentText() == "Calcular Montante (F)"

        result_text = ""

        if calc_f:
            p = self.get_float_from_line_edit(self.interest_p)
            if is_compound:
                f = p * (1 + i) ** n
                # passos detalhados
                steps = []
                steps.append("Juros Compostos - Cálculo do Montante (F)\n")
                steps.append(f"Fórmula: F = P * (1 + i)^n\n")
                steps.append(f"Substituindo: F = {p:.2f} * (1 + {i:.6f})^{n}\n")
                pow_val = (1 + i) ** n
                steps.append(f"Cálculo intermediário: (1 + i)^n = (1 + {i:.6f})^{n} = {pow_val:.6f}\n")
                steps.append(f"Montante: F = {p:.2f} * {pow_val:.6f} = R$ {f:.2f}\n")
                result_text = "".join(steps)

            else: # Juros Simples
                f = p * (1 + n * i)
                steps = []
                steps.append("Juros Simples - Cálculo do Montante (F)\n")
                steps.append("Fórmula: F = P * (1 + n * i)\n")
                steps.append(f"Substituindo: F = {p:.2f} * (1 + {n} * {i:.6f})\n")
                interp = 1 + n * i
                steps.append(f"Cálculo intermediário: 1 + n * i = {interp:.6f}\n")
                steps.append(f"Montante: F = {p:.2f} * {interp:.6f} = R$ {f:.2f}\n")
                result_text = "".join(steps)

        else: # Calcular Principal (P)
            f = self.get_float_from_line_edit(self.interest_f)
            if is_compound:
                p = f / (1 + i) ** n
                steps = []
                steps.append("Juros Compostos - Cálculo do Principal (P)\n")
                steps.append("Fórmula: P = F / (1 + i)^n\n")
                steps.append(f"Substituindo: P = {f:.2f} / (1 + {i:.6f})^{n}\n")
                denom = (1 + i) ** n
                steps.append(f"Cálculo intermediário: (1 + i)^n = {denom:.6f}\n")
                steps.append(f"Principal: P = {f:.2f} / {denom:.6f} = R$ {p:.2f}\n")
                result_text = "".join(steps)

            else: # Juros Simples
                p = f / (1 + n * i)
                steps = []
                steps.append("Juros Simples - Cálculo do Principal (P)\n")
                steps.append("Fórmula: P = F / (1 + n * i)\n")
                steps.append(f"Substituindo: P = {f:.2f} / (1 + {n} * {i:.6f})\n")
                denom = 1 + n * i
                steps.append(f"Cálculo intermediário: 1 + n * i = {denom:.6f}\n")
                steps.append(f"Principal: P = {f:.2f} / {denom:.6f} = R$ {p:.2f}\n")
                result_text = "".join(steps)

        self.interest_result.setText(result_text)

    except Exception as e:
        self.interest_result.setText(f"Erro: {e}")
