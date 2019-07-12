from pprint import pprint

import pytest

from html_to_draftjs import html_to_draftjs

# FIXME: test typed blocks as well


def test_convert_block():
    """Tests converting inline HTML contained into a block."""
    html = "<p>My content has <strong>some <em>content</em></strong></p>"
    json = html_to_draftjs(html, strict=True)
    assert json == {
        "entityMap": {},
        "blocks": [
            {
                "key": "",
                "text": "My content has some content",
                "type": "unstyled",
                "depth": 0,
                "inlineStyleRanges": [
                    {"offset": 15, "length": 12, "style": "BOLD"},
                    {"offset": 20, "length": 7, "style": "ITALIC"},
                ],
                "entityRanges": [],
                "data": {},
            }
        ],
    }


def test_convert_inline():
    """Tests converting ** HTML structure, where inline tags are not
    in a block tag."""
    html = (
        "My content has <strong>some <em>content</em></strong>"
        "<p>A paragraph here</p>"
    )
    json = html_to_draftjs(html)
    assert json == {
        "entityMap": {},
        "blocks": [
            {
                "key": "",
                "text": "My content has some content",
                "type": "unstyled",
                "depth": 0,
                "inlineStyleRanges": [
                    {"offset": 15, "length": 12, "style": "BOLD"},
                    {"offset": 20, "length": 7, "style": "ITALIC"},
                ],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "A paragraph here",
                "type": "unstyled",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
        ],
    }


@pytest.mark.parametrize(
    "html, expected",
    (
        (
            "<img src='picture.png' />",
            {
                "entityMap": {
                    "0": {
                        "type": "IMAGE",
                        "mutability": "MUTABLE",
                        "data": {
                            "alt": "",
                            "src": "picture.png",
                            "height": "initial",
                            "width": "initial",
                        },
                    }
                },
                "blocks": [
                    {
                        "key": "",
                        "text": "",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [],
                        "entityRanges": [{"offset": 0, "length": 0, "key": 0}],
                        "data": {},
                    }
                ],
            },
        ),
        (
            "<p><img src='picture.png' /><img src='picture2.png' /></p>",
            {
                "entityMap": {
                    "0": {
                        "type": "IMAGE",
                        "mutability": "MUTABLE",
                        "data": {
                            "alt": "",
                            "src": "picture.png",
                            "height": "initial",
                            "width": "initial",
                        },
                    },
                    "1": {
                        "type": "IMAGE",
                        "mutability": "MUTABLE",
                        "data": {
                            "alt": "",
                            "src": "picture2.png",
                            "height": "initial",
                            "width": "initial",
                        },
                    },
                },
                "blocks": [
                    {
                        "key": "",
                        "text": "",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [],
                        "entityRanges": [
                            {"offset": 0, "length": 0, "key": 0},
                            {"offset": 0, "length": 0, "key": 1},
                        ],
                        "data": {},
                    }
                ],
            },
        ),
        (
            "<p><img src='picture.png'>Invalid</img></p>",
            {
                "entityMap": {
                    "0": {
                        "type": "IMAGE",
                        "mutability": "MUTABLE",
                        "data": {
                            "alt": "",
                            "src": "picture.png",
                            "height": "initial",
                            "width": "initial",
                        },
                    }
                },
                "blocks": [
                    {
                        "key": "",
                        "text": "Invalid",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [],
                        "entityRanges": [{"offset": 0, "length": 0, "key": 0}],
                        "data": {},
                    }
                ],
            },
        ),
        (
            "<p><img src='picture.png' alt='my picture' height='255' /></p>",
            {
                "entityMap": {
                    "0": {
                        "type": "IMAGE",
                        "mutability": "MUTABLE",
                        "data": {
                            "alt": "my picture",
                            "src": "picture.png",
                            "height": "255px",
                            "width": "initial",
                        },
                    }
                },
                "blocks": [
                    {
                        "key": "",
                        "text": "",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [],
                        "entityRanges": [{"offset": 0, "length": 0, "key": 0}],
                        "data": {},
                    }
                ],
            },
        ),
    ),
)
def test_convert_image(html, expected):
    """Tests converting a image tag into JSON."""
    json = html_to_draftjs(html, strict=True)
    assert json == expected


@pytest.mark.parametrize(
    "html",
    (
        "hello <a href='#my-link'>worl<strong>d</strong></a>",
        "<p>hello <a href='#my-link'>worl<strong>d</strong></a></p>",
    ),
)
def test_convert_link(html):
    """Tests converting HTML links into JSON."""
    json = html_to_draftjs(html, strict=True)
    assert json == {
        "entityMap": {
            "0": {"type": "LINK", "mutability": "MUTABLE", "data": {"href": "#my-link"}}
        },
        "blocks": [
            {
                "key": "",
                "text": "hello world",
                "type": "unstyled",
                "depth": 0,
                "inlineStyleRanges": [{"offset": 10, "length": 1, "style": "BOLD"}],
                "entityRanges": [{"offset": 6, "length": 5, "key": 0}],
                "data": {},
            }
        ],
    }


@pytest.mark.parametrize(
    "html, expected_type",
    (
        ("<h1>My content</h1>", "header-one"),
        ("<blockquote>My content</blockquote>", "blockquote"),
    ),
)
def test_convert_typed_block(html, expected_type):
    """Tests converting HTML links into JSON."""
    json = html_to_draftjs(html, strict=True)
    assert json == {
        "entityMap": {},
        "blocks": [
            {
                "key": "",
                "text": "My content",
                "type": expected_type,
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            }
        ],
    }


@pytest.mark.parametrize(
    "html, expected_type",
    (
        ("<ul><li>a</li><li>b</li></ul>", "unordered-list-item"),
        ("<ol><li>a</li><li>b</li></ol>", "ordered-list-item"),
    ),
)
def test_convert_typed_block_list(html, expected_type):
    """Tests converting HTML links into JSON."""
    json = html_to_draftjs(html, strict=True)
    assert json == {
        "entityMap": {},
        "blocks": [
            {
                "key": "",
                "text": "a",
                "type": expected_type,
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "b",
                "type": expected_type,
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
        ],
    }


def test_convert_page():
    """Tests converting a full dummy HTML page into JSON.

    This covers all the cases, which are:
        - Titles
        - Blockquotes
        - Images
        - Links
        - Inline formatting
        - Ordered lists
        - Unordered lists
    """

    html = """
        <h1>HTML Ipsum Presents</h1>

        <p><strong>Pellentesque habitant morbi tristique</strong> senectus et netus.</p>

        <h2>Header Level 2</h2>

        <ol>
           <li>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</li>
           <li>Aliquam tincidunt mauris eu risus.</li>
        </ol>

        <blockquote>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        </blockquote>

        <h3>Header Level 3</h3>

        <ul>
           <li>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</li>
           <li>Aliquam tincidunt mauris eu risus.</li>
        </ul>
    """

    json = html_to_draftjs(html, strict=True)
    pprint(json)
    assert json == {
        "entityMap": {},
        "blocks": [
            {
                "key": "",
                "text": "HTML Ipsum Presents",
                "type": "header-one",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Pellentesque habitant morbi tristique senectus et netus.",
                "type": "unstyled",
                "depth": 0,
                "inlineStyleRanges": [{"offset": 0, "length": 37, "style": "BOLD"}],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Header Level 2",
                "type": "header-two",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
                "type": "ordered-list-item",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Aliquam tincidunt mauris eu risus.",
                "type": "ordered-list-item",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "type": "blockquote",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Header Level 3",
                "type": "header-three",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
                "type": "unordered-list-item",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
            {
                "key": "",
                "text": "Aliquam tincidunt mauris eu risus.",
                "type": "unordered-list-item",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
                "data": {},
            },
        ],
    }
