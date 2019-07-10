WHITE_SPACE_CHARS = "\n\r "


class InvalidValueError(ValueError):
    MSG = "Invalid value for the attribute (%s)"

    def __init__(self, attribute_name):
        super(InvalidValueError, self).__init__(self.MSG % attribute_name)


def _get_next_attribute(from_pos, raw):
    """
    :param from_pos: The position to start looking from
    :param raw: The content to parse.

    :return:
        The name, the value and the stop position.
        It will return None as the attribute name if nothing was found.

    :rtype: (Optional[str], Union[str, bool], int)
    """

    skip_next = False
    found_name = False
    found_value = False
    value_quote_type = None  # the quote type of the value
    name = ""
    value = ""

    pos = from_pos

    def _get_next_char():
        return None if len(raw) < pos + 2 else raw[pos + 1]

    for pos, c in enumerate(raw[from_pos:], from_pos):  # type: int, str
        next_char = _get_next_char()

        if skip_next is True:
            skip_next = False
            continue

        if found_name:
            if c == value_quote_type:
                if next_char is not None and raw[pos + 1] not in WHITE_SPACE_CHARS:
                    raise InvalidValueError(name)
                found_value = True
                break
            value += c
        else:
            if c == "=":
                found_name = True
                if next_char is None or raw[pos + 1] not in "\"'":
                    raise InvalidValueError(name)
                value_quote_type = raw[pos + 1]
                skip_next = True
            # If we didn't find the name yet but reached the end of the attribute.
            elif next_char is None:
                return name + c, True, pos
            elif name and c in WHITE_SPACE_CHARS:
                return name, True, pos
            else:
                name += c

    if not found_name:
        return None, None, pos

    if not found_value:
        raise InvalidValueError(name)

    return name, value, pos


def parse_attributes(raw):
    """
    Parses a raw string attribute list to a dict.

    Example usages:
        >>> parse_attributes("href='https://example.com/' target='_blank'")
        >>> # {"href": "https://example.com/", "target": "_blank"}
        >>>
        >>> parse_attributes("title='hello' checked")
        >>> # {"title": "hello", "checked": True}

    :param raw:
    :type raw: str

    :return: The parsed attributes as a dictionary.
    :rtype: Dict[str, Union[bool, str]]
    """
    results = {}
    cursor_pos = 0

    while True:
        current_part = raw[cursor_pos:]
        stripped_part = current_part.lstrip()
        cursor_pos += len(current_part) - len(stripped_part)

        name, value, cursor_pos = _get_next_attribute(cursor_pos, raw)

        if name is None:
            return results

        results[name] = value
        cursor_pos += 1
