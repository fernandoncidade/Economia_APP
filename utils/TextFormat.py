import re

_SUB_UNICODE = str.maketrans({
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
    "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉",
    "a": "ₐ", "e": "ₑ", "h": "ₕ", "i": "ᵢ", "j": "ⱼ",
    "k": "ₖ", "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ",
    "p": "ₚ", "r": "ᵣ", "s": "ₛ", "t": "ₜ", "u": "ᵤ",
    "v": "ᵥ", "x": "ₓ", "c": "ᴄ",
    "A": "ₐ", "E": "ₑ", "H": "ₕ", "I": "ᵢ", "J": "ⱼ",
    "K": "ₖ", "L": "ₗ", "M": "ₘ", "N": "ₙ", "O": "ₒ",
    "P": "ₚ", "R": "ᵣ", "S": "ₛ", "T": "ₜ", "U": "ᵤ",
    "V": "ᵥ", "X": "ₓ", "C": "ᴄ",
    "+": "₊", "-": "₋", "=": "₌", "(": "₍", ")": "₎",
    "/": "/", ".": ".", ",": ","
})

_SUPER_UNICODE = str.maketrans({
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "+": "⁺", "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾",
    ".": "·", ",": "·",
    "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ", "e": "ᵉ", "f": "ᶠ",
    "g": "ᵍ", "h": "ʰ", "i": "ⁱ", "j": "ʲ", "k": "ᵏ", "l": "ˡ",
    "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "r": "ʳ", "s": "ˢ",
    "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ", "z": "ᶻ",
    "A": "ᵃ", "B": "ᵇ", "C": "ᶜ", "D": "ᵈ", "E": "ᵉ", "F": "ᶠ",
    "G": "ᵍ", "H": "ʰ", "I": "ⁱ", "J": "ʲ", "K": "ᵏ", "L": "ˡ",
    "M": "ᵐ", "N": "ⁿ", "O": "ᵒ", "P": "ᵖ", "R": "ʳ", "S": "ˢ",
    "T": "ᵗ", "U": "ᵘ", "V": "ᵛ", "W": "ʷ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ",
})

_SUB_PATTERN = re.compile(r'([A-Za-zÀ-ÖØ-öø-ÿ])_({[^}]+}|[A-Za-z0-9+\-*/.,]+)(?![A-Za-z0-9_])')

def to_html_subscripts(text: str) -> str:
    def _repl(m: re.Match) -> str:
        base = m.group(1)
        idx = m.group(2)
        if idx.startswith("{") and idx.endswith("}"):
            idx = idx[1:-1]

        return f"{base}<sub>{idx}</sub>"

    return _SUB_PATTERN.sub(_repl, text or "")

def to_unicode_subscripts(text: str) -> str:
    def _repl(m: re.Match) -> str:
        base = m.group(1)
        idx = m.group(2)
        if idx.startswith("{") and idx.endswith("}"):
            idx = idx[1:-1]

        idx_uni = idx.translate(_SUB_UNICODE)
        return f"{base}{idx_uni}"

    return _SUB_PATTERN.sub(_repl, text or "")

def to_subscript(text) -> str:
    text = str(text)
    return text.translate(_SUB_UNICODE)

def to_superscript(text) -> str:
    text = str(text)
    return text.translate(_SUPER_UNICODE)

def to_superscript_parens(text) -> str:
    s = to_superscript(str(text))
    return f"⁽{s}⁾"

def format_currency(value, decimals=2) -> str:
    s = f"{value:,.{decimals}f}"
    s = s.replace(",", "T")
    s = s.replace(".", ",")
    s = s.replace("T", ".")
    return s

def format_fraction(numer_str, denom_str, prefix="") -> tuple[str, str, str]:
    numer = str(numer_str)
    denom = str(denom_str)
    width = max(len(numer), len(denom), 3)
    pad = " " * len(prefix)
    numer_line = pad + numer.center(width)
    divider_line = prefix + "─" * width
    denom_line = pad + denom.center(width)
    return numer_line, divider_line, denom_line

def format_fraction_inline(numer_str, denom_str) -> str:
    return f"{numer_str} / {denom_str}"

def format_equation_steps(steps: list) -> str:
    return "\n".join(f"  {step}" for step in steps)
