from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def generate_hamburgues_table(self, p, i, n, carencia, capitalizar_juros):
    try:
        saldo_devedor = p

        # Fase 1: Carência
        for k in range(1, carencia + 1):
            if capitalizar_juros:
                # Juros são capitalizados (incorporados ao saldo)
                juros = saldo_devedor * i
                prestacao = 0
                amortizacao = 0
                saldo_devedor = saldo_devedor + juros

            else:
                # Juros são pagos mensalmente
                juros = saldo_devedor * i
                prestacao = juros
                amortizacao = 0
                # Saldo devedor não muda

            self.set_amort_table_row(k, prestacao, juros, amortizacao, saldo_devedor)

        # Fase 2: Amortização (SAC sobre o saldo devedor ao final da carência)
        n_amort = n - carencia
        amortizacao_constante = saldo_devedor / n_amort

        for k in range(carencia + 1, n + 1):
            juros = saldo_devedor * i
            amortizacao = amortizacao_constante
            prestacao = juros + amortizacao
            saldo_devedor -= amortizacao

            self.set_amort_table_row(k, prestacao, juros, amortizacao, saldo_devedor)

        return self.get_table_data(n)

    except Exception as e:
        logger.error(f"Erro ao gerar tabela Sistema Hamburguês: {e}", exc_info=True)
        raise
