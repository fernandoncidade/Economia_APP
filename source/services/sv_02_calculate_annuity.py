def calculate_annuity(self):
    try:
        i = self.get_float_from_line_edit(self.annuity_i, is_percentage=True)
        n = self.get_float_from_line_edit(self.annuity_n)

        is_postecipada = self.annuity_type.currentText() == "Postecipada"
        calc_a = self.annuity_calc_type.currentText() == "Calcular Prestação (A)"

        result_text = ""

        if calc_a:
            p = self.get_float_from_line_edit(self.annuity_p)
            if is_postecipada:
                # Fator A/P
                pow_val = (1 + i) ** n
                num = i * pow_val
                den = pow_val - 1
                factor = num / den
                a = p * factor
                steps = []
                steps.append("Cálculo da Prestação (A) - Série Postecipada\n")
                steps.append("Fórmula: A = P * [i*(1+i)^n] / [(1+i)^n - 1]\n")
                steps.append(f"(1+i)^n = {pow_val:.6f}\n")
                steps.append(f"Numerador: i*(1+i)^n = {i:.6f} * {pow_val:.6f} = {num:.6f}\n")
                steps.append(f"Denominador: (1+i)^n - 1 = {pow_val:.6f} - 1 = {den:.6f}\n")
                steps.append(f"Fator A/P = {num:.6f} / {den:.6f} = {factor:.6f}\n")
                steps.append(f"Prestação A = {p:.2f} * {factor:.6f} = R$ {a:.2f}\n")
                result_text = "".join(steps)

            else: # Antecipada
                pow_n = (1 + i) ** n
                pow_nm1 = (1 + i) ** (n - 1) if n > 0 else 1.0
                num = i * pow_nm1
                den = pow_n - 1
                factor = num / den if den != 0 else 0
                a = p * factor
                steps = []
                steps.append("Cálculo da Prestação (A') - Série Antecipada\n")
                steps.append("Fórmula: A' = P * [i*(1+i)^(n-1)] / [(1+i)^n - 1]\n")
                steps.append(f"(1+i)^n = {pow_n:.6f}\n")
                steps.append(f"(1+i)^(n-1) = {pow_nm1:.6f}\n")
                steps.append(f"Numerador: i*(1+i)^(n-1) = {i:.6f} * {pow_nm1:.6f} = {num:.6f}\n")
                steps.append(f"Denominador: (1+i)^n - 1 = {pow_n:.6f} - 1 = {den:.6f}\n")
                steps.append(f"Fator A'/P = {num:.6f} / {den:.6f} = {factor:.6f}\n")
                steps.append(f"Prestação A' = {p:.2f} * {factor:.6f} = R$ {a:.2f}\n")
                result_text = "".join(steps)

            if result_text:
                self.annuity_result.append(result_text)

        else: # Calcular P
            a = self.get_float_from_line_edit(self.annuity_a)
            if is_postecipada:
                pow_val = (1 + i) ** n
                num = pow_val - 1
                den = i * pow_val
                factor = num / den
                p = a * factor
                steps = []
                steps.append("Cálculo do Valor Presente (P) - Série Postecipada\n")
                steps.append("Fórmula: P = A * [(1+i)^n - 1] / [i*(1+i)^n]\n")
                steps.append(f"(1+i)^n = {pow_val:.6f}\n")
                steps.append(f"Numerador: (1+i)^n - 1 = {pow_val:.6f} - 1 = {num:.6f}\n")
                steps.append(f"Denominador: i*(1+i)^n = {i:.6f} * {pow_val:.6f} = {den:.6f}\n")
                steps.append(f"Fator P/A = {num:.6f} / {den:.6f} = {factor:.6f}\n")
                steps.append(f"P = {a:.2f} * {factor:.6f} = R$ {p:.2f}\n")
                result_text = "".join(steps)

            else: # Antecipada
                pow_n = (1 + i) ** n
                pow_nm1 = (1 + i) ** (n - 1) if n > 0 else 1.0
                num = pow_n - 1
                den = i * pow_nm1
                factor = num / den if den != 0 else 0
                p = a * factor
                steps = []
                steps.append("Cálculo do Valor Presente (P) - Série Antecipada\n")
                steps.append("Fórmula: P = A' * [(1+i)^n - 1] / [i*(1+i)^(n-1)]\n")
                steps.append(f"(1+i)^n = {pow_n:.6f}\n")
                steps.append(f"(1+i)^(n-1) = {pow_nm1:.6f}\n")
                steps.append(f"Numerador: (1+i)^n - 1 = {pow_n:.6f} - 1 = {num:.6f}\n")
                steps.append(f"Denominador: i*(1+i)^(n-1) = {i:.6f} * {pow_nm1:.6f} = {den:.6f}\n")
                steps.append(f"Fator P/A' = {num:.6f} / {den:.6f} = {factor:.6f}\n")
                steps.append(f"P = {a:.2f} * {factor:.6f} = R$ {p:.2f}\n")
                result_text = "".join(steps)

            if result_text:
                self.annuity_result.append(result_text)

    except Exception as e:
        self.annuity_result.append(f"Erro: {e}")
