from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def calculate_investment(self):
    try:
        tr = QCoreApplication.translate

        analysis_type = self.invest_analysis_type.currentIndex()
        # 0 = VPL/VAUE Uniforme, 1 = VPL Detalhado, 2 = Payback Descontado, 3 = Análise de Sensibilidade

        # Validação de campos obrigatórios
        if not self.invest_initial.text().strip():
            self.invest_result.append(tr("App", "Erro: Investimento Inicial é obrigatório"))
            return

        if not self.invest_n.text().strip():
            self.invest_result.append(tr("App", "Erro: Número de Períodos é obrigatório"))
            return

        if not self.invest_tma.text().strip():
            self.invest_result.append(tr("App", "Erro: TMA é obrigatória"))
            return

        if analysis_type == 0:  # VPL/VAUE Uniforme
            if not self.invest_cashflow.text().strip():
                self.invest_result.append(tr("App", "Erro: Fluxo de Caixa é obrigatório"))
                return

            _calculate_vpl_vaue_uniform(self)

        elif analysis_type == 1:  # VPL Detalhado
            if not self.invest_annual_revenue.text().strip():
                self.invest_result.append(tr("App", "Erro: Receita Anual é obrigatória"))
                return

            if not self.invest_annual_cost.text().strip():
                self.invest_result.append(tr("App", "Erro: Custo Anual é obrigatório"))
                return

            _calculate_vpl_detailed(self)

        elif analysis_type == 2:  # Payback Descontado
            if not self.invest_cashflow.text().strip():
                self.invest_result.append(tr("App", "Erro: Fluxo de Caixa é obrigatório"))
                return

            _calculate_payback_discounted(self)

        else:  # analysis_type == 3 - Análise de Sensibilidade
            if not self.invest_annual_revenue.text().strip():
                self.invest_result.append(tr("App", "Erro: Receita Anual é obrigatória"))
                return

            if not self.invest_annual_cost.text().strip():
                self.invest_result.append(tr("App", "Erro: Custo Anual é obrigatório"))
                return

            if not self.invest_sensitivity_variation.text().strip():
                self.invest_result.append(tr("App", "Erro: Variação Percentual é obrigatória"))
                return

            _calculate_sensitivity_analysis(self)

    except Exception as e:
        logger.error(f"Erro ao calcular investimento: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.invest_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass

def _calculate_vpl_vaue_uniform(self):
    tr = QCoreApplication.translate
    inv_inicial = self.get_float_from_line_edit(self.invest_initial)
    a = self.get_float_from_line_edit(self.invest_cashflow)
    n = self.get_float_from_line_edit(self.invest_n)
    tma = self.get_float_from_line_edit(self.invest_tma, is_percentage=True)

    def format_currency(value, decimals=2):
        s = f"{value:,.{decimals}f}"
        s = s.replace(",", "T")
        s = s.replace(".", ",")
        s = s.replace("T", ".")
        return s

    def to_superscript(num):
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
            '.': '·', '-': '⁻'
        }
        return ''.join(superscript_map.get(c, c) for c in str(num))

    def format_fraction(numer_str, denom_str, prefix=""):
        numer = str(numer_str)
        denom = str(denom_str)
        width = max(len(numer), len(denom), 3)
        pad = " " * len(prefix)
        numer_line = pad + numer.center(width)
        divider_line = prefix + "─" * width
        denom_line = pad + denom.center(width)
        return numer_line, divider_line, denom_line

    pow_val = (1 + tma) ** n
    num_pa = pow_val - 1
    den_pa = tma * pow_val
    factor_pa = num_pa / den_pa
    vpb = a * factor_pa
    vpl = vpb - inv_inicial

    num_ap = tma * pow_val
    den_ap = pow_val - 1
    factor_ap = num_ap / den_ap
    vaue = vpl * factor_ap

    steps = []
    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "ANÁLISE DE INVESTIMENTOS - VPL E VAUE") + "\n")
    steps.append("═" * 60 + "\n\n")

    steps.append(tr("App", "Dados do problema:") + "\n")
    steps.append(f"  {tr('App', 'Investimento Inicial')}   = R$ {format_currency(inv_inicial)}\n")
    steps.append(f"  {tr('App', 'Fluxo de Caixa')} (A)     = R$ {format_currency(a)} {tr('App', 'por período')}\n")
    steps.append(f"  {tr('App', 'Períodos')} (n)           = {format_currency(n)}\n")
    steps.append(f"  TMA                    = {format_currency(tma*100)}% {tr('App', 'ao período')}\n\n")

    n_super = to_superscript(int(n))

    steps.append("─" * 60 + "\n")
    steps.append(f"1. {tr('App', 'CÁLCULO DO VPB (Valor Presente dos Benefícios)')}\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    f1, f2, f3 = format_fraction("(1 + TMA)ⁿ - 1", "TMA × (1 + TMA)ⁿ", prefix="  VPB = A × ")
    steps.append(f1 + "\n")
    steps.append(f2 + "\n")
    steps.append(f3 + "\n\n")

    steps.append(tr("App", "Cálculo do fator (P/A):") + "\n")
    steps.append(f"  (1 + TMA)ⁿ = (1 + {format_currency(tma)}){n_super}\n")
    steps.append(f"  (1 + TMA)ⁿ = {format_currency(pow_val)}\n\n")

    steps.append(f"  {tr('App', 'Numerador')}   = (1+TMA)ⁿ - 1 = {format_currency(pow_val)} - 1 = {format_currency(num_pa)}\n")
    steps.append(f"  {tr('App', 'Denominador')} = TMA × (1+TMA)ⁿ = {format_currency(tma)} × {format_currency(pow_val)} = {format_currency(den_pa)}\n")
    nf1, nf2, nf3 = format_fraction(format_currency(num_pa), format_currency(den_pa), prefix=f"  {tr('App', 'Fator')} (P/A) = ")
    steps.append(nf1 + "\n")
    steps.append(nf2 + "\n")
    steps.append(nf3 + f" = {format_currency(factor_pa)}\n\n")

    steps.append(tr("App", "Cálculo do VPB:") + "\n")
    steps.append(f"  VPB = A × {tr('App', 'Fator')}(P/A)\n")
    steps.append(f"  VPB = {format_currency(a)} × {format_currency(factor_pa)}\n")
    steps.append(f"  VPB = R$ {format_currency(vpb)}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(f"2. {tr('App', 'CÁLCULO DO VPL (Valor Presente Líquido)')}\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    steps.append("  VPL = VPB - VPC\n")
    steps.append(f"  VPC = {tr('App', 'Investimento Inicial')}\n\n")

    steps.append(tr("App", "Cálculo:") + "\n")
    steps.append(f"  VPC = R$ {format_currency(inv_inicial)}\n")
    steps.append(f"  VPL = {format_currency(vpb)} - {format_currency(inv_inicial)}\n")
    steps.append(f"  VPL = R$ {format_currency(vpl)}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(f"3. {tr('App', 'CÁLCULO DA VAUE (Valor Anual Uniforme Equivalente)')}\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    steps.append(f"  VAUE = VPL × {tr('App', 'Fator')}(A/P)\n\n")

    steps.append(tr("App", "Cálculo do fator (A/P):") + "\n")
    steps.append(f"  {tr('App', 'Numerador')}   = TMA × (1+TMA)ⁿ = {format_currency(tma)} × {format_currency(pow_val)} = {format_currency(num_ap)}\n")
    steps.append(f"  {tr('App', 'Denominador')} = (1+TMA)ⁿ - 1 = {format_currency(pow_val)} - 1 = {format_currency(den_ap)}\n")
    af1, af2, af3 = format_fraction(format_currency(num_ap), format_currency(den_ap), prefix=f"  {tr('App', 'Fator')} (A/P) = ")
    steps.append(af1 + "\n")
    steps.append(af2 + "\n")
    steps.append(af3 + f" = {format_currency(factor_ap)}\n\n")

    steps.append(tr("App", "Cálculo da VAUE:") + "\n")
    steps.append(f"  VAUE = {format_currency(vpl)} × {format_currency(factor_ap)}\n")
    steps.append(f"  VAUE = R$ {format_currency(vaue)}\n\n")

    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "CONCLUSÃO") + "\n")
    steps.append("═" * 60 + "\n\n")

    if vpl > 0:
        steps.append(f"  VPL = R$ {format_currency(vpl)} > 0\n")
        steps.append(f"  VAUE = R$ {format_currency(vaue)} > 0\n\n")
        steps.append(f"  ✓ {tr('App', 'O projeto é VIÁVEL economicamente')}\n")
        steps.append(f"  ✓ {tr('App', 'O investimento proporciona retorno acima da TMA')}\n")

    elif vpl < 0:
        steps.append(f"  VPL = R$ {format_currency(vpl)} < 0\n")
        steps.append(f"  VAUE = R$ {format_currency(vaue)} < 0\n\n")
        steps.append(f"  ✗ {tr('App', 'O projeto é INVIÁVEL economicamente')}\n")
        steps.append(f"  ✗ {tr('App', 'O investimento não atinge a TMA desejada')}\n")

    else:
        steps.append(f"  VPL = R$ {format_currency(vpl)} = 0\n")
        steps.append(f"  VAUE = R$ {format_currency(vaue)} = 0\n\n")
        steps.append(f"  ~ {tr('App', 'O projeto está no limite de viabilidade')}\n")
        steps.append(f"  ~ {tr('App', 'O investimento retorna exatamente a TMA')}\n")

    steps.append("\n" + "─" * 60 + "\n")

    self.invest_result.append("".join(steps))

def _calculate_vpl_detailed(self):
    tr = QCoreApplication.translate
    inv_inicial = self.get_float_from_line_edit(self.invest_initial)
    receita_anual = self.get_float_from_line_edit(self.invest_annual_revenue)
    custo_anual = self.get_float_from_line_edit(self.invest_annual_cost)
    n = int(self.get_float_from_line_edit(self.invest_n))
    tma = self.get_float_from_line_edit(self.invest_tma, is_percentage=True)

    def format_currency(value, decimals=2):
        s = f"{value:,.{decimals}f}"
        s = s.replace(",", "T")
        s = s.replace(".", ",")
        s = s.replace("T", ".")
        return s

    def to_superscript(num):
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
            '.': '·', '-': '⁻'
        }
        return ''.join(superscript_map.get(c, c) for c in str(num))

    def format_fraction(numer_str, denom_str, prefix=""):
        numer = str(numer_str)
        denom = str(denom_str)
        width = max(len(numer), len(denom), 3)
        pad = " " * len(prefix)
        numer_line = pad + numer.center(width)
        divider_line = prefix + "─" * width
        denom_line = pad + denom.center(width)
        return numer_line, divider_line, denom_line

    fluxo_liquido = receita_anual - custo_anual

    pow_val = (1 + tma) ** n
    num_pa = pow_val - 1
    den_pa = tma * pow_val
    factor_pa = num_pa / den_pa

    vpb = fluxo_liquido * factor_pa
    vpl = vpb - inv_inicial

    steps = []
    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "VPL DETALHADO (RECEITAS E CUSTOS SEPARADOS)") + "\n")
    steps.append("═" * 60 + "\n\n")

    steps.append(tr("App", "Dados do problema:") + "\n")
    steps.append(f"  {tr('App', 'Investimento Inicial (C₀)')}: R$ {format_currency(inv_inicial)}\n")
    steps.append(f"  {tr('App', 'Receita Anual')}:            R$ {format_currency(receita_anual)}\n")
    steps.append(f"  {tr('App', 'Custo/Desembolso Anual')}:   R$ {format_currency(custo_anual)}\n")
    steps.append(f"  {tr('App', 'Fluxo Líquido Anual (A)')}:  R$ {format_currency(fluxo_liquido)}\n")
    steps.append(f"  {tr('App', 'Períodos')} (n):             {n}\n")
    steps.append(f"  TMA:                        {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}\n\n")

    n_super = to_superscript(int(n))

    steps.append("─" * 60 + "\n")
    steps.append(f"1. {tr('App', 'CÁLCULO DO FLUXO LÍQUIDO')}\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(f"  A = {tr('App', 'Receita')} - {tr('App', 'Custo')}\n")
    steps.append(f"  A = {format_currency(receita_anual)} - {format_currency(custo_anual)}\n")
    steps.append(f"  A = R$ {format_currency(fluxo_liquido)}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(f"2. {tr('App', 'CÁLCULO DO FATOR (P/A)')}\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    f1, f2, f3 = format_fraction("(1 + i)ⁿ - 1", "i × (1 + i)ⁿ", prefix="  (P/A; i; n) = ")
    steps.append(f1 + "\n")
    steps.append(f2 + "\n")
    steps.append(f3 + "\n\n")

    steps.append(tr("App", "Cálculo:") + "\n")
    steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(tma, 6)}){n_super}\n")
    steps.append(f"  (1 + i)ⁿ = {format_currency(pow_val, 6)}\n\n")

    steps.append(f"  {tr('App', 'Numerador')}   = (1+i)ⁿ - 1\n")
    steps.append(f"                = {format_currency(pow_val, 6)} - 1\n")
    steps.append(f"                = {format_currency(num_pa, 6)}\n\n")

    steps.append(f"  {tr('App', 'Denominador')} = i × (1+i)ⁿ\n")
    steps.append(f"                = {format_currency(tma, 6)} × {format_currency(pow_val, 6)}\n")
    steps.append(f"                = {format_currency(den_pa, 6)}\n\n")

    nf1, nf2, nf3 = format_fraction(format_currency(num_pa, 6), format_currency(den_pa, 6), prefix="  (P/A; 12%; 5) = ")
    steps.append(nf1 + "\n")
    steps.append(nf2 + "\n")
    steps.append(nf3 + f" = {format_currency(factor_pa, 6)}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(f"3. {tr('App', 'CÁLCULO DO VPB (Valor Presente dos Benefícios)')}\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(f"  VPB = A × (P/A; i; n)\n")
    steps.append(f"  VPB = {format_currency(fluxo_liquido)} × {format_currency(factor_pa, 6)}\n")
    steps.append(f"  VPB = R$ {format_currency(vpb)}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(f"4. {tr('App', 'CÁLCULO DO VPL (Valor Presente Líquido)')}\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    steps.append("  VPL = VPB - VPC\n")
    steps.append(f"  VPL = VPB - C₀\n\n")

    steps.append(tr("App", "Cálculo:") + "\n")
    steps.append(f"  VPL = {format_currency(vpb)} - {format_currency(inv_inicial)}\n")
    steps.append(f"  VPL = R$ {format_currency(vpl)}\n\n")

    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "RESPOSTA:") + "\n")
    steps.append(f"  {tr('App', 'O Valor Presente Líquido é de')} R$ {format_currency(vpl, 2)}\n")
    steps.append("═" * 60 + "\n")

    self.invest_result.append("".join(steps))

