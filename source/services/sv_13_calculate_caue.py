from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtGui import QBrush
from source.utils.LogManager import LogManager
from source.utils.TextFormat import format_currency, to_subscript, to_superscript, format_fraction

logger = LogManager.get_logger()

def calculate_caue(self):
    try:
        tr = QCoreApplication.translate

        # Ler dados principais
        p = self.get_float_from_line_edit(self.caue_initial_cost)
        tma = self.get_float_from_line_edit(self.caue_tma, is_percentage=True)
        max_years = int(self.get_float_from_line_edit(self.caue_max_years))

        # Ler dados da tabela
        dados = []
        for n in range(max_years):
            try:
                vr_item = self.caue_input_table.item(n, 1)
                com_item = self.caue_input_table.item(n, 2)

                if not vr_item or not com_item or not vr_item.text().strip() or not com_item.text().strip():
                    self.caue_result.append(tr("App", f"Erro: Dados incompletos na linha {n+1}"))
                    return

                vr_n = float(vr_item.text().replace('.', '').replace(',', '.'))
                com_n = float(com_item.text().replace('.', '').replace(',', '.'))
                dados.append({'ano': n+1, 'vr': vr_n, 'com': com_n})

            except ValueError:
                self.caue_result.append(tr("App", f"Erro: Valores inválidos na linha {n+1}"))
                return

        steps = []
        steps.append("═" * 70 + "\n")
        steps.append(tr("App", "CÁLCULO DE CAUE E VIDA ECONÔMICA DO ATIVO") + "\n")
        steps.append("═" * 70 + "\n\n")

        steps.append(tr("App", "DADOS DO EXERCÍCIO:") + "\n")
        steps.append("─" * 70 + "\n")
        steps.append(f"  • {tr('App', 'Custo de Aquisição (P)')}: R$ {format_currency(p)}\n")
        steps.append(f"  • {tr('App', 'Taxa Mínima de Atratividade (TMA)')}: {format_currency(tma*100, 2)}% {tr('App', 'ao ano')}\n")
        steps.append(f"  • {tr('App', 'Período máximo de análise')}: {max_years} {tr('App', 'anos')}\n\n")

        steps.append(tr("App", "Valores de Revenda (VR_n) e Custos de Operação (Com_n):") + "\n\n")
        steps.append(f"  {'Ano (n)':>8} | {'VR_n (R$)':>15} | {'Com_n (R$)':>15}\n")
        steps.append("  " + "─" * 45 + "\n")
        for d in dados:
            steps.append(f"  {d['ano']:>8} | {format_currency(d['vr']):>15} | {format_currency(d['com']):>15}\n")

        steps.append("\n")

        steps.append("═" * 70 + "\n")
        steps.append(tr("App", "METODOLOGIA DE CÁLCULO") + "\n")
        steps.append("═" * 70 + "\n\n")

        steps.append(tr("App", "O objetivo é determinar a vida econômica do ativo, que é o período que resulta no menor Custo Anual Uniforme Equivalente (CAUE).") + "\n\n")

        steps.append(tr("App", "Fórmula do CAUE:") + "\n")
        steps.append(f"  CAUE{to_subscript('n')} = VP{to_subscript('n')} × (A/P; i; n)\n\n")

        steps.append(tr("App", "Onde o VP_n (Valor Presente total dos custos) é:") + "\n")
        steps.append(f"  VP{to_subscript('n')} = P + VP(Custos){to_subscript('n')} - VP(Revenda){to_subscript('n')}\n\n")

        # Cálculos para cada ano
        resultados = []

        for idx, d in enumerate(dados):
            n = d['ano']

            steps.append("═" * 70 + "\n")
            steps.append(f"{tr('App', 'ANO')} {n} (n={n})\n")
            steps.append("═" * 70 + "\n\n")

            # VP dos Custos de Operação (acumulado)
            vp_com_total = 0
            steps.append(f"1. {tr('App', 'VP DOS CUSTOS DE OPERAÇÃO (ACUMULADO)')}\n")
            steps.append("─" * 70 + "\n\n")

            for j in range(1, n+1):
                pf_factor = 1 / ((1 + tma) ** j)
                vp_com_j = dados[j-1]['com'] * pf_factor
                vp_com_total += vp_com_j

                steps.append(f"  {tr('App', 'Ano')} {j}:\n")
                steps.append(f"    (P/F; {format_currency(tma*100, 2)}%; {j}) = 1 / (1 + {format_currency(tma, 6)}){to_superscript(j)}\n")
                steps.append(f"    (P/F; {format_currency(tma*100, 2)}%; {j}) = {format_currency(pf_factor, 6)}\n")
                steps.append(f"    VP(Com{to_subscript(j)}) = {format_currency(dados[j-1]['com'])} × {format_currency(pf_factor, 6)}\n")
                steps.append(f"    VP(Com{to_subscript(j)}) = R$ {format_currency(vp_com_j)}\n\n")

            steps.append(f"  VP(Custos){to_subscript(n)} = R$ {format_currency(vp_com_total)}\n\n")

            # VP do Valor de Revenda
            steps.append(f"2. {tr('App', 'VP DO VALOR DE REVENDA')}\n")
            steps.append("─" * 70 + "\n\n")

            pf_revenda = 1 / ((1 + tma) ** n)
            vp_revenda = d['vr'] * pf_revenda

            steps.append(f"  (P/F; {format_currency(tma*100, 2)}%; {n}) = 1 / (1 + {format_currency(tma, 6)}){to_superscript(n)}\n")
            steps.append(f"  (P/F; {format_currency(tma*100, 2)}%; {n}) = {format_currency(pf_revenda, 6)}\n")
            steps.append(f"  VP(VR{to_subscript(n)}) = {format_currency(d['vr'])} × {format_currency(pf_revenda, 6)}\n")
            steps.append(f"  VP(VR{to_subscript(n)}) = R$ {format_currency(vp_revenda)}\n\n")

            # VP Total
            steps.append(f"3. {tr('App', 'VP TOTAL')}\n")
            steps.append("─" * 70 + "\n\n")

            vp_total = p + vp_com_total - vp_revenda

            steps.append(f"  VP{to_subscript(n)} = P + VP(Custos){to_subscript(n)} - VP(Revenda){to_subscript(n)}\n")
            steps.append(f"  VP{to_subscript(n)} = {format_currency(p)} + {format_currency(vp_com_total)} - {format_currency(vp_revenda)}\n")
            steps.append(f"  VP{to_subscript(n)} = R$ {format_currency(vp_total)}\n\n")

            # CAUE
            steps.append(f"4. {tr('App', 'CÁLCULO DO CAUE')}\n")
            steps.append("─" * 70 + "\n\n")

            pow_val = (1 + tma) ** n
            ap_num = tma * pow_val
            ap_den = pow_val - 1
            ap_factor = ap_num / ap_den
            caue = vp_total * ap_factor

            steps.append(tr("App", "Fator (A/P):") + "\n")
            f1, f2, f3 = format_fraction(
                f"i × (1+i){to_superscript(n)}", 
                f"(1+i){to_superscript(n)} - 1", 
                prefix="  (A/P; 12%; " + str(n) + ") = "
            )
            steps.append(f1 + "\n")
            steps.append(f2 + "\n")
            steps.append(f3 + "\n\n")

            steps.append(f"  (1 + i){to_superscript(n)} = (1 + {format_currency(tma, 6)}){to_superscript(n)}\n")
            steps.append(f"  (1 + i){to_superscript(n)} = {format_currency(pow_val, 6)}\n\n")

            steps.append(f"  {tr('App', 'Numerador')}: {format_currency(tma, 6)} × {format_currency(pow_val, 6)} = {format_currency(ap_num, 6)}\n")
            steps.append(f"  {tr('App', 'Denominador')}: {format_currency(pow_val, 6)} - 1 = {format_currency(ap_den, 6)}\n\n")

            steps.append(f"  (A/P; {format_currency(tma*100, 2)}%; {n}) = {format_currency(ap_num, 6)} / {format_currency(ap_den, 6)}\n")
            steps.append(f"  (A/P; {format_currency(tma*100, 2)}%; {n}) = {format_currency(ap_factor, 6)}\n\n")

            steps.append(f"  CAUE{to_subscript(n)} = VP{to_subscript(n)} × (A/P; {format_currency(tma*100, 2)}%; {n})\n")
            steps.append(f"  CAUE{to_subscript(n)} = {format_currency(vp_total)} × {format_currency(ap_factor, 6)}\n")
            steps.append(f"  CAUE{to_subscript(n)} = R$ {format_currency(caue, 2)}\n\n")

            resultados.append({'ano': n, 'vr': d['vr'], 'com': d['com'], 'caue': caue})

        # Tabela resumo (texto)
        steps.append("═" * 70 + "\n")
        steps.append(tr("App", "TABELA DE RESULTADOS") + "\n")
        steps.append("═" * 70 + "\n\n")

        steps.append(f"  {'Ano (n)':>8} | {'VR_n (R$)':>15} | {'Com_n (R$)':>15} | {'CAUE_n (R$)':>15}\n")
        steps.append("  " + "─" * 60 + "\n")

        menor_caue = min(resultados, key=lambda x: x['caue'])

        for r in resultados:
            marker = " ← MENOR CAUE" if r['ano'] == menor_caue['ano'] else ""
            steps.append(f"  {r['ano']:>8} | {format_currency(r['vr']):>15} | {format_currency(r['com']):>15} | {format_currency(r['caue'], 2):>15}{marker}\n")

        steps.append("\n")

        # Criar tabela QTableWidget que será inserida dentro da entrada do HistoryContainer
        try:
            table_widget = QTableWidget()
            table_widget.setColumnCount(4)
            table_headers = [
                tr("App", "Ano (n)"),
                tr("App", "VR_n (R$)"),
                tr("App", "Com_n (R$)"),
                tr("App", "CAUE_n (R$)"),
            ]
            table_widget.setHorizontalHeaderLabels(table_headers)
            table_widget.setRowCount(len(resultados))
            table_widget.horizontalHeader().setSectionResizeMode(0, table_widget.horizontalHeader().ResizeMode.Stretch)
            table_widget.horizontalHeader().setSectionResizeMode(1, table_widget.horizontalHeader().ResizeMode.Stretch)
            table_widget.horizontalHeader().setSectionResizeMode(2, table_widget.horizontalHeader().ResizeMode.Stretch)
            table_widget.horizontalHeader().setSectionResizeMode(3, table_widget.horizontalHeader().ResizeMode.Stretch)
            # Ajuste: preferir altura fixa para garantir não sobrepor texto
            table_widget.setFixedHeight(140)

            for r_idx, r in enumerate(resultados):
                it_n = QTableWidgetItem(str(r['ano']))
                it_vr = QTableWidgetItem(format_currency(r['vr']))
                it_com = QTableWidgetItem(format_currency(r['com']))
                it_caue = QTableWidgetItem(format_currency(r['caue'], 2))

                for it in (it_n, it_vr, it_com, it_caue):
                    it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)

                table_widget.setItem(r_idx, 0, it_n)
                table_widget.setItem(r_idx, 1, it_vr)
                table_widget.setItem(r_idx, 2, it_com)
                table_widget.setItem(r_idx, 3, it_caue)

            # Opcional: destacar a linha do menor CAUE (fundo leve)
            try:
                for r_idx, r in enumerate(resultados):
                    if r['ano'] == menor_caue['ano']:
                        for c in range(table_widget.columnCount()):
                            item = table_widget.item(r_idx, c)
                            if item:
                                item.setBackground(QBrush())

            except Exception:
                pass

        except Exception as e_tbl:
            logger.error(f"Erro ao criar tabela de resultados CAUE para inserir no HistoryContainer: {e_tbl}", exc_info=True)
            table_widget = None

        # Inserir texto + tabela dentro do HistoryContainer (tabela fica parte integrante da resposta)
        try:
            self.caue_result.append("".join(steps), extra_widget=table_widget)

        except Exception as e_append:
            logger.error(f"Erro ao inserir resultado CAUE no HistoryContainer: {e_append}", exc_info=True)
            try:
                self.caue_result.append("".join(steps))

            except Exception:
                pass

        # Também preencher, para compatibilidade, a caue_output_table (atributo disponível mas não mostrado no layout)
        try:
            if hasattr(self, "caue_output_table") and self.caue_output_table is not None:
                tbl = self.caue_output_table
                tbl.setRowCount(len(resultados))
                for r, row in enumerate(resultados):
                    it_n = QTableWidgetItem(str(row['ano']))
                    it_vr = QTableWidgetItem(format_currency(row['vr']))
                    it_com = QTableWidgetItem(format_currency(row['com']))
                    it_caue = QTableWidgetItem(format_currency(row['caue'], 2))

                    for it in (it_n, it_vr, it_com, it_caue):
                        it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)

                    tbl.setItem(r, 0, it_n)
                    tbl.setItem(r, 1, it_vr)
                    tbl.setItem(r, 2, it_com)
                    tbl.setItem(r, 3, it_caue)

                # Remover qualquer destaque de fundo (incolor)
                for r in range(tbl.rowCount()):
                    for c in range(tbl.columnCount()):
                        item = tbl.item(r, c)
                        if item:
                            item.setBackground(QBrush())

        except Exception as e_tbl:
            logger.error(f"Erro ao preencher tabela de resultados CAUE (atributo oculto): {e_tbl}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao calcular CAUE: {e}", exc_info=True)
        tr = QCoreApplication.translate

        try:
            self.caue_result.append(f"{tr('App', 'Erro')}: {e}")

        except Exception:
            pass
