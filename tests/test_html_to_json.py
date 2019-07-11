import pytest

from html_to_draftjs import html_to_draftjs


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
    assert json == {}


@pytest.mark.parametrize(
    "html, expected",
    (
        ("<img src='picture.png' />", {}),
        ("<p><img src='picture.png' /><img src='picture2.png' /></p>", {}),
        ("<p><img src='picture.png'>Invalid</img></p>", {}),
        ("<p><img src='picture.png' alt='my picture' /></p>", {}),
    ),
)
def test_convert_image(html, expected):
    """Tests converting a image tag into JSON."""


@pytest.mark.parametrize(
    "html, expected",
    (
        ("hello <a href='#my-link'>worl<strong>d</strong></a>", {}),
        ("<p>hello <a href='#my-link'>worl<strong>d</strong></a></p>", {}),
    ),
)
def test_convert_link(html, expected):
    """Tests converting HTML links into JSON."""
    pass


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
    pass
