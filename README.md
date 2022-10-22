# mkdocs-badges
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-badges)](https://pypi.org/project/mkdocs-badges/)
![License](https://img.shields.io/pypi/l/mkdocs-badges)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-badges)

This package allows you to add badges to your mkdocs site.

## Documentation

This README is just a short intro to the package.
For a quick start and detailed information please see the [documentation](https://mkdocs-badges.six-two.dev/).
The documentation is also available in the `docs` folder of the source code and can be built localy with [MkDocs](https://www.mkdocs.org/).

## Testing

The documentation also serves as a test of the plugin.
A hidden test page is available at `/test`.

Build the documentation with the latest source code:
```bash
pip install . && mkdocs serve -t <theme>
```

Themes that sould work are `mkdocs`, `readthedocs`, and `material`.

### Unit tests

The github repository now contains some unit test.
You can run them against the current code with the following command (issued in the root directory of the repository):

```bash
pip install . && python -m unittest
```


## Notable changes

### 0.4.0

- Now requires MkDocs 1.4 or newer
- Updated the layout rules for badges. This should better handle oversized contents (like images or very long texts).

### Version 0.3.4

- Added single element badges

### Version 0.3.3

- Added tags badges

### Version 0.3.1

- Better error handling, fixed a crash
- Started adding unit tests

### Version 0.3.0

- Breaking changes to the badges formats. See the [migration guide](https://mkdocs-badges.six-two.dev/migration/)
- Added support for reference links

### Version 0.2.0

- Each badge now needs to be the only thing on its line
- Badges inside code blocks are no longer parsed
- The `|end` at the end of custom badges is no longer neccessary. A simple `|` is enough. This shorter form is recommended from now on.
- Documentation is now in the `docs` folder in the form of a mkdocs website
- Added link badges
