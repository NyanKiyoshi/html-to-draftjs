import bs4

from html_to_draftjs.converter import SoupConverter


def html_to_draftjs(html, features="lxml", strict=False):
    soup = bs4.BeautifulSoup(html, features)
    return SoupConverter(strict=strict).convert(soup).to_dict()


def soup_to_draftjs(soup: bs4.BeautifulSoup, strict=False):
    return SoupConverter(strict=strict).convert(soup).to_dict()