def _calculate_payback_discounted(self):
    tr = QCoreApplication.translate
    inv_inicial = self.get_float_from_line_edit(self.invest_initial)
    fluxo_anual = self.get_float_from_line_edit(self.invest_cashflow)
    n_max = int(self.get_float_from_line_edit(self.invest_n))
    tma = self.get_float_from_line_edit(self.invest_tma, is_percentage=True)

    def format_currency(value, decimals=2):
        s = f"{value:,.{decimals}f}"
        s = s.replace(",", "T")
        s = s.replace(".", ",")
        s = s.replace("T", ".")
        return s

    def to_superscript(num):
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
            '.': '·', '-': '⁻'
        }
        return ''.join(superscript_map.get(c, c) for c in str(num))

    steps = []
    steps.append("═" * 60 + "\n")
    steps.append(tr("App", "PAYBACK DESCONTADO (PERÍODO DE RECUPERAÇÃO)") + "\n")
    steps.append("═" * 60 + "\n\n")

    steps.append(tr("App", "Dados do problema:") + "\n")
    steps.append(f"  {tr('App', 'Investimento Inicial (C₀)')}: R$ {format_currency(inv_inicial)}\n")
    steps.append(f"  {tr('App', 'Fluxo de Caixa Anual (A)')}: R$ {format_currency(fluxo_anual)}\n")
    steps.append(f"  TMA:                         {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}\n")
    steps.append(f"  {tr('App', 'Período máximo analisado')}:  {n_max} {tr('App', 'anos')}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(tr("App", "OBJETIVO:") + "\n")
    steps.append("─" * 60 + "\n\n")

    target = inv_inicial / fluxo_anual
    steps.append(f"  {tr('App', 'Encontrar k tal que')}: A × (P/A; i; k) ≥ C₀\n")
    steps.append(f"  {tr('App', 'Ou seja')}: (P/A; i; k) ≥ {format_currency(inv_inicial)} / {format_currency(fluxo_anual)}\n")
    steps.append(f"  (P/A; i; k) ≥ {format_currency(target, 6)}\n\n")

    steps.append("─" * 60 + "\n")
    steps.append(tr("App", "CÁLCULO DOS FATORES (P/A) E VP ACUMULADO:") + "\n")
    steps.append("─" * 60 + "\n\n")

    steps.append(f"{'Ano':<6} {'(P/F)':<12} {'VP Anual':<15} {'VP Acum.':<15} {'(P/A)':<12}\n")
    steps.append("─" * 60 + "\n")

    vp_acumulado = 0
    payback_year = None

    for k in range(1, n_max + 1):
        # Fator (P/F; i; k) = 1 / (1+i)^k
        factor_pf = 1 / ((1 + tma) ** k)
        vp_anual = fluxo_anual * factor_pf
        vp_acumulado += vp_anual

        # Fator (P/A; i; k) acumulado
        factor_pa_k = vp_acumulado / fluxo_anual

        steps.append(f"{k:<6} {format_currency(factor_pf, 6):<12} R$ {format_currency(vp_anual):<13} R$ {format_currency(vp_acumulado):<13} {format_currency(factor_pa_k, 6):<12}\n")

        if payback_year is None and vp_acumulado >= inv_inicial:
            payback_year = k

    steps.append("\n")
    steps.append("─" * 60 + "\n")
    steps.append(tr("App", "ANÁLISE:") + "\n")
    steps.append("─" * 60 + "\n\n")

    if payback_year:
        vp_ano_anterior = 0
        for k in range(1, payback_year):
            factor_pf = 1 / ((1 + tma) ** k)
            vp_ano_anterior += fluxo_anual * factor_pf

        vp_ano_payback = 0
        for k in range(1, payback_year + 1):
            factor_pf = 1 / ((1 + tma) ** k)
            vp_ano_payback += fluxo_anual * factor_pf

        steps.append(f"  {tr('App', 'Investimento inicial')}: R$ {format_currency(inv_inicial)}\n\n")
        
        if payback_year > 1:
            steps.append(f"  {tr('App', 'VP acumulado até ano')} {payback_year-1}: R$ {format_currency(vp_ano_anterior)}\n")

        steps.append(f"  {tr('App', 'VP acumulado até ano')} {payback_year}: R$ {format_currency(vp_ano_payback)}\n\n")
        steps.append(f"  {tr('App', 'O investimento é recuperado durante o ano')} {payback_year}.\n\n")

        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "RESPOSTA:") + "\n")
        steps.append(f"  {tr('App', 'Payback Descontado')}: {payback_year} {tr('App', 'anos')}\n")
        steps.append("═" * 60 + "\n")

    else:
        steps.append(f"  {tr('App', 'O investimento NÃO é recuperado em')} {n_max} {tr('App', 'anos')}.\n")
        steps.append(f"  {tr('App', 'VP acumulado máximo')}: R$ {format_currency(vp_acumulado)}\n")
        steps.append(f"  {tr('App', 'Investimento inicial')}: R$ {format_currency(inv_inicial)}\n\n")

        steps.append("═" * 60 + "\n")
        steps.append(tr("App", "RESPOSTA:") + "\n")
        steps.append(f"  {tr('App', 'Payback Descontado: Não recuperado em')} {n_max} {tr('App', 'anos')}\n")
        steps.append("═" * 60 + "\n")

    self.invest_result.append("".join(steps))

