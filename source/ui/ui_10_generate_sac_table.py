def generate_sac_table(self, p, i, n):
    saldo_devedor = p
    amortizacao_constante = p / n
    for k in range(1, n + 1):
        juros = saldo_devedor * i
        prestacao = amortizacao_constante + juros
        saldo_devedor -= amortizacao_constante
        self.set_amort_table_row(k, prestacao, juros, amortizacao_constante, saldo_devedor)

    return self.get_table_data(n)
