from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager
from utils.TextFormat import format_currency, to_subscript, to_superscript, format_fraction

logger = LogManager.get_logger()

def calculate_vpl_with_taxes(self):
    try:
        tr = QCoreApplication.translate

        # Ler dados de entrada
        investimento = self.get_float_from_line_edit(self.vpl_tax_investment)
        lucro_anual = self.get_float_from_line_edit(self.vpl_tax_annual_profit)
        vida_util = int(self.get_float_from_line_edit(self.vpl_tax_useful_life))
        taxa_irpj = self.get_float_from_line_edit(self.vpl_tax_irpj, is_percentage=True)
        taxa_csll = self.get_float_from_line_edit(self.vpl_tax_csll, is_percentage=True)
        tma = self.get_float_from_line_edit(self.vpl_tax_tma, is_percentage=True)

        # Campos opcionais
        valor_residual = self.get_float_from_line_edit(self.vpl_tax_residual_value, default=0.0)
        ano_venda = int(self.get_float_from_line_edit(self.vpl_tax_sale_year, default=vida_util))
        valor_venda = self.get_float_from_line_edit(self.vpl_tax_sale_value, default=0.0)

        # Campos de financiamento
        financiado = self.vpl_tax_financed.isChecked()
        taxa_financiamento = 0.0
        n_parcelas = 0

        if financiado:
            taxa_financiamento = self.get_float_from_line_edit(self.vpl_tax_finance_rate, is_percentage=True)
            n_parcelas = int(self.get_float_from_line_edit(self.vpl_tax_finance_periods))

        # Validações
        if ano_venda > vida_util:
            self.vpl_tax_result.append(tr("App", "Erro: Ano de venda não pode ser maior que a vida útil"))
            return

        if financiado and n_parcelas <= 0:
            self.vpl_tax_result.append(tr("App", "Erro: Número de parcelas deve ser maior que zero"))
            return

        taxa_imposto_total = taxa_irpj + taxa_csll

        # Depreciação contábil linear
        dc_anual = (investimento - valor_residual) / vida_util

        steps = []
        steps.append("═" * 120 + "\n")
        steps.append(tr("App", "VPL COM IMPOSTOS, DEPRECIAÇÃO E FINANCIAMENTO") + "\n")
        steps.append("═" * 120 + "\n\n")

        steps.append(tr("App", "DADOS DO PROBLEMA:") + "\n")
        steps.append("─" * 120 + "\n")
        steps.append(f"  • {tr('App', 'Investimento inicial')}: R$ {format_currency(investimento)}\n")
        steps.append(f"  • {tr('App', 'Lucro antes impostos e juros')}: R$ {format_currency(lucro_anual)} {tr('App', 'por ano')}\n")
        steps.append(f"  • {tr('App', 'Vida útil para depreciação')}: {vida_util} {tr('App', 'anos')}\n")
        steps.append(f"  • {tr('App', 'Valor residual')}: R$ {format_currency(valor_residual)}\n")
        steps.append(f"  • IRPJ: {format_currency(taxa_irpj*100, 2)}%\n")
        steps.append(f"  • CSLL: {format_currency(taxa_csll*100, 2)}%\n")
        steps.append(f"  • {tr('App', 'Imposto total')} (IRPJ+CSLL): {format_currency(taxa_imposto_total*100, 2)}%\n")
        steps.append(f"  • TMA: {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}\n")

        if financiado:
            steps.append(f"  • {tr('App', 'Forma de pagamento')}: {tr('App', 'Financiamento pelo Sistema SAC')}\n")
            steps.append(f"  • {tr('App', 'Taxa de juros do financiamento')}: {format_currency(taxa_financiamento*100, 2)}% {tr('App', 'ao ano')}\n")
            steps.append(f"  • {tr('App', 'Número de parcelas')}: {n_parcelas} {tr('App', 'anos')}\n")

        else:
            steps.append(f"  • {tr('App', 'Forma de pagamento')}: {tr('App', 'À vista')}\n")

        if valor_venda > 0:
            steps.append(f"  • {tr('App', 'Venda no ano')}: {ano_venda}\n")
            steps.append(f"  • {tr('App', 'Valor de venda')}: R$ {format_currency(valor_venda)}\n")

        steps.append("\n")

        # ETAPA 1: Depreciação
        steps.append("═" * 120 + "\n")
        steps.append(f"ETAPA 1: {tr('App', 'CÁLCULO DA DEPRECIAÇÃO CONTÁBIL ANUAL')}\n")
        steps.append("═" * 120 + "\n\n")

        steps.append(tr("App", "A depreciação contábil (DC) é calculada pelo método linear:") + "\n\n")
        steps.append("  Fórmula: DC = (Valor de Aquisição - Valor Residual) / Vida Útil\n\n")

        f1, f2, f3 = format_fraction(
            f"{format_currency(investimento)} - {format_currency(valor_residual)}", 
            str(vida_util), 
            prefix="  DC = "
        )
        steps.append(f1 + "\n")
        steps.append(f2 + "\n")
        steps.append(f3 + "\n\n")

        steps.append(f"  DC = {format_currency(investimento - valor_residual)} / {vida_util}\n")
        steps.append(f"  DC = R$ {format_currency(dc_anual)} {tr('App', 'por ano')}\n\n")

        steps.append(tr("App", "A depreciação contábil é dedutível da base tributável.") + "\n\n")

        # ETAPA 2: Tabela de financiamento (se aplicável)
        amortizacao_dados = []
        if financiado:
            steps.append("═" * 120 + "\n")
            steps.append(f"ETAPA 2: {tr('App', 'TABELA DE AMORTIZAÇÃO PELO SISTEMA SAC (Sistema de Amortização Constante)')}\n")
            steps.append("═" * 120 + "\n\n")

            steps.append(tr("App", "No Sistema SAC, a amortização é constante em todos os períodos:") + "\n\n")
            steps.append("  Fórmula: a = P / n\n\n")

            amortizacao_constante = investimento / n_parcelas

            f1, f2, f3 = format_fraction(format_currency(investimento), str(n_parcelas), prefix="  a = ")
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n\n")

            steps.append(f"  {tr('App', 'Amortização constante')}: a = R$ {format_currency(amortizacao_constante)}\n\n")

            steps.append(tr("App", "Os juros de cada período são calculados sobre o saldo devedor do período anterior:") + "\n")
            steps.append("  j(k) = i × SD(k-1)\n\n")
            steps.append(tr("App", "A prestação é a soma da amortização constante com os juros:") + "\n")
            steps.append("  p(k) = a + j(k)\n\n")

            # Cabeçalho
            steps.append(f"{'Ano':>4} | {'Saldo Inicial':>18} | {'Juros':>15} | {'Amortização':>15} | {'Prestação':>15} | {'Saldo Final':>18}\n")
            steps.append("─" * 110 + "\n")

            saldo_devedor = investimento
            steps.append(f"{0:4} | {format_currency(saldo_devedor):>18} | {'-':>15} | {'-':>15} | {'-':>15} | {format_currency(saldo_devedor):>18}\n")

            for ano in range(1, n_parcelas + 1):
                saldo_inicial = saldo_devedor
                juros = saldo_devedor * taxa_financiamento
                prestacao = amortizacao_constante + juros
                saldo_devedor -= amortizacao_constante

                amortizacao_dados.append({
                    'ano': ano,
                    'prestacao': prestacao,
                    'amortizacao': amortizacao_constante,
                    'juros': juros,
                    'saldo': max(0, saldo_devedor)
                })

                steps.append(f"{ano:4} | {format_currency(saldo_inicial):>18} | {format_currency(juros):>15} | ")
                steps.append(f"{format_currency(amortizacao_constante):>15} | {format_currency(prestacao):>15} | ")
                steps.append(f"{format_currency(max(0, saldo_devedor)):>18}\n")

            steps.append("\n")
            steps.append(tr("App", "Cálculos detalhados por período:") + "\n\n")

            saldo_devedor = investimento
            for ano in range(1, n_parcelas + 1):
                steps.append(f"  {tr('App', 'Ano')} {ano}:\n")
                steps.append(f"    j({ano}) = {format_currency(taxa_financiamento*100, 2)}% × {format_currency(saldo_devedor)} = R$ {format_currency(saldo_devedor * taxa_financiamento)}\n")
                steps.append(f"    p({ano}) = {format_currency(amortizacao_constante)} + {format_currency(saldo_devedor * taxa_financiamento)} = R$ {format_currency(amortizacao_constante + saldo_devedor * taxa_financiamento)}\n")
                saldo_devedor -= amortizacao_constante
                steps.append(f"    SD({ano}) = {format_currency(saldo_devedor + amortizacao_constante)} - {format_currency(amortizacao_constante)} = R$ {format_currency(max(0, saldo_devedor))}\n\n")

            steps.append(tr("App", "IMPORTANTE: Os juros do financiamento são dedutíveis da base tributável.") + "\n\n")

        # ETAPA 3: Tabela de fluxo de caixa
        steps.append("═" * 120 + "\n")
        numero_secao = 3 if financiado else 2
        steps.append(f"ETAPA {numero_secao}: {tr('App', 'CÁLCULO DO FLUXO DE CAIXA COM IMPOSTOS')}\n")
        steps.append("═" * 120 + "\n\n")

        if financiado:
            steps.append(tr("App", "Fórmula da Renda Tributável (com financiamento):") + "\n")
            steps.append("  Renda Tributável = Lucro Bruto - Depreciação Contábil - Juros do Financiamento ± Diferença Contábil\n\n")

        else:
            steps.append(tr("App", "Fórmula da Renda Tributável (sem financiamento):") + "\n")
            steps.append("  Renda Tributável = Lucro Bruto - Depreciação Contábil ± Diferença Contábil\n\n")

        steps.append(tr("App", "Onde:") + "\n")
        steps.append(f"  • {tr('App', 'Diferença Contábil')} = {tr('App', 'Valor de Venda')} - {tr('App', 'Valor Contábil')}\n")
        steps.append(f"  • {tr('App', 'Valor Contábil')} = {tr('App', 'Valor de Aquisição')} - ({tr('App', 'Depreciação Anual')} × {tr('App', 'Anos de Uso')})\n")
        steps.append(f"  • {tr('App', 'Se Diferença Contábil < 0')}: {tr('App', 'Perda de capital (dedutível)')}\n")
        steps.append(f"  • {tr('App', 'Se Diferença Contábil > 0')}: {tr('App', 'Ganho de capital (tributável)')}\n\n")

        steps.append(tr("App", "Cálculo do Imposto:") + "\n")
        steps.append(f"  Imposto = Renda Tributável × {format_currency(taxa_imposto_total*100, 2)}%\n\n")

        if financiado:
            steps.append(tr("App", "Cálculo do Fluxo de Caixa Líquido:") + "\n")
            steps.append("  Fluxo Líquido = Lucro Bruto + Valor de Venda - Imposto - Prestação\n\n")

        else:
            steps.append(tr("App", "Cálculo do Fluxo de Caixa Líquido:") + "\n")
            steps.append("  Fluxo Líquido = Lucro Bruto + Valor de Venda - Imposto\n\n")

        # Cabeçalho da tabela
        steps.append(f"{'Ano':>4} | {'Fluxo Bruto':>13} | {'DC':>10} | {'Juros':>10} | {'Dif.Cont.':>10} | ")
        steps.append(f"{'Renda Trib.':>13} | {'Imposto':>13} | {'Prestação':>13} | {'Fluxo Líq.':>13}\n")
        steps.append("─" * 120 + "\n")

        # Ano 0
        fluxo_ano_0 = 0.0 if financiado else -investimento
        steps.append(f"{0:4} | {format_currency(fluxo_ano_0):>13} | {'-':>10} | {'-':>10} | {'-':>10} | ")
        steps.append(f"{'-':>13} | {'-':>13} | {'-':>13} | {format_currency(fluxo_ano_0):>13}\n")

        fluxos_liquidos = [fluxo_ano_0]

        # Anos 1 até max_anos
        max_anos = max(ano_venda, n_parcelas if financiado else ano_venda)

        for ano in range(1, max_anos + 1):
            fluxo_bruto = lucro_anual if ano <= ano_venda else 0.0
            deprec = dc_anual if ano <= vida_util else 0.0
            juros_financ = amortizacao_dados[ano-1]['juros'] if financiado and ano <= n_parcelas else 0.0
            prestacao = amortizacao_dados[ano-1]['prestacao'] if financiado and ano <= n_parcelas else 0.0
            diferenca_cont = 0.0

            # Venda no último ano
            if ano == ano_venda and valor_venda > 0:
                vc = investimento - (ano * dc_anual)
                diferenca_cont = valor_venda - vc
                fluxo_bruto += valor_venda

            # Lucro tributável
            lucro_tributavel = lucro_anual - deprec - juros_financ + diferenca_cont
            imposto = lucro_tributavel * taxa_imposto_total

            # Fluxo líquido
            fluxo_liquido = fluxo_bruto - imposto - prestacao
            
            fluxos_liquidos.append(fluxo_liquido)

            # Linha da tabela
            juros_str = format_currency(juros_financ) if juros_financ != 0 else '-'
            dif_str = format_currency(diferenca_cont) if diferenca_cont != 0 else '-'
            prest_str = format_currency(prestacao) if prestacao != 0 else '-'

            steps.append(f"{ano:4} | {format_currency(fluxo_bruto):>13} | {format_currency(deprec):>10} | {juros_str:>10} | {dif_str:>10} | ")
            steps.append(f"{format_currency(lucro_tributavel):>13} | {format_currency(imposto):>13} | {prest_str:>13} | {format_currency(fluxo_liquido):>13}\n")

        steps.append("\n")

        # Cálculos detalhados por ano
        steps.append(tr("App", "CÁLCULOS DETALHADOS POR ANO:") + "\n")
        steps.append("─" * 120 + "\n\n")

        if not financiado:
            steps.append(f"  {tr('App', 'Ano')} 0:\n")
            steps.append(f"    {tr('App', 'Investimento inicial pago à vista')}: -R$ {format_currency(investimento)}\n")
            steps.append(f"    {tr('App', 'Fluxo de caixa')}: -R$ {format_currency(investimento)}\n\n")

        else:
            steps.append(f"  {tr('App', 'Ano')} 0:\n")
            steps.append(f"    {tr('App', 'Investimento 100% financiado - sem desembolso inicial')}\n")
            steps.append(f"    {tr('App', 'Fluxo de caixa')}: R$ 0,00\n\n")

        for ano in range(1, max_anos + 1):
            fluxo_bruto = lucro_anual if ano <= ano_venda else 0.0
            deprec = dc_anual if ano <= vida_util else 0.0
            juros_financ = amortizacao_dados[ano-1]['juros'] if financiado and ano <= n_parcelas else 0.0
            prestacao = amortizacao_dados[ano-1]['prestacao'] if financiado and ano <= n_parcelas else 0.0
            diferenca_cont = 0.0
            valor_venda_ano = 0.0

            steps.append(f"  {tr('App', 'Ano')} {ano}:\n")

            # Venda
            if ano == ano_venda and valor_venda > 0:
                vc = investimento - (ano * dc_anual)
                diferenca_cont = valor_venda - vc
                valor_venda_ano = valor_venda
                fluxo_bruto += valor_venda

                steps.append(f"    {tr('App', 'Lucro bruto operacional')}: R$ {format_currency(lucro_anual)}\n")
                steps.append(f"    {tr('App', 'Venda do ativo')}: R$ {format_currency(valor_venda)}\n")
                steps.append(f"    {tr('App', 'Fluxo bruto total')}: R$ {format_currency(fluxo_bruto)}\n\n")

                steps.append(f"    {tr('App', 'Cálculo da Diferença Contábil')}:\n")
                steps.append(f"      {tr('App', 'Valor Contábil')} (VC{to_subscript(str(ano))}): {format_currency(investimento)} - ({ano} × {format_currency(dc_anual)}) = R$ {format_currency(vc)}\n")
                steps.append(f"      {tr('App', 'Diferença Contábil')}: {format_currency(valor_venda)} - {format_currency(vc)} = R$ {format_currency(diferenca_cont)}\n")

                if diferenca_cont < 0:
                    steps.append(f"      → {tr('App', 'Perda de capital de')} R$ {format_currency(abs(diferenca_cont))} ({tr('App', 'dedutível')})\n\n")

                elif diferenca_cont > 0:
                    steps.append(f"      → {tr('App', 'Ganho de capital de')} R$ {format_currency(diferenca_cont)} ({tr('App', 'tributável')})\n\n")

                else:
                    steps.append(f"      → {tr('App', 'Sem ganho ou perda de capital')}\n\n")

            else:
                steps.append(f"    {tr('App', 'Lucro bruto operacional')}: R$ {format_currency(lucro_anual)}\n\n")

            # Renda tributável
            steps.append(f"    {tr('App', 'Cálculo da Renda Tributável')}:\n")
            steps.append(f"      {tr('App', 'Renda Tributável')} = {format_currency(lucro_anual)} - {format_currency(deprec)}")

            if juros_financ > 0:
                steps.append(f" - {format_currency(juros_financ)}")

            if diferenca_cont != 0:
                if diferenca_cont > 0:
                    steps.append(f" + {format_currency(diferenca_cont)}")

                else:
                    steps.append(f" - {format_currency(abs(diferenca_cont))}")

            lucro_tributavel = lucro_anual - deprec - juros_financ + diferenca_cont
            steps.append(f" = R$ {format_currency(lucro_tributavel)}\n\n")

            # Imposto
            imposto = lucro_tributavel * taxa_imposto_total
            steps.append(f"    {tr('App', 'Cálculo do Imposto')}:\n")
            steps.append(f"      {tr('App', 'Imposto')} = {format_currency(lucro_tributavel)} × {format_currency(taxa_imposto_total*100, 2)}% = R$ {format_currency(imposto)}\n\n")

            # Fluxo líquido
            fluxo_liquido = fluxo_bruto - imposto - prestacao
            steps.append(f"    {tr('App', 'Cálculo do Fluxo de Caixa Líquido')}:\n")
            steps.append(f"      {tr('App', 'Fluxo Líquido')} = {format_currency(fluxo_bruto)} - {format_currency(imposto)}")

            if prestacao > 0:
                steps.append(f" - {format_currency(prestacao)}")

            steps.append(f" = R$ {format_currency(fluxo_liquido)}\n\n")

        # ETAPA FINAL: Cálculo do VPL
        steps.append("═" * 120 + "\n")
        numero_secao += 1
        steps.append(f"ETAPA {numero_secao}: {tr('App', 'CÁLCULO DO VALOR PRESENTE LÍQUIDO (VPL)')}\n")
        steps.append("═" * 120 + "\n\n")

        steps.append(tr("App", "Fórmula do VPL:") + "\n\n")
        steps.append("         n    Fluxo(k)\n")
        steps.append("  VPL = Σ  ─────────────\n")
        steps.append("        k=0  (1 + TMA)ᵏ\n\n")

        steps.append(tr("App", "Onde:") + "\n")
        steps.append(f"  • n = {max_anos} ({tr('App', 'número de períodos')})\n")
        steps.append(f"  • TMA = {format_currency(tma*100, 2)}% = {format_currency(tma, 6)} ({tr('App', 'taxa mínima de atratividade')})\n")
        steps.append(f"  • Fluxo(k) = {tr('App', 'Fluxo de caixa líquido no período k')}\n\n")

        steps.append(tr("App", "CÁLCULO DETALHADO DO VPL:") + "\n")
        steps.append("─" * 120 + "\n\n")

        vpl = 0.0

        for ano, fluxo in enumerate(fluxos_liquidos):
            if ano == 0:
                vp = fluxo
                if financiado:
                    steps.append(f"  {tr('App', 'Ano')} {ano}: VP₀ = {format_currency(fluxo):>15} ({tr('App', 'sem desembolso inicial')})\n\n")

                else:
                    steps.append(f"  {tr('App', 'Ano')} {ano}: VP₀ = {format_currency(fluxo):>15} ({tr('App', 'investimento inicial')})\n\n")

            else:
                fator = (1 + tma) ** ano
                vp = fluxo / fator
                steps.append(f"  {tr('App', 'Ano')} {ano}:\n")
                steps.append(f"    VP{to_subscript(str(ano))} = {format_currency(fluxo)} / (1 + {format_currency(tma, 6)}){to_superscript(str(ano))}\n")
                steps.append(f"    VP{to_subscript(str(ano))} = {format_currency(fluxo)} / {format_currency(fator, 6)}\n")
                steps.append(f"    VP{to_subscript(str(ano))} = R$ {format_currency(vp)}\n\n")

            vpl += vp

        steps.append("─" * 120 + "\n\n")
        steps.append(tr("App", "SOMATÓRIO DOS VALORES PRESENTES:") + "\n\n")
        steps.append("  VPL = ")

        for ano in range(len(fluxos_liquidos)):
            if ano > 0:
                steps.append(" + ")

            steps.append(f"VP{to_subscript(str(ano))}")

        steps.append("\n\n")

        steps.append(f"  VPL = R$ {format_currency(vpl, 2)}\n\n")

        # ANÁLISE DO RESULTADO
        steps.append("═" * 120 + "\n")
        steps.append(tr("App", "ANÁLISE DO RESULTADO") + "\n")
        steps.append("═" * 120 + "\n\n")

        if vpl > 0:
            steps.append(f"  ✓ VPL > 0: {tr('App', 'PROJETO VIÁVEL ECONOMICAMENTE')}\n\n")
            steps.append(f"  {tr('App', 'O investimento gera um valor adicional de')} R$ {format_currency(vpl)}\n")
            steps.append(f"  {tr('App', 'Isso significa que o retorno do projeto supera a TMA de')} {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}.\n")
            steps.append(f"  {tr('App', 'O projeto cria valor para a empresa e deve ser aceito')}.\n")

        elif vpl < 0:
            steps.append(f"  ✗ VPL < 0: {tr('App', 'PROJETO INVIÁVEL ECONOMICAMENTE')}\n\n")
            steps.append(f"  {tr('App', 'O investimento resulta em uma perda de')} R$ {format_currency(abs(vpl))}\n")
            steps.append(f"  {tr('App', 'Isso significa que o retorno do projeto é inferior à TMA de')} {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}.\n")
            steps.append(f"  {tr('App', 'O projeto destrói valor para a empresa e deve ser rejeitado')}.\n")

        else:
            steps.append(f"  VPL = 0: {tr('App', 'PROJETO NO LIMITE DE VIABILIDADE')}\n\n")
            steps.append(f"  {tr('App', 'O retorno do projeto é exatamente igual à TMA de')} {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}.\n")
            steps.append(f"  {tr('App', 'O projeto não cria nem destrói valor')}.\n")

        steps.append("\n")
        steps.append("═" * 120 + "\n")
        steps.append(f"RESPOSTA: {tr('App', 'O Valor Presente Líquido (VPL) é de')} R$ {format_currency(vpl, 2)}\n")
        steps.append("═" * 120 + "\n")

        self.vpl_tax_result.append("".join(steps))

    except Exception as e:
        logger.error(f"Erro ao calcular VPL com impostos: {e}", exc_info=True)
        tr = QCoreApplication.translate
        try:
            self.vpl_tax_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
