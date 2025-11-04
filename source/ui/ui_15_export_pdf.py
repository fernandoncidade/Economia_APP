from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QTextDocument
from html import escape

def export_to_pdf(self, text_widget, suggested_name="export.pdf"):
    filename, _ = QFileDialog.getSaveFileName(self, "Salvar como PDF", suggested_name, "PDF Files (*.pdf)")
    if not filename:
        return

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    printer = QPrinter()
    try:
        printer.setOutputFormat(QPrinter.PdfFormat)

    except Exception:
        pass

    printer.setOutputFileName(filename)

    if hasattr(text_widget, "document"):
        doc = text_widget.document()

    else:
        if hasattr(text_widget, "toPlainText"):
            doc = QTextDocument()
            doc.setPlainText(text_widget.toPlainText())

        else:
            doc = QTextDocument()
            doc.setPlainText(str(text_widget))

    if hasattr(doc, "print_"):
        doc.print_(printer)

    else:
        try:
            doc.print(printer)

        except Exception:
            pass

def amort_table_to_html(self):
    tw = getattr(self, "amort_table", None)
    if tw is None:
        return ""

    cols = tw.columnCount()
    rows = tw.rowCount()

    # Cabeçalhos
    headers = []
    for c in range(cols):
        hi = tw.horizontalHeaderItem(c)
        headers.append(escape(hi.text() if hi else f"Col {c+1}"))

    # Linhas
    body_rows = []
    for r in range(rows):
        tds = []
        for c in range(cols):
            it = tw.item(r, c)
            tds.append(escape(it.text() if it else ""))

        body_rows.append("<tr>" + "".join(f"<td>{td}</td>" for td in tds) + "</tr>")

    table_css = """
    <style>
    table { border-collapse: collapse; width: 100%; font-size: 10pt; }
    th, td { border: 1px solid #444; padding: 4px 6px; text-align: left; }
    thead tr { background: #f0f0f0; }
    h1, h2 { margin: 12px 0 6px 0; }
    pre { white-space: pre-wrap; font-family: Consolas, monospace; }
    </style>
    """

    html = [
        table_css,
        "<h2>Tabela de Amortização</h2>",
        "<table>",
        "<thead><tr>",
        "".join(f"<th>{h}</th>" for h in headers),
        "</tr></thead>",
        "<tbody>",
        "\n".join(body_rows),
        "</tbody></table>",
    ]
    return "".join(html)

def export_amortization_pdf(self, suggested_name="amortizacao.pdf"):
    filename, _ = QFileDialog.getSaveFileName(self, "Salvar como PDF", suggested_name, "PDF Files (*.pdf)")
    if not filename:
        return

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    calc_widget = getattr(self, "amort_result", None)
    calc_text = ""
    if calc_widget and hasattr(calc_widget, "toPlainText"):
        calc_text = calc_widget.toPlainText().strip()

    calc_html = ""
    if calc_text:
        calc_html = f"<h2>Cálculos</h2><pre>{escape(calc_text)}</pre>"

    table_html = amort_table_to_html(self)

    full_html = f"""
    <html>
    <head><meta charset="utf-8"></head>
    <body>
        <h1>Amortização</h1>
        {calc_html}
        {table_html}
    </body>
    </html>
    """

    printer = QPrinter()
    try:
        printer.setOutputFormat(QPrinter.PdfFormat)

    except Exception:
        pass

    printer.setOutputFileName(filename)

    doc = QTextDocument()
    doc.setHtml(full_html)

    if hasattr(doc, "print_"):
        doc.print_(printer)

    else:
        try:
            doc.print(printer)

        except Exception:
            pass
