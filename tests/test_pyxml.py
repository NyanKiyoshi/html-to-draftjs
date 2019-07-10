import mock
import pytest

from html_to_draftjs.pyxml import Tag
from html_to_draftjs.utils import InvalidValueError, parse_attributes


def test_get_inner_text_without_tags():
    html = " Hi :) "
    root = Tag("root", html)
    text, stopped_at = root.next(0)  # type: (str, int)

    # Check pos
    assert stopped_at == len(html)

    # Check text
    assert text == html, "Should have found the text"


def test_get_inner_text_with_tags():
    html = "Hello <strong>world</strong>"
    root = Tag("root", html)
    text, stopped_at = root.next(0)  # type: (str, int)

    # Check pos
    assert stopped_at == len("hello ")

    # Check text
    assert text == "Hello ", "Should have found the text"

    tag, stopped_at = root.next(stopped_at)  # type: (Tag, int)
    assert isinstance(tag, Tag)
    assert tag.name == "strong"
    assert tag.inner_html == "world"
    assert tag.attributes == {}


def test_get_nested():
    html = "<p><strong>world</strong></p>"
    root = Tag("root", html)
    tag, stopped_at = root.next(0)  # type: (Tag, int)

    # Check pos
    assert stopped_at == len(html)

    # Check tag
    assert isinstance(tag, Tag)
    assert tag.name == "p"
    assert tag.inner_html == "<strong>world</strong>"
    assert tag.attributes == {}


def test_name_collision():
    html = "<p><stronp>world</stronp></p>"
    root = Tag("root", html)
    tag, stopped_at = root.next(0)  # type: (Tag, int)

    # Check pos
    assert stopped_at == len(html)

    # Check tag
    assert isinstance(tag, Tag)
    assert tag.name == "p"
    assert tag.inner_html == "<stronp>world</stronp>"
    assert tag.attributes == {}


@mock.patch("html_to_draftjs.utils.parse_attributes", wraps=parse_attributes)
def test_get_tag_with_inner(mocked_attribute_parser):
    html = "<a href='hello world'> Hi :) </a>"
    root = Tag("root", html)
    tag, stopped_at = root.next(0)  # type: (Tag, int)

    # Check tag
    assert tag is not None, "Should have returned a tag"
    assert tag.name == "a", "The tag should have been a hyperlink"
    assert tag.inner_html == "Hi :)", "The inner HTML should have been raw + stripped"

    # Check attributes
    mocked_attribute_parser.assert_called_once_with("href='hello world'")
    assert tag.attributes == {"href": "hello world"}

    # Check pos
    assert stopped_at == len(html)


@pytest.mark.parametrize("html", ("<img src='abc'/>", "<img src='abc' />"))
@mock.patch("html_to_draftjs.utils.parse_attributes", wraps=parse_attributes)
def test_get_tag_without_inner(mocked_attribute_parser, html):
    root = Tag("root", html)
    tag, stopped_at = root.next(0)  # type: (Tag, int)

    # Check tag
    assert tag is not None, "Should have returned a tag"
    assert tag.name == "img", "The tag should have been a image"
    assert tag.inner_html == "", "The inner HTML should be empty"

    # Check attributes
    mocked_attribute_parser.assert_called_once_with("src='abc'")
    assert tag.attributes == {"src": "abc"}

    # Check pos
    assert stopped_at == len(html)


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


def test_root_tag_iterator():
    html = "<p>Hello to <strong><em>our</em>World <em>:)</em></strong></p>"
    tag = Tag(name="body", attributes={}, inner_html=html)

    nodes = list(tag)
    assert len(nodes) == 1, nodes
    assert nodes[0][0].name == "p"

    nodes = list(nodes[0][0])
    assert len(nodes) == 2, nodes

    text, tag = nodes
    assert text == ("Hello to ", 9)
    assert tag[0].name == "strong"
    assert tag[0].inner_html == "<em>our</em>World <em>:)</em>"
    assert tag[1] == 55

    nodes = list(tag[0])
    assert len(nodes) == 3

    tag1, text, tag2 = nodes
    assert tag1[0].name == "em"
    assert tag1[0].inner_html == "our"
    assert tag1[1] == 12

    assert text[0] == "World "
    assert text[1] == 18

    assert tag2[0].name == "em"
    assert tag2[0].inner_html == ":)"
    assert tag2[1] == 29

    nodes = list(tag2[0])
    assert len(nodes) == 1
    assert nodes[0][0] == ":)"
    assert nodes[0][1] == 2
