

def remove_html(string):
    """Expurgate HTML from string data."""
    result = string
    result = re.sub(
        '<.*/?>|<.*>.*<.*>',
        '',
        result
    )
    return result