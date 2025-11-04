from utils.LogManager import LogManager
logger = LogManager.get_logger()

def generate_price_table(self, p, i, n):
    try:
        saldo_devedor = p
        factor = (i * (1 + i) ** n) / ((1 + i) ** n - 1)
        prestacao = p * factor
        for k in range(1, n + 1):
            juros = saldo_devedor * i
            amortizacao = prestacao - juros
            saldo_devedor -= amortizacao
            self.set_amort_table_row(k, prestacao, juros, amortizacao, saldo_devedor)

        return self.get_table_data(n)

    except Exception as e:
        logger.error(f"Erro ao gerar tabela Price: {e}", exc_info=True)
        raise
