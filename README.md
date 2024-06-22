# mkdocs-badges
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-badges)](https://pypi.org/project/mkdocs-badges/)
![License](https://img.shields.io/pypi/l/mkdocs-badges)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-badges)

This package allows you to add badges to your MkDocs site.

## Documentation

This README is just a short intro to the package.
For a quick start and detailed information please see the [documentation](https://mkdocs-badges.six-two.dev/).
The documentation is also available in the `docs` folder of the source code and can be built locally with [MkDocs](https://www.mkdocs.org/).

A development version built with the latest changes (`HEAD` commit) can be found at <https://mkdocs-badges-dev.six-two.dev/>.

## Testing

The documentation also serves as a test of the plugin, especially the files under the `Tests` menu item.

Build the documentation with the latest source code:
```bash
pip install . && mkdocs serve -t <theme>
```

Themes that should work are `mkdocs`, `readthedocs`, and `material`.

### Unit tests

The GitHub repository now contains some unit test.
You can run them against the current code with the following command (issued in the root directory of the repository):

```bash
pip install . && python -m unittest
```

## Known issues

- At least on iPhones (which only support Safari based engines) only one toast can be shown.
    After that you need to reload the page to show the same toast again or to show another toast.
    This seems to be an issue with <https://github.com/mlcheng/js-toast/> (used in `src/mkdocs_badges/assets/badge.js`) which seems no longer maintained.

## Notable changes

### Head

- Changed behavior of the `install_badge_data` option.
    Instead of removing the defaults the specified file is merged with them
- Changed install badge data.
    Renamed `brew` to `brew_formula` and added `brew_cask`, `docker_hub`, and `docker_ghcr`
- Fixed crash of JavaScript copy code if the text contains a single quote

### Version 0.4.2

- Detect markdown tables even if they have only a single dash in the header. Fixes [#4](https://github.com/six-two/mkdocs-badges/issues/4)
- Option to disable warnings (use this at your own risk) by adding `disable_warnings: True` to the plugin config in your `mkdocs.yml`

### Version 0.4.1

- Now requires MkDocs 1.5 or newer
- The included script is now marked as `async` by default, maybe improving loading times a tiny bit. This can be disabled by adding `async: False` to the plugin config in your `mkdocs.yml`

### Version 0.4.0

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
