import pytest

from html_to_draftjs.pyxml import Tag


def test_get_tag_with_inner():
    html = "<a href='hello world'> Hi :) </a>"
    root = Tag("root", html)
    text, tag, stopped_at = root.next(0)  # type: (str, Tag, int)

    # Check tag
    assert tag is not None, "Should have returned a tag"
    assert tag.name == "a", "The tag should have been a hyperlink"
    assert tag.inner_html == "Hi :)", "The inner HTML should have been raw + stripped"

    # TODO: check attributes
    "..."

    # Check pos
    assert stopped_at == len(html) - 1

    # Check text
    assert text == "", "Should not have found any text"


@pytest.mark.parametrize("html", ("<img src='abc'/>", "<img src='abc' />"))
def test_get_tag_without_inner(html):
    root = Tag("root", html)
    text, tag, stopped_at = root.next(0)  # type: (str, Tag, int)

    # Check tag
    assert tag is not None, "Should have returned a tag"
    assert tag.name == "img", "The tag should have been a image"
    assert tag.inner_html == "", "The inner HTML should be empty"

    # TODO: check attributes
    "..."

    # Check pos
    assert stopped_at == len(html) - 1

    # Check text
    assert text == "", "Should not have found any text"
