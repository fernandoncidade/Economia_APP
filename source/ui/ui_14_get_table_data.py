def get_table_data(self, n):
    data = []
    for k in range(1, n + 1):
        data.append({
            'prestacao': float(self.amort_table.item(k, 1).text()),
            'juros': float(self.amort_table.item(k, 2).text()),
            'amortizacao': float(self.amort_table.item(k, 3).text()),
            'saldo': float(self.amort_table.item(k, 4).text())
        })
    return data
