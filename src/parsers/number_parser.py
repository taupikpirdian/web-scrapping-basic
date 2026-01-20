"""Number parsing utilities."""


def parse_id_number(text: str) -> float:
    """Parse format angka Indonesia ke float.

    Args:
        text: String angka dengan format Indonesia (1.000,50)

    Returns:
        Float value dari angka yang di-parse

    Examples:
        >>> parse_id_number("1.000,50")
        1000.5
        >>> parse_id_number("500")
        500.0
    """
    return float(text.replace(".", "").replace(",", "."))
