from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def generate_american_table(self, p, i, n):
    try:
        saldo_devedor = p
        juros_periodo = p * i

        # Períodos intermediários: apenas juros
        for k in range(1, n):
            prestacao = juros_periodo
            amortizacao = 0
            self.set_amort_table_row(k, prestacao, juros_periodo, amortizacao, saldo_devedor)

        # Último período: juros + amortização total
        prestacao_final = juros_periodo + p
        self.set_amort_table_row(n, prestacao_final, juros_periodo, p, 0)

        return self.get_table_data(n)

    except Exception as e:
        logger.error(f"Erro ao gerar tabela Sistema Americano: {e}", exc_info=True)
        raise
