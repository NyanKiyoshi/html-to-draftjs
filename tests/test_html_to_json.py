import pytest


def test_convert_inline():
    """Tests converting *invalid* HTML structure, where inline tags are not
    in a block tag."""
    html = (
        "My content has <strong>some <em>content</em></strong>"
        "<p>A paragraph here</p>"
    )
    assert html


def test_convert_block():
    """Tests converting inline HTML contained into a block."""
    html = "<p>My content has <strong>some <em>content</em></strong></p>"
    assert html


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
