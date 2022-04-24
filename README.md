# mkdocs-badges
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-badges)](https://pypi.org/project/mkdocs-badges/)
![License](https://img.shields.io/pypi/l/mkdocs-badges)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-badges)

This package allows you to add badges to your mkdocs site.

## Setup

Install the plugin using pip:

```bash
pip install mkdocs-badges
```

Then, add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - badges
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

More information about plugins in the [MkDocs documentation](http://www.mkdocs.org/user-guide/plugins/).

## Usage

Badges are defined like this:

```
|@github:six-two/mkdocs-badges|
|@pip:mkdocs-badges|
|"Badge name":badge value|
|"Height":N/A|
```

This should create badges that look like this (actual colors will depend on your theme):

![Screenshot of badges](badges_screenshot.png)

There are different types of badges.

### Normal badges

Normal badges use the syntax `|"Name":value|`.
They just render a badge, but do not react to clicks.
If you want to link to something, you can put the badge in a link like this:

```
[|"Github":mkdocs-badges|](q)
```

### Install badges

Install badges can be used to tell users how to install software.
They are defined like this:

```
|@github:six-two/mkdocs-badges|
```

Clicking on the badge name `Github` will copy the command used to install the software (`git clone https://github.com/six-two/mkdocs-badges`).
Clicking on the badge's value `six-two/mkdocs-badges` will bring the user to the package's site (`https://github.com/six-two/mkdocs-badges`).

The currently supported badge names can be seen in `src/mkdocs_badges/assets/install_badge_data.json`.
You can define also your own badge data and use the `install_badge_data` setting to use it as your data file.


## Configuration

Confiruration option | Type | Default value | Description
---|---|---|---
install_badges | bool | `True` | Enables parsing of install badges. Use `False` to not parse them
normal_badges | bool | `True` | Enables parsing of normal badges. Use `False` to not parse them
badge_css | str | `""` | Use a different CSS file for the badges. The given path will be added to `extra_css`, so that it is included on every page. If the file does not exist or an empty value is used, the default CSS is used.
badge_js | str | `""` | Use a different JavaScript file for the badges. The given path will be added to `extra_javascript`, so that it is included on every page. If the file does not exist or an empty value is used, the default JavaScript code is used.
install_badge_data | str | `""` | Load the install badge data from the given file.

