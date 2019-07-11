import warnings
from typing import Dict, Optional  # noqa: F401

from bs4 import BeautifulSoup
from bs4.element import Tag

from html_to_draftjs import types

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

        # -- The generated entity map for DraftJS
        # The cursor for types
        self._entity_cursor = None  # type: Optional[int]

        # the defined types (images, links, etc.)
        self._entities = None  # type: Optional[dict]

        # the defined blocks (p, div, etc.)
        self._blocks = None  # type: Optional[list]

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
        self._blocks = []

    def _process_element_for_block(
        self, block, element: Tag, parent_element: Optional[Tag]
    ):
        for node in element.contents:
            # If the node is a string, append it to the text
            if isinstance(node, str):
                block["text"] += node
                continue

            tag_name = node.name.lower()

            # If the node is a block, build a block
            if tag_name in self.blocks_types or tag_name in self.typed_blocks_types:
                if (
                    parent_element is not None
                    and parent_element.name in self._all_inline_tags
                ):
                    self.dispatch_error(
                        "Doesn't support blocks within a inline tag (invalid)",
                        tag_name,
                        node,
                        parent_element,
                    )
                    continue

                # Build the block
                self.build_block(node)

                # Stop there, we don't need to post-process blocks
                continue

            # Check if the node is a inline tag, then
            if tag_name not in self._all_inline_tags:
                self.dispatch_error("Unsupported tag in block", tag_name, node)
                continue

            # Process the inline tags
            start_pos = len(block["text"])
            self._process_element_for_block(block, node, element)
            end_pos = len(block["text"])

            length = end_pos - start_pos

            if tag_name in self.entities_types:
                self.build_entity(node, block, start_pos, length)
            else:
                self.handle_inline(node, block, start_pos, length)

    def build_block(self, element):
        """
        :param element:
        :type element: Tag

        :return:
        """

        # FIXME: handle typed blocks here

        # Create and store an empty block, ready to get populated
        block = self.create_default_block()
        self.append_block(block)

        # Convert the HTML content to DraftJS
        self._process_element_for_block(block, element, None)

        # Finalize the block data
        block["key"] = self.key_generator(block)

    def handle_inline(self, node: Tag, current_block, start_pos, length):
        """
        :param current_block: The block being processed.
        :type current_block: dict

        :return:
        """
        if length == 0:
            self.dispatch_error("Inline styles cannot have empty inner", node)
            return

        styles = current_block["inlineStyleRanges"]
        styles.append(
            {
                "offset": start_pos,
                "length": length,
                "style": self.inlines_types[node.name.lower()],
            }
        )

    @staticmethod
    def build_typed_block(current_block):
        """
        :param current_block: The block being processed.
        :type current_block: dict

        :return:
        """

    def build_entity(self, node: Tag, current_block, start_pos, length):
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
        :type args: Any

        :return:
        """
        if self.strict:
            raise ValueError(msg, *args)
        self.warn("{}: {}".format(msg, repr(args)))

    def clean_block(self):
        blocks_to_remove = [block for block in self._blocks if block["text"] == ""]

        for block in blocks_to_remove:
            self._blocks.remove(block)

        for block in self._blocks:
            block["inlineStyleRanges"] = list(
                sorted(block["inlineStyleRanges"], key=lambda o: o["offset"])
            )

    def to_dict(self):
        self.clean_block()

        return {"entityMap": self._entities, "blocks": self._blocks}

    def convert(self, soup: BeautifulSoup):
        """
        Converts the passed bs4 soup into a standard Draft JS JSON format
        as a python dictionary.

        :param soup:
        :type soup: BeautifulSoup

        :return:
        :rtype: SoupConverter
        """

        # Populate the session
        self.initialize_session_converter()

        body = soup.select_one("body")  # type: Optional[Tag]

        if not Tag:
            return self

        self.build_block(body)
        return self