def _calculate_sensitivity_analysis(self):
    tr = QCoreApplication.translate
    inv_inicial = self.get_float_from_line_edit(self.invest_initial)
    receita_base = self.get_float_from_line_edit(self.invest_annual_revenue)
    custo_anual = self.get_float_from_line_edit(self.invest_annual_cost)
    n = int(self.get_float_from_line_edit(self.invest_n))
    tma = self.get_float_from_line_edit(self.invest_tma, is_percentage=True)
    variacao_percentual = self.get_float_from_line_edit(self.invest_sensitivity_variation, is_percentage=True)

    def format_currency(value, decimals=2):
        s = f"{value:,.{decimals}f}"
        s = s.replace(",", "T")
        s = s.replace(".", ",")
        s = s.replace("T", ".")
        return s

    def to_superscript(num):
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
            '.': '·', '-': '⁻'
        }
        return ''.join(superscript_map.get(c, c) for c in str(num))

    def format_fraction(numer_str, denom_str, prefix=""):
        numer = str(numer_str)
        denom = str(denom_str)
        width = max(len(numer), len(denom), 3)
        pad = " " * len(prefix)
        numer_line = pad + numer.center(width)
        divider_line = prefix + "─" * width
        denom_line = pad + denom.center(width)
        return numer_line, divider_line, denom_line

    # Cálculo do VPL Base
    fluxo_base = receita_base - custo_anual
    pow_val = (1 + tma) ** n
    num_pa = pow_val - 1
    den_pa = tma * pow_val
    factor_pa = num_pa / den_pa
    vpb_base = fluxo_base * factor_pa
    vpl_base = vpb_base - inv_inicial

    # Cálculo do VPL com Variação
    receita_nova = receita_base * (1 + variacao_percentual)
    fluxo_novo = receita_nova - custo_anual
    vpb_novo = fluxo_novo * factor_pa
    vpl_novo = vpb_novo - inv_inicial

    # Variação Percentual do VPL
    variacao_vpl = ((vpl_novo - vpl_base) / vpl_base) * 100

    steps = []
    steps.append("═" * 70 + "\n")
    steps.append(tr("App", "ANÁLISE DE SENSIBILIDADE DO VPL") + "\n")
    steps.append("═" * 70 + "\n\n")

    steps.append(tr("App", "Dados do problema:") + "\n")
    steps.append(f"  {tr('App', 'Investimento Inicial (C₀)')}: R$ {format_currency(inv_inicial)}\n")
    steps.append(f"  {tr('App', 'Receita Anual Base')}:       R$ {format_currency(receita_base)}\n")
    steps.append(f"  {tr('App', 'Custo Anual')}:              R$ {format_currency(custo_anual)}\n")
    steps.append(f"  {tr('App', 'Fluxo Líquido Base (A)')}:   R$ {format_currency(fluxo_base)}\n")
    steps.append(f"  {tr('App', 'Períodos')} (n):             {n} {tr('App', 'anos')}\n")
    steps.append(f"  TMA (i):                     {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}\n")
    steps.append(f"  {tr('App', 'Variação na Receita')}:      {format_currency(variacao_percentual*100, 2)}%\n\n")

    n_super = to_superscript(int(n))

    steps.append("─" * 70 + "\n")
    steps.append(f"1. {tr('App', 'CÁLCULO DO FATOR (P/A)')}\n")
    steps.append("─" * 70 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    f1, f2, f3 = format_fraction("(1 + i)ⁿ - 1", "i × (1 + i)ⁿ", prefix="  (P/A; i; n) = ")
    steps.append(f1 + "\n")
    steps.append(f2 + "\n")
    steps.append(f3 + "\n\n")

    steps.append(tr("App", "Cálculo:") + "\n")
    steps.append(f"  (1 + i)ⁿ = (1 + {format_currency(tma, 6)}){n_super}\n")
    steps.append(f"  (1 + i)ⁿ = {format_currency(pow_val, 6)}\n\n")

    steps.append(f"  {tr('App', 'Numerador')}   = (1+i)ⁿ - 1 = {format_currency(pow_val, 6)} - 1\n")
    steps.append(f"                = {format_currency(num_pa, 6)}\n\n")

    steps.append(f"  {tr('App', 'Denominador')} = i × (1+i)ⁿ = {format_currency(tma, 6)} × {format_currency(pow_val, 6)}\n")
    steps.append(f"                = {format_currency(den_pa, 6)}\n\n")

    nf1, nf2, nf3 = format_fraction(format_currency(num_pa, 6), format_currency(den_pa, 6), prefix=f"  (P/A; {format_currency(tma*100)}%; {n}) = ")
    steps.append(nf1 + "\n")
    steps.append(nf2 + "\n")
    steps.append(nf3 + f" = {format_currency(factor_pa, 6)}\n\n")

    steps.append("─" * 70 + "\n")
    steps.append(f"2. {tr('App', 'CÁLCULO DO VPL BASE (CENÁRIO ORIGINAL)')}\n")
    steps.append("─" * 70 + "\n\n")

    steps.append(f"  {tr('App', 'Fluxo Líquido Base')} = {tr('App', 'Receita')} - {tr('App', 'Custo')}\n")
    steps.append(f"  A_base = {format_currency(receita_base)} - {format_currency(custo_anual)}\n")
    steps.append(f"  A_base = R$ {format_currency(fluxo_base)}\n\n")

    steps.append(f"  VPB_base = A_base × (P/A; i; n)\n")
    steps.append(f"  VPB_base = {format_currency(fluxo_base)} × {format_currency(factor_pa, 6)}\n")
    steps.append(f"  VPB_base = R$ {format_currency(vpb_base)}\n\n")

    steps.append(f"  VPL_base = VPB_base - C₀\n")
    steps.append(f"  VPL_base = {format_currency(vpb_base)} - {format_currency(inv_inicial)}\n")
    steps.append(f"  VPL_base = R$ {format_currency(vpl_base)}\n\n")

    steps.append("─" * 70 + "\n")
    steps.append(f"3. {tr('App', 'CÁLCULO DO VPL COM VARIAÇÃO NA RECEITA')}\n")
    steps.append("─" * 70 + "\n\n")

    sinal = "+" if variacao_percentual >= 0 else ""
    steps.append(f"  {tr('App', 'Variação aplicada')}: {sinal}{format_currency(variacao_percentual*100, 2)}%\n\n")

    steps.append(f"  {tr('App', 'Nova Receita')} = {tr('App', 'Receita Base')} × (1 {sinal} {format_currency(abs(variacao_percentual), 6)})\n")
    steps.append(f"  {tr('App', 'Nova Receita')} = {format_currency(receita_base)} × {format_currency(1 + variacao_percentual, 6)}\n")
    steps.append(f"  {tr('App', 'Nova Receita')} = R$ {format_currency(receita_nova)}\n\n")

    steps.append(f"  {tr('App', 'Novo Fluxo Líquido')} = {tr('App', 'Nova Receita')} - {tr('App', 'Custo')}\n")
    steps.append(f"  A_novo = {format_currency(receita_nova)} - {format_currency(custo_anual)}\n")
    steps.append(f"  A_novo = R$ {format_currency(fluxo_novo)}\n\n")

    steps.append(f"  VPB_novo = A_novo × (P/A; i; n)\n")
    steps.append(f"  VPB_novo = {format_currency(fluxo_novo)} × {format_currency(factor_pa, 6)}\n")
    steps.append(f"  VPB_novo = R$ {format_currency(vpb_novo)}\n\n")

    steps.append(f"  VPL_novo = VPB_novo - C₀\n")
    steps.append(f"  VPL_novo = {format_currency(vpb_novo)} - {format_currency(inv_inicial)}\n")
    steps.append(f"  VPL_novo = R$ {format_currency(vpl_novo)}\n\n")

    steps.append("─" * 70 + "\n")
    steps.append(f"4. {tr('App', 'CÁLCULO DA VARIAÇÃO PERCENTUAL DO VPL')}\n")
    steps.append("─" * 70 + "\n\n")

    steps.append(tr("App", "Fórmula:") + "\n")
    vf1, vf2, vf3 = format_fraction("VPL_novo - VPL_base", "VPL_base", prefix="  Variação % = ")
    steps.append(vf1 + " × 100\n")
    steps.append(vf2 + "\n")
    steps.append(vf3 + "\n\n")

    diff_vpl = vpl_novo - vpl_base
    steps.append(tr("App", "Cálculo:") + "\n")
    steps.append(f"  {tr('App', 'Numerador')}   = VPL_novo - VPL_base\n")
    steps.append(f"                = {format_currency(vpl_novo)} - {format_currency(vpl_base)}\n")
    steps.append(f"                = R$ {format_currency(diff_vpl)}\n\n")

    steps.append(f"  {tr('App', 'Denominador')} = VPL_base\n")
    steps.append(f"                = R$ {format_currency(vpl_base)}\n\n")

    varf1, varf2, varf3 = format_fraction(format_currency(diff_vpl), format_currency(vpl_base), prefix="  Variação % = ")
    steps.append(varf1 + " × 100\n")
    steps.append(varf2 + "\n")
    steps.append(varf3 + "\n\n")

    steps.append(f"  Variação % = {format_currency(diff_vpl / vpl_base, 6)} × 100\n")
    steps.append(f"  Variação % = {format_currency(variacao_vpl, 2)}%\n\n")

    steps.append("═" * 70 + "\n")
    steps.append(tr("App", "RESUMO DA ANÁLISE DE SENSIBILIDADE") + "\n")
    steps.append("═" * 70 + "\n\n")

    steps.append(f"  VPL_base = R$ {format_currency(vpl_base)}\n")
    steps.append(f"  VPL_novo = R$ {format_currency(vpl_novo)}\n")
    steps.append(f"  {tr('App', 'Variação do VPL')} = R$ {format_currency(diff_vpl)}\n")
    steps.append(f"  {tr('App', 'Variação Percentual')} = {format_currency(variacao_vpl, 2)}%\n\n")

    if variacao_vpl > 0:
        steps.append(f"  ✓ {tr('App', 'O VPL aumentou com a variação na receita')}\n")

    elif variacao_vpl < 0:
        steps.append(f"  ✗ {tr('App', 'O VPL diminuiu com a variação na receita')}\n")

    else:
        steps.append(f"  = {tr('App', 'O VPL permaneceu inalterado')}\n")

    steps.append("\n" + "═" * 70 + "\n")
    steps.append(tr("App", "RESPOSTA:") + "\n")
    steps.append(f"  {tr('App', 'A respectiva variação percentual do Valor Presente Líquido é de')}\n")
    steps.append(f"  {format_currency(variacao_vpl, 2)}%\n")
    steps.append("═" * 70 + "\n")

    self.invest_result.append("".join(steps))
