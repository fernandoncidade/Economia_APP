def calculate_investment(self):
    try:
        inv_inicial = self.get_float_from_line_edit(self.invest_initial)
        a = self.get_float_from_line_edit(self.invest_cashflow)
        n = self.get_float_from_line_edit(self.invest_n)
        tma = self.get_float_from_line_edit(self.invest_tma, is_percentage=True)

        # VPL = VPB - VPC
        pow_val = (1 + tma) ** n
        num_pa = pow_val - 1
        den_pa = tma * pow_val
        factor_pa = num_pa / den_pa
        vpb = a * factor_pa
        vpl = vpb - inv_inicial

        # VAUE = VPL * (A/P, tma, n)
        num_ap = tma * pow_val
        den_ap = pow_val - 1
        factor_ap = num_ap / den_ap
        vaue = vpl * factor_ap

        steps = []
        steps.append("Análise de Investimentos - VPL e VAUE\n")
        steps.append(f"Entradas: Investimento Inicial = R$ {inv_inicial:.2f}, A = R$ {a:.2f}, n = {n}, TMA = {tma*100:.6f} %\n\n")
        steps.append("Cálculo do VPB (Valor Presente dos Benefícios):\n")
        steps.append("VPB = A * (P/A, TMA, n)\n")
        steps.append(f"(1+TMA)^n = {pow_val:.6f}\n")
        steps.append(f"(P/A) = [ (1+TMA)^n - 1 ] / [ TMA * (1+TMA)^n ] = ({num_pa:.6f}) / ({den_pa:.6f}) = {factor_pa:.6f}\n")
        steps.append(f"VPB = {a:.2f} * {factor_pa:.6f} = R$ {vpb:.2f}\n\n")
        steps.append(f"VPC (custos) = Investimento Inicial = R$ {inv_inicial:.2f}\n")
        steps.append(f"VPL = VPB - VPC = {vpb:.2f} - {inv_inicial:.2f} = R$ {vpl:.2f}\n\n")
        steps.append("Cálculo da VAUE (Valor Anualizado do VPL):\n")
        steps.append("VAUE = VPL * (A/P, TMA, n)\n")
        steps.append(f"(A/P) = [ TMA*(1+TMA)^n ] / [ (1+TMA)^n - 1 ] = ({num_ap:.6f}) / ({den_ap:.6f}) = {factor_ap:.6f}\n")
        steps.append(f"VAUE = {vpl:.2f} * {factor_ap:.6f} = R$ {vaue:.2f}\n\n")
        steps.append(f"Conclusão: O projeto é {'viável' if vpl > 0 else 'inviável'} (VPL {'>' if vpl>0 else '<='} 0).\n")

        self.invest_result.append("".join(steps))

    except Exception as e:
        self.invest_result.append(f"Erro: {e}")
