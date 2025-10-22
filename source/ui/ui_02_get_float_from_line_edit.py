from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_float_from_line_edit(self, line_edit, is_percentage=False):
    try:
        text = line_edit.text().strip().replace(',', '.')
        if not text:
            raise ValueError("O campo não pode estar vazio.")

        value = float(text)
        return value / 100.0 if is_percentage else value

    except Exception as e:
        logger.error(f"Erro ao obter float do LineEdit: {e}", exc_info=True)
        raise
