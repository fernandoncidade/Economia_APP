def generate_sam_table(self, p, i, n):
    self.amort_table.setVisible(False)
    sac_data = self.generate_sac_table(p, i, n)
    price_data = self.generate_price_table(p, i, n)
    self.amort_table.setVisible(True)

    for k in range(1, n + 1):
        prestacao = (sac_data[k-1]['prestacao'] + price_data[k-1]['prestacao']) / 2
        juros = (sac_data[k-1]['juros'] + price_data[k-1]['juros']) / 2
        amortizacao = (sac_data[k-1]['amortizacao'] + price_data[k-1]['amortizacao']) / 2
        saldo_devedor = (sac_data[k-1]['saldo'] + price_data[k-1]['saldo']) / 2
        self.set_amort_table_row(k, prestacao, juros, amortizacao, saldo_devedor)
