from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_table_data(self, n):
    try:
        data = []
        for k in range(1, n + 1):
            data.append({
                'prestacao': float(self.amort_table.item(k, 1).text()),
                'juros': float(self.amort_table.item(k, 2).text()),
                'amortizacao': float(self.amort_table.item(k, 3).text()),
                'saldo': float(self.amort_table.item(k, 4).text())
            })
        return data

    except Exception as e:
        logger.error(f"Erro ao obter dados da tabela de amortização: {e}", exc_info=True)
        raise
