import logging

from html_to_draftjs import utils

XML_TAG_START = "<"
XML_TAG_END = ">"
XML_CLOSED_TAG = "/"
XML_WHITE_LISTED_CHARS = "\"'"  # characters to ignore inside of a tag

logger = logging.getLogger(__name__)

__all__ = ["Tag"]


class Tag(object):
    __slots__ = ("name", "inner_html", "attributes")

    def __init__(self, name, inner_html=None, attributes=None):
        self.name = name.lower()  # type: str
        self.attributes = attributes if attributes is not None else {}  # type: dict
        self.inner_html = inner_html if inner_html is not None else ""  # type: str

    def __repr__(self):
        return "<{self.name}>{self.inner_html}</{self.name}>".format(self=self)

    def _get_tag(
        self,
        tag_name,
        opening_start_pos,
        opening_end_pos,
        closing_tag_end_pos=None,
        has_inner=False,
    ):
        tag_name = tag_name.rstrip("\0")  # remove NUL

        attributes = self.inner_html[opening_start_pos:opening_end_pos]
        attributes = utils.parse_attributes(attributes)

        inner_html = None
        if has_inner:
            # 2 => `</`
            inner_start = opening_end_pos + 1
            inner_stop = closing_tag_end_pos - len(tag_name) - len("</")
            inner_html = self.inner_html[inner_start:inner_stop]
            inner_html = inner_html.strip()

        return Tag(name=tag_name, attributes=attributes, inner_html=inner_html)

    def next(self, start_pos):
        """
        :rtype
        :param pos: The starting position.

        :return: The content retrieved, the text or the tag and the stop position.
        :rtype: Tuple[str, Union[str, Tag], int]
        """
        text = ""

        tag_opening_start_pos = None
        tag_opening_end_pos = None
        tag_name = ""
        pos = start_pos
        for pos, char in enumerate(self.inner_html[pos:], pos):
            if char == XML_TAG_START:
                if tag_opening_start_pos is None:
                    logger.debug("Entered Tag at %d", pos)
                    tag_opening_start_pos = pos

            elif tag_opening_start_pos is not None:
                if char == XML_TAG_END:
                    logger.debug("Found possible end of tag at %d", pos)

                    if tag_opening_end_pos is None:
                        tag_opening_end_pos = pos

                    _possible_tag_start = pos + 1 - len(tag_name)
                    _possible_tag_stop = pos

                    possible_tag_name = self.inner_html[
                        _possible_tag_start:_possible_tag_stop
                    ]

                    # Tag closing without inner
                    if self.inner_html[pos - 1] == "/":
                        tag = self._get_tag(
                            tag_name,
                            tag_opening_start_pos,
                            pos,
                            closing_tag_end_pos=None,
                            has_inner=False,
                        )
                        return text, tag, pos

                    # Tag closing with inner HTML
                    elif possible_tag_name == tag_name.rstrip("\0"):  # noqa
                        tag = self._get_tag(
                            tag_name,
                            tag_opening_start_pos,
                            tag_opening_end_pos,
                            closing_tag_end_pos=pos,
                            has_inner=True,
                        )
                        return text, tag, pos

                # if we didn't retrieve the tag name yet, add the character
                # to the tag name
                elif tag_name[-1:] != "\0":
                    if char in (" ", "\n"):
                        tag_name += "\0"
                    else:
                        tag_name += char

            else:
                text += char

        if tag_opening_start_pos is not None:
            raise ValueError(
                "Did not find a closure for: {}".format(tag_name.rstrip("\0")),
                self.inner_html,
            )

        return text, None, pos

    def __iter__(self):
        """
        Yields the text and each children (of type Tag).

        :rtype: Union[str, Tag]
        :raise: StopIteration
        """
        raise StopIteration
