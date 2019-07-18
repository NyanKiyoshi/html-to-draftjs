from collections import namedtuple
from typing import Optional


def str_value_to_dimension(value: Optional[str]):
    if isinstance(value, str) and value.isnumeric():
        return value + "px"
    return value


ENTITY_TYPE = namedtuple("ENTITY_TYPE", ["type", "attributes"])

# All the HTML tags that should be translated to a given string
TEXT_TAGS = {"br": "\n"}

# All the supported inline styling tag
INLINE_TAGS = {
    # Bold style
    "b": "BOLD",
    "strong": "BOLD",
    # Italic style
    "i": "ITALIC",
    "em": "ITALIC",
}

# All the supported block tag
BLOCK_TAGS = ("p", "div", "ul")

# All the supported block tag having a special type/feature
TYPED_TAGS = {
    # Headers
    "h1": "header-one",
    "h2": "header-two",
    "h3": "header-three",
    "h4": "header-four",
    "h5": "header-five",
    "h6": "header-six",
    # Blockquotes
    "blockquote": "blockquote",
    # Lists
    "li": [
        {"parent": "ul", "type": "unordered-list-item"},
        {"parent": "ol", "type": "ordered-list-item"},
    ],
    "p": [{"parent": "blockquote", "type": "blockquote"}],
    "ol": "",
    "ul": "",
}

# All the supported mutable entities
ENTITIES = {
    # Links
    "a": ENTITY_TYPE(type="LINK", attributes={"href": {"name": "url"}}),
    # Images
    "img": ENTITY_TYPE(
        type="IMAGE",
        attributes={
            "src": {},
            "alt": {"default": ""},
            "height": {"default": "initial", "convert": str_value_to_dimension},
            "width": {"default": "initial", "convert": str_value_to_dimension},
        },
    ),
}
