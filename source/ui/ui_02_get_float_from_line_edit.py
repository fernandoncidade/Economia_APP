def get_float_from_line_edit(self, line_edit, is_percentage=False):
    text = line_edit.text().strip().replace(',', '.')
    if not text:
        raise ValueError("O campo não pode estar vazio.")

    value = float(text)
    return value / 100.0 if is_percentage else value
