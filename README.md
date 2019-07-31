<div align='center'>
  <h1>HTML to DraftJS</h1>
  <p>Convert HTML into DraftJS JSON format.</p>
  <p>
    <a href='https://travis-ci.org/NyanKiyoshi/html-to-draftjs/'>
      <img src='https://travis-ci.org/NyanKiyoshi/html-to-draftjs.svg?branch=master' alt='Requirement Status' />
    </a>
    <a href='https://codecov.io/gh/NyanKiyoshi/html-to-draftjs'>
      <img src='https://codecov.io/gh/NyanKiyoshi/html-to-draftjs/branch/master/graph/badge.svg' alt='Coverage Status' />
    </a>
    <a href='https://pypi.python.org/pypi/html-to-draftjs'>
      <img src='https://img.shields.io/pypi/v/html-to-draftjs.svg' alt='Version' />
    </a>
  </p>
  <p>
    <a href='https://github.com/NyanKiyoshi/html-to-draftjs/compare/v1.0.1...master'>
      <img src='https://img.shields.io/github/commits-since/NyanKiyoshi/html-to-draftjs/v1.0.1.svg' alt='Commits since latest release' />
    </a>
    <a href='https://pypi.python.org/pypi/html-to-draftjs'>
      <img src='https://img.shields.io/pypi/pyversions/html-to-draftjs.svg' alt='Supported versions' />
    </a>
    <a href='https://pypi.python.org/pypi/html-to-draftjs'>
      <img src='https://img.shields.io/pypi/implementation/html-to-draftjs.svg' alt='Supported implementations' />
    </a>
  </p>
</div>

## Installation
```
pip install html-to-draftjs
```

## Usage

```python
from html_to_draftjs import html_to_draftjs


json = html_to_draftjs("""
    <h1>My Page</h1>

    <h2>Introduction</h2>

    <p>Some <em>content</em> that is pretty <strong>interesting</strong></p>
    <p>Don't forget to <a href="https://example.com">follow me!</a></p>

    <h2>Illustration</h2>
    <p><img src="https://example.com/image.png" alt="image" /></p>
""")
```

## API
### `html_to_draftjs(raw_html_content: str[, features="lxml", strict=False]) -> dict`
Converts a given HTML input into JSON.

- `features` the features for the HTML tree-builder. By default it is set to `lxml` which is fast and powerful.
- `strict` (boolean), if false, it will only warn on invalid operations. If true, it will raise errors.

### `soup_to_draftjs(bs_object: BeautifulSoup[, strict=False]) -> dict`
Converts a given beautiful soup into JSON. Useful if you have to select a given part of the HTML content to convert it (e.g. `#content`).

- `strict` (boolean), if false, it will only warn on invalid operations. If true, it will raise errors.

## Supported Tags and Attributes

### Blocks
- `<div>`, `<p>`
- `<h1>` ... `<h6>`
- `<blockquote>`
- `<li>` and `<ol>` (doesn't support `<ul>` grouping)
- Doesn't support the `align` attribute.

### Inline Styling
- `<strong>`, `<b>`
- `<em>`, `<i>`

### Entities
- `<img src="url" [alt="alt"] [height="123"] [width="123"]>`
- `<a href="url">`
- `<br/>`
- Doesn't support the `title` and `align` attributes.

## Development
```
./setup.py develop
pip install -r requirements_dev.txt
```
