def implode(separator, list):
    if separator is None:
        separator = ", "

    error_message = separator.join(str(x) for x in list)
    return error_message
