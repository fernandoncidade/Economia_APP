from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
from source.utils.TextFormat import format_currency, to_superscript, to_subscript, format_fraction

logger = LogManager.get_logger()

def calculate_value_at_k(self):
    tr = QCoreApplication.translate
    try:
        # Leitura segura dos campos obrigatórios
        p_total = self.get_float_from_line_edit(self.amort_p)
        i = self.get_float_from_line_edit(self.amort_i, is_percentage=True)
        n = int(self.get_float_from_line_edit(self.amort_n))

        # Leitura segura dos campos opcionais usando default
        entrada = self.get_float_from_line_edit(self.amort_e, default=0.0)
        carencia = int(self.get_float_from_line_edit(self.amort_carencia, default=0.0))

        # Validação do campo k
        try:
            k = int(self.get_float_from_line_edit(self.amort_k))

        except Exception:
            self.amort_result.append(tr("App", "Erro: É necessário informar o período k desejado."))
            return

        capitalizar = self.amort_juros_capitalizados.isChecked()

        # Validações
        if n <= 0:
            self.amort_result.append(tr("App", "Erro: Prazo (n) deve ser maior que zero."))
            return

        if k < 1 or k > n:
            self.amort_result.append(tr("App", "Erro: O período k deve estar entre 1 e n."))
            return

        if carencia < 0 or carencia >= n:
            self.amort_result.append(tr("App", "Erro: O período de carência deve ser menor que n e não negativo."))
            return

        p_fin = max(0.0, p_total - entrada)
        if p_fin <= 0:
            self.amort_result.append(tr("App", "Atenção: Entrada (E) igual ou maior que o principal resulta em financiamento zero ou negativo."))
            return

        system_index = self.amort_system.currentIndex()

        # Identificação textual do sistema
        sys_name = {
            0: tr("App", "Sistema Francês (Price)"),
            1: tr("App", "Sistema de Amortização Constante (SAC)"),
            4: tr("App", "Sistema Hamburguês (SAC com Carência)")
        }.get(system_index, tr("App", "Sistema não suportado para este cálculo pontual"))

        # Cabeçalho
        lines = []
        lines.append("═" * 60 + "\n")
        lines.append(tr("App", "CÁLCULO NO PERÍODO k") + " — " + sys_name + "\n")
        lines.append("═" * 60 + "\n\n")

        # Helpers para formatação de índices
        def var_with_sub(var_name: str, idx: str) -> str:
            # Usa sintaxe A_{idx} para conversão futura em HTML <sub> (HistoryContainer)
            return f"{var_name}_{{{idx}}}"

        def sup_index(idx: str) -> str:
            # Remove underscore do índice e converte tudo para superscrito unicode
            return to_superscript(str(idx).replace("_", ""))

        # Labels com subscrito completo (sem perder letras como 'f' ou 'b')
        P_fin_lbl = var_with_sub("P", "fin")
        P_base_lbl = var_with_sub("P", "base")

        # Dados
        lines.append(tr("App", "Dados:") + "\n")
        lines.append(f"  {tr('App', 'P (Principal) = R$')} {format_currency(p_total)}\n")
        if entrada > 0:
            lines.append(f"  {tr('App', 'E (Entrada) = R$')} {format_currency(entrada)}\n")
            lines.append(f"  {P_fin_lbl} ({tr('App', 'P - E')}) = R$ {format_currency(p_fin)}\n")

        else:
            lines.append(f"  {tr('App', 'E (Entrada) = R$ 0,00 (sem entrada)')}\n")
            lines.append(f"  {P_fin_lbl} = R$ {format_currency(p_fin)}\n")

        lines.append(f"  {tr('App', 'i (taxa) =')} {format_currency(i*100, 2)}% {tr('App', 'ao período')}\n")
        lines.append(f"  {tr('App', 'n (períodos) =')} {n}\n")

        if carencia > 0:
            lines.append(f"  {tr('App', 'carência (c) =')} {carencia}\n")
            lines.append(f"  {tr('App', 'Capitalizar juros na carência?')} {'Sim' if capitalizar else 'Não'}\n")

        else:
            lines.append(f"  {tr('App', 'carência (c) = 0 (sem carência)')}\n")

        lines.append(f"  {tr('App', 'k (período) =')} {k}\n\n")

        # Cálculo para Price: amortização na prestação k
        if system_index == 0:
            if k <= carencia:
                # Durante a carência não há amortização
                if capitalizar:
                    lines.append(tr("App", "Durante a carência com capitalização: não há amortização.") + "\n")

                else:
                    lines.append(tr("App", "Durante a carência com juros pagos: não há amortização.") + "\n")

                lines.append("─" * 60 + "\n")
                lines.append(f"{tr('App', 'Resultado')}: a{to_subscript(k)} = R$ {format_currency(0)}\n")
                self.amort_result.append("".join(lines))
                return

            # Saldo para iniciar a fase de amortização
            if carencia > 0:
                if capitalizar:
                    p_base = p_fin * ((1 + i) ** carencia)
                    lines.append(tr("App", "Saldo após carência (juros capitalizados):") + "\n")
                    car_super = to_superscript(carencia)
                    lines.append(f"  {P_base_lbl} = {P_fin_lbl} × (1 + i){car_super}\n")
                    lines.append(f"  {P_base_lbl} = {format_currency(p_fin)} × (1 + {format_currency(i,6)}){car_super}\n")
                    lines.append(f"  {P_base_lbl} = R$ {format_currency(p_base)}\n\n")

                else:
                    p_base = p_fin
                    lines.append(tr("App", "Saldo após carência (juros pagos):") + "\n")
                    lines.append(f"  {P_base_lbl} = {P_fin_lbl} = R$ {format_currency(p_base)}\n\n")

            else:
                p_base = p_fin
                lines.append(tr("App", "Sem carência, iniciando amortização imediatamente:") + "\n")
                lines.append(f"  {P_base_lbl} = {P_fin_lbl} = R$ {format_currency(p_base)}\n\n")

            n_amort = n - carencia
            m = k - carencia  # índice dentro da fase de amortização

            # i = 0: caso degenerado
            if abs(i) < 1e-15:
                pmt = p_base / n_amort
                a1 = pmt
                ak = a1  # constante
                lines.append(tr("App", "Taxa zero: prestação e amortização constantes na fase de amortização.") + "\n")
                lines.append(f"  PMT = {P_base_lbl} / n_amort = {format_currency(p_base)} / {n_amort}\n")
                lines.append(f"  PMT = R$ {format_currency(pmt)}\n")
                lines.append(f"  a₁ = PMT = R$ {format_currency(a1)}\n")
                lines.append(f"  a{to_subscript(k)} = a₁ = R$ {format_currency(ak)}\n")

            else:
                pow_val = (1 + i) ** n_amort
                num = i * pow_val
                den = pow_val - 1
                fator = num / den

                pmt = p_base * fator
                a1 = pmt - p_base * i
                ak = a1 * ((1 + i) ** (m - 1))

                # Termos com expoente n_amort inteiro como superscrito (underscore suprimido)
                n_amort_sup = sup_index("n_amort")
                
                # PASSO 1: Fórmula com variáveis
                numer_str = f"i × (1+i){n_amort_sup}"
                denom_str = f"(1+i){n_amort_sup} - 1"

                lines.append(tr("App", "Fator (A/P) na fase de amortização:") + "\n")
                f1, f2, f3 = format_fraction(numer_str, denom_str, prefix="  (A/P) = ")
                lines.append(f1 + "\n" + f2 + "\n" + f3 + f" = {format_currency(fator,6)}\n\n")

                # PASSO 2: Fórmula com valores numéricos substituídos
                n_amort_sup_num = to_superscript(str(n_amort))
                numer_str_valores = f"{format_currency(i,6)} × (1+{format_currency(i,6)}){n_amort_sup_num}"
                denom_str_valores = f"(1+{format_currency(i,6)}){n_amort_sup_num} - 1"

                lines.append(tr("App", "Substituindo os valores:") + "\n")
                f1_val, f2_val, f3_val = format_fraction(numer_str_valores, denom_str_valores, prefix="  (A/P) = ")
                lines.append(f1_val + "\n" + f2_val + "\n" + f3_val + "\n\n")

                # PASSO 3: Cálculo do numerador e denominador separadamente
                lines.append(tr("App", "Cálculo intermediário:") + "\n")
                lines.append(f"  {tr('App', 'Numerador')} = {format_currency(i,6)} × (1+{format_currency(i,6)}){n_amort_sup_num}\n")
                lines.append(f"  {tr('App', 'Numerador')} = {format_currency(i,6)} × {format_currency(1+i,6)}{n_amort_sup_num}\n")
                lines.append(f"  {tr('App', 'Numerador')} = {format_currency(i,6)} × {format_currency(pow_val,6)}\n")
                lines.append(f"  {tr('App', 'Numerador')} = {format_currency(num,6)}\n\n")

                lines.append(f"  {tr('App', 'Denominador')} = (1+{format_currency(i,6)}){n_amort_sup_num} - 1\n")
                lines.append(f"  {tr('App', 'Denominador')} = {format_currency(1+i,6)}{n_amort_sup_num} - 1\n")
                lines.append(f"  {tr('App', 'Denominador')} = {format_currency(pow_val,6)} - 1\n")
                lines.append(f"  {tr('App', 'Denominador')} = {format_currency(den,6)}\n\n")

                # PASSO 4: Resultado final da divisão
                lines.append(tr("App", "Cálculo final:") + "\n")
                f1_final, f2_final, f3_final = format_fraction(
                    format_currency(num,6), 
                    format_currency(den,6), 
                    prefix="  (A/P) = "
                )
                lines.append(f1_final + "\n" + f2_final + "\n" + f3_final + f" = {format_currency(fator,6)}\n\n")

                lines.append(tr("App", "Prestação constante:") + "\n")
                lines.append(f"  PMT = {P_base_lbl} × (A/P) = {format_currency(p_base)} × {format_currency(fator,6)}\n")
                lines.append(f"  PMT = R$ {format_currency(pmt)}\n\n")
                lines.append(tr("App", "Amortização inicial e na k-ésima:") + "\n")
                lines.append(f"  a₁ = PMT - {P_base_lbl} × i = {format_currency(pmt)} - {format_currency(p_base)} × {format_currency(i,6)}\n")
                lines.append(f"  a₁ = R$ {format_currency(a1)}\n")
                lines.append(f"  a{to_subscript(k)} = a₁ × (1+i){to_superscript(m-1)} = {format_currency(a1)} × (1+{format_currency(i,6)}){to_superscript(m-1)}\n")
                lines.append(f"  a{to_subscript(k)} = R$ {format_currency(ak)}\n")

            lines.append("─" * 60 + "\n")
            lines.append(f"{tr('App', 'Resultado')}: a{to_subscript(k)} = R$ {format_currency(ak)}\n")
            self.amort_result.append("".join(lines))
            return

        # Cálculo para SAC (ou Hamburguês): prestação na prestação k
        if system_index in (1, 4):
            if k <= carencia:
                # Durante carência: sem amortização
                if capitalizar:
                    pmt_k = 0.0
                    lines.append(tr("App", "Durante a carência com capitalização: não há pagamento (PMT_k = 0).") + "\n")

                else:
                    juros = p_fin * i
                    pmt_k = juros
                    lines.append(tr("App", "Durante a carência com juros pagos: prestação igual aos juros.") + "\n")
                    lines.append(f"  PMT{to_subscript(k)} = J = {P_fin_lbl} × i = {format_currency(p_fin)} × {format_currency(i,6)} = R$ {format_currency(pmt_k)}\n")

                lines.append("─" * 60 + "\n")
                lines.append(f"{tr('App', 'Resultado')}: PMT{to_subscript(k)} = R$ {format_currency(pmt_k)}\n")
                self.amort_result.append("".join(lines))
                return

            # Após carência
            if carencia > 0:
                if capitalizar:
                    saldo_pos_car = p_fin * ((1 + i) ** carencia)
                    lines.append(tr("App", "Saldo após carência (juros capitalizados):") + "\n")
                    lines.append(f"  SD{to_subscript(carencia)} = {P_fin_lbl} × (1+i){to_superscript(carencia)} = R$ {format_currency(saldo_pos_car)}\n\n")

                else:
                    saldo_pos_car = p_fin
                    lines.append(tr("App", "Saldo após carência (juros pagos):") + "\n")
                    lines.append(f"  SD{to_subscript(carencia)} = {P_fin_lbl} = R$ {format_currency(saldo_pos_car)}\n\n")

            else:
                saldo_pos_car = p_fin
                lines.append(tr("App", "Sem carência, iniciando amortização imediatamente:") + "\n")
                lines.append(f"  SD{to_subscript(0)} = {P_fin_lbl} = R$ {format_currency(saldo_pos_car)}\n\n")

            n_amort = n - carencia
            a = saldo_pos_car / n_amort
            m = k - carencia  # índice dentro da fase de amortização

            # Juros no período m da fase de amortização
            # j_m = i × (SD_c - a × (m-1))
            juros_m = i * (saldo_pos_car - a * (m - 1))
            pmt_k = a + juros_m

            lines.append(tr("App", "Amortização constante na fase de amortização (SAC):") + "\n")
            if carencia > 0:
                lines.append(f"  a = SD{to_subscript(carencia)} / n_amort = {format_currency(saldo_pos_car)} / {n_amort}\n")

            else:
                lines.append(f"  a = P_fin / n = {format_currency(saldo_pos_car)} / {n_amort}\n")

            lines.append(f"  a = R$ {format_currency(a)}\n\n")
            lines.append(tr("App", "Juros no período k:") + "\n")
            if carencia > 0:
                lines.append(f"  J{to_subscript(k)} = i × (SD{to_subscript(carencia)} - a × ({m}-1))\n")

            else:
                lines.append(f"  J{to_subscript(k)} = i × (P_fin - a × ({m}-1))\n")

            lines.append(f"  J{to_subscript(k)} = {format_currency(i,6)} × ({format_currency(saldo_pos_car)} - {format_currency(a)} × {m-1}) = R$ {format_currency(juros_m)}\n\n")
            lines.append(tr("App", "Prestação na k-ésima:") + "\n")
            lines.append(f"  PMT{to_subscript(k)} = a + J{to_subscript(k)} = {format_currency(a)} + {format_currency(juros_m)}\n")
            lines.append(f"  PMT{to_subscript(k)} = R$ {format_currency(pmt_k)}\n")

            lines.append("─" * 60 + "\n")
            lines.append(f"{tr('App', 'Resultado')}: PMT{to_subscript(k)} = R$ {format_currency(pmt_k)}\n")
            self.amort_result.append("".join(lines))
            return

        # Sistemas não suportados para cálculo pontual
        self.amort_result.append(tr("App", "Sistema selecionado não suporta cálculo pontual de k."))

    except Exception as e:
        logger.error(f"Erro em calculate_value_at_k: {e}", exc_info=True)
        self.amort_result.append(f"{tr('App', 'Erro')}: {e}")
