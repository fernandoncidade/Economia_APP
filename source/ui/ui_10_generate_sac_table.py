from utils.LogManager import LogManager
logger = LogManager.get_logger()

def generate_sac_table(self, p, i, n):
    try:
        saldo_devedor = p
        amortizacao_constante = p / n
        for k in range(1, n + 1):
            juros = saldo_devedor * i
            prestacao = amortizacao_constante + juros
            saldo_devedor -= amortizacao_constante
            self.set_amort_table_row(k, prestacao, juros, amortizacao_constante, saldo_devedor)

        return self.get_table_data(n)

    except Exception as e:
        logger.error(f"Erro ao gerar tabela SAC: {e}", exc_info=True)
        raise
