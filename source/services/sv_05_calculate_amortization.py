from PySide6.QtWidgets import QTableWidgetItem

def calculate_amortization(self):
    try:
        p = self.get_float_from_line_edit(self.amort_p)
        i = self.get_float_from_line_edit(self.amort_i, is_percentage=True)
        n = int(self.get_float_from_line_edit(self.amort_n))

        self.amort_table.setRowCount(n + 1)

        self.amort_table.setItem(0, 0, QTableWidgetItem("0"))
        for col in range(1, 4): self.amort_table.setItem(0, col, QTableWidgetItem("-"))
        self.amort_table.setItem(0, 4, QTableWidgetItem(f"{p:.2f}"))

        system = self.amort_system.currentText()

        # Preparar texto detalhado com passos
        steps = []
        steps.append(f"Entradas: P = R$ {p:.2f}, i = {i*100:.6f} %, n = {n}\n")

        if system.startswith("Sistema de Amortização Constante"):
            steps.append("Sistema SAC (Amortização constante)\n")
            steps.append("Fórmulas gerais:\n")
            steps.append(" - Amortização (constante): A_k = P / n\n")
            steps.append(" - Juros: J_k = SD_{k-1} * i\n")
            steps.append(" - Prestação: Prest_k = A_k + J_k\n")
            steps.append(" - Saldo: SD_k = SD_{k-1} - A_k\n")
            amort_const = p / n
            steps.append(f"\nAmortização constante = P / n = {p:.2f} / {n} = R$ {amort_const:.2f}\n")
            juros1 = p * i
            prest1 = amort_const + juros1
            saldo1 = p - amort_const
            steps.append("Período 1:\n")
            steps.append(f" Juros J_1 = SD_0 * i = {p:.2f} * {i:.6f} = R$ {juros1:.2f}\n")
            steps.append(f" Prestação = A_1 + J_1 = {amort_const:.2f} + {juros1:.2f} = R$ {prest1:.2f}\n")
            steps.append(f" Saldo SD_1 = SD_0 - A_1 = {p:.2f} - {amort_const:.2f} = R$ {saldo1:.2f}\n")
            self.amort_result.append("".join(steps))

            self.generate_sac_table(p, i, n)

        elif system.startswith("Sistema Francês"):
            steps.append("Sistema Francês (Price)\n")
            steps.append("Fórmulas gerais:\n")
            steps.append(" - Fator (A/P) = [i*(1+i)^n] / [(1+i)^n - 1]\n")
            steps.append(" - Juros: J_k = SD_{k-1} * i\n")
            steps.append(" - Amortização: Amort_k = A - J_k\n")
            steps.append(" - Saldo: SD_k = SD_{k-1} - Amort_k\n")
            pow_val = (1 + i)**n
            num = i * pow_val
            den = pow_val - 1
            factor = num / den
            prest = p * factor
            steps.append(f"(1+i)^n = {pow_val:.6f}\n")
            steps.append(f"Numerador: i*(1+i)^n = {i:.6f} * {pow_val:.6f} = {num:.6f}\n")
            steps.append(f"Denominador: (1+i)^n - 1 = {pow_val:.6f} - 1 = {den:.6f}\n")
            steps.append(f"Fator (A/P) = {num:.6f} / {den:.6f} = {factor:.6f}\n")
            steps.append(f"Prestação constante A = P * fator = {p:.2f} * {factor:.6f} = R$ {prest:.2f}\n")
            juros1 = p * i
            amort1 = prest - juros1
            saldo1 = p - amort1
            steps.append("Período 1:\n")
            steps.append(f" Juros J_1 = SD_0 * i = {p:.2f} * {i:.6f} = R$ {juros1:.2f}\n")
            steps.append(f" Amortização Amort_1 = A - J_1 = {prest:.2f} - {juros1:.2f} = R$ {amort1:.2f}\n")
            steps.append(f" Saldo SD_1 = SD_0 - Amort_1 = {p:.2f} - {amort1:.2f} = R$ {saldo1:.2f}\n")
            self.amort_result.append("".join(steps))

            self.generate_price_table(p, i, n)

        else: # SAM
            steps.append("Sistema Misto (SAM) - média entre SAC e Price por período\n")
            steps.append("Procedimento por período k:\n")
            steps.append(" 1) Calcular Prest_SAC_k, J_SAC_k, Amort_SAC_k, SD_SAC_k\n")
            steps.append(" 2) Calcular Prest_Price_k, J_Price_k, Amort_Price_k, SD_Price_k\n")
            steps.append(" 3) Tirar a média: Prest_SAM_k = (Prest_SAC_k + Prest_Price_k)/2 (idem para Juros, Amortização e Saldo)\n")
            # Demonstração detalhada do 1º período
            amort_const = p / n
            sac_juros1 = p * i
            sac_prest1 = amort_const + sac_juros1
            sac_saldo1 = p - amort_const

            pow_val = (1 + i)**n
            num = i * pow_val
            den = pow_val - 1
            factor = num / den
            price_prest = p * factor
            price_juros1 = p * i
            price_amort1 = price_prest - price_juros1
            price_saldo1 = p - price_amort1

            sam_prest1 = (sac_prest1 + price_prest) / 2
            sam_juros1 = (sac_juros1 + price_juros1) / 2
            sam_amort1 = (amort_const + price_amort1) / 2
            sam_saldo1 = (sac_saldo1 + price_saldo1) / 2

            steps.append("\nDemonstração no período 1:\n")
            steps.append(f" SAC: A_const = P/n = {p:.2f}/{n} = {amort_const:.2f}, J_1 = {p:.2f}*{i:.6f} = {sac_juros1:.2f}, Prest_1 = {sac_prest1:.2f}, SD_1 = {sac_saldo1:.2f}\n")
            steps.append(f" Price: fator (A/P) = {num:.6f}/{den:.6f} = {factor:.6f} -> A = {p:.2f}*{factor:.6f} = {price_prest:.2f}, ")
            steps.append(f"J_1 = {p:.2f}*{i:.6f} = {price_juros1:.2f}, Amort_1 = {price_amort1:.2f}, SD_1 = {price_saldo1:.2f}\n")
            steps.append(f" SAM (médias): Prest_1 = ({sac_prest1:.2f}+{price_prest:.2f})/2 = {sam_prest1:.2f}, ")
            steps.append(f"J_1 = ({sac_juros1:.2f}+{price_juros1:.2f})/2 = {sam_juros1:.2f}, ")
            steps.append(f"Amort_1 = ({amort_const:.2f}+{price_amort1:.2f})/2 = {sam_amort1:.2f}, ")
            steps.append(f"SD_1 = ({sac_saldo1:.2f}+{price_saldo1:.2f})/2 = {sam_saldo1:.2f}\n")

            self.amort_result.append("".join(steps))

            self.generate_sam_table(p, i, n)

    except Exception as e:
        self.amort_table.setRowCount(1)
        self.amort_table.setSpan(0,0,1,5)
        self.amort_table.setItem(0,0, QTableWidgetItem(f"Erro ao gerar tabela: {e}"))
        self.amort_result.append(f"Erro: {e}")
