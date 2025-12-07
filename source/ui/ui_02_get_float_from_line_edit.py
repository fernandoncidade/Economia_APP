from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_float_from_line_edit(self, line_edit, is_percentage=False, default=None):
    try:
        text = line_edit.text().strip().replace(',', '.')
        if not text:
            if default is not None:
                return default

            raise ValueError("O campo não pode estar vazio.")

        value = float(text)
        return value / 100.0 if is_percentage else value

    except ValueError as e:
        if default is not None and "could not convert" in str(e):
            logger.warning(f"Valor inválido no campo, usando padrão: {default}")
            return default

        logger.error(f"Erro ao obter float do LineEdit: {e}", exc_info=True)
        raise

    except Exception as e:
        logger.error(f"Erro ao obter float do LineEdit: {e}", exc_info=True)
        raise
