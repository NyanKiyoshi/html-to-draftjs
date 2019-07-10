import warnings

from html_to_draftjs import types
from html_to_draftjs.pyxml import Tag

try:
    from typing import Any, Union, Callable, Dict, Tuple  # noqa
except ImportError:
    """Un-supported import for Python < 3.6"""


__all__ = ["SoupConverter"]


class SoupConverter(object):
    def __init__(
        self,
        strict=False,
        key_generator=lambda tag: "",
        inlines=types.INLINE_TAGS,
        blocks=types.BLOCK_TAGS,
        typed_blocks=types.TYPED_TAGS,
        entities=types.ENTITIES,
        default_block_tag_name=None,
    ):
        """
        Handles a HTML soup (beautifulsoup4) to convert it to Draft JS's JSON format.

        :param strict: Whether unsupported tags or structures should raise an error.
        :type strict: bool

        :param key_generator:
            The key generator. Called every time a block key must be generated,
            it takes the generated DraftJS block dictionary as parameter.
            By default, it returns an empty key (no key), which is valid for DraftJS.
        :type key_generator: Callable[Dict[str, Any]]

        :param inlines:
        :type inlines: Dict[str, str]

        :param blocks:
        :type blocks: tuple

        :param typed_blocks:
        :type typed_blocks: Dict[str, str]

        :param entities:
        :type entities: Dict[str, types.ENTITY_TYPE]

        :param default_block_tag_name: The tag for blocks to wrap invalid HTML structure
            that has inline tags as root element.
        :type default_block_tag_name: str
        """

        self.strict = strict
        self.key_generator = key_generator

        self.inlines_types = inlines
        self.blocks_types = blocks
        self.typed_blocks_types = typed_blocks
        self.entities_types = entities
        self.default_block_tag_name = default_block_tag_name or self.blocks_types[0]

        # Contains all the tags that are inline
        self._all_inline_tags = set()
        self._all_inline_tags.update(self.inlines_types.keys())
        self._all_inline_tags.update(self.entities_types.keys())

        # The generated entity map for DraftJS
        self._entity_cursor = None  # The cursor for types
        self._entities = None  # the defined types (images, links, etc.)
        self._blocks = None  # the defined blocks (p, div, etc.)

    @staticmethod
    def create_default_block():
        return {
            "key": "",
            "text": "",
            "type": "unstyled",
            "depth": 0,
            "inlineStyleRanges": [],
            "entityRanges": [],
            "data": {},
        }

    def append_entity(self, entity):
        """
        Appends an entity to the current session and increment the key cursor.

        :param entity:
        :type: dict

        :return: The key of the entity,
        :rtype: str
        """
        key = str(self._entity_cursor)
        self._entity_cursor += 1
        self._entities[key] = entity
        return key

    def append_block(self, block_data):
        self._blocks.append(block_data)

    def initialize_session_converter(self):
        """Initialize the session to zero."""
        self._entity_cursor = 0
        self._entities = {}
        self._blocks = {}

    def build_block(self, element):
        """
        :param element:
        :type element: Tag

        :return:
        """

        # Create an empty block, ready to get populated
        block = self.create_default_block()

        # Convert the HTML content to DraftJS
        "..."

        # Finalize the data
        block["key"] = self.key_generator(block)

        # Store the generated block
        self.append_block(block)

    def handle_inline(self, current_block):
        """
        :param current_block: The block being processed.
        :type current_block: dict

        :return:
        """

    def build_typed_block(self, current_block):
        """
        :param current_block: The block being processed.
        :type current_block: dict

        :return:
        """

    def build_entity(self, current_block):
        """
        :param current_block: The block being processed.
        :type current_block: dict

        :return:
        """

        entity = {}
        key = self.append_entity(entity)
        assert key

    def dispatch_tag(self):
        pass

    @staticmethod
    def warn(msg):
        warnings.warn(msg)

    def dispatch_error(self, msg, *args):
        """
        Dispatch an error caused by an unhandled event.

        - If the converter was called in strict mode, it will raise a ValueError.
        - If the converter is not in strict mode (default), it will ignore the error
          and simply generate a warning.

        :param msg:
        :type msg: str

        :param args:
        :type args: tuple

        :return:
        """
        if self.strict:
            raise ValueError(msg, *args)
        self.warn("{}: {}".format(msg, repr(args)))

    def convert(self, soup):
        """
        Converts the passed bs4 soup into a standard Draft JS JSON format
        as a python dictionary.

        :param soup:
        :type soup: BeautifulSoup

        :return:
        :rtype: dict
        """

        # Populate the session
        self.initialize_session_converter()

        while soup.tagStack:
            element = soup.popTag()  # type: Tag

            # Check if the current root tag is inline (invalid HTML structure).
            # If it is inline, we have to give it a block parent to properly handle it.
            if element.name in self._all_inline_tags:
                # Inject a block parent to the invalid inline tag
                parent = Tag(name=self.default_block_tag_name)
                parent.append(element)

                element = parent

            self.build_block(element)
