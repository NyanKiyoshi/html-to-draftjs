import mock
import pytest

from html_to_draftjs.pyxml import Tag
from html_to_draftjs.utils import InvalidValueError, parse_attributes


def test_get_inner_text_without_tags():
    html = " Hi :) "
    root = Tag("root", html)
    text, tag, stopped_at = root.next(0)  # type: (str, Tag, int)

    # Check tag
    assert tag is None, "Not tag should have been found"

    # Check pos
    assert stopped_at == len(html) - 1

    # Check text
    assert text == html, "Should have found the text"


@mock.patch("html_to_draftjs.utils.parse_attributes", wraps=parse_attributes)
def test_get_tag_with_inner(mocked_attribute_parser):
    html = "<a href='hello world'> Hi :) </a>"
    root = Tag("root", html)
    text, tag, stopped_at = root.next(0)  # type: (str, Tag, int)

    # Check tag
    assert tag is not None, "Should have returned a tag"
    assert tag.name == "a", "The tag should have been a hyperlink"
    assert tag.inner_html == "Hi :)", "The inner HTML should have been raw + stripped"

    # Check attributes
    mocked_attribute_parser.assert_called_once_with("href='hello world'")
    assert tag.attributes == {"href": "hello world"}

    # Check pos
    assert stopped_at == len(html) - 1

    # Check text
    assert text == "", "Should not have found any text"


@pytest.mark.parametrize("html", ("<img src='abc'/>", "<img src='abc' />"))
@mock.patch("html_to_draftjs.utils.parse_attributes", wraps=parse_attributes)
def test_get_tag_without_inner(mocked_attribute_parser, html):
    root = Tag("root", html)
    text, tag, stopped_at = root.next(0)  # type: (str, Tag, int)

    # Check tag
    assert tag is not None, "Should have returned a tag"
    assert tag.name == "img", "The tag should have been a image"
    assert tag.inner_html == "", "The inner HTML should be empty"

    # Check attributes
    mocked_attribute_parser.assert_called_once_with("src='abc'")
    assert tag.attributes == {"src": "abc"}

    # Check pos
    assert stopped_at == len(html) - 1

    # Check text
    assert text == "", "Should not have found any text"


@pytest.mark.parametrize(
    "raw_input, expected",
    (
        ("href='abc'", {"href": "abc"}),
        ('href="abc"', {"href": "abc"}),
        ("src='hello' href=\"abc\"", {"src": "hello", "href": "abc"}),
        ("a='1'     b='2'", {"a": "1", "b": "2"}),
        ("a='1'\nb='2'", {"a": "1", "b": "2"}),
        ("a", {"a": True}),
        ("a b src='hello'", {"a": True, "b": True, "src": "hello"}),
        ("a=''", {"a": ""}),
    ),
)
def test_parse_attributes(raw_input, expected):
    results = parse_attributes(raw_input)
    assert results == expected


@pytest.mark.parametrize(
    "raw_input",
    ("href='abc\"", "href=abc", "href=", "href= hello", "href='abc'invalid"),
)
def test_parse_attributes_with_invalid_values(raw_input):
    with pytest.raises(InvalidValueError) as exc:
        print(parse_attributes(raw_input))
    assert exc.value.args == ("Invalid value for the attribute (href)",)
