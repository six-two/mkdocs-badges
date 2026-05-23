# Standalone Preprocessor

If you want to use a different Markdown-based static site generator from ProperDocs / MkDocs, then you can use the included `markdown-badges-standalone` CLI tool.
It takes a folder of Markdown files and replaces all badges found in it with badge HTML.
You can then feed the modified Markdown files into any static site generator, configure it to load the badge resources (one CSS and one optional Javascript file) and you should have badges in your site.

## Using the preprocessor

If you have installed `mkdocs-badges` version 0.6.0 or newer, the `markdown-badges-standalone` tool should be in your PATH.
You can run it like this:

```bash
markdown-badges-standalone --docs path/to/copy/of/docs --copy-resources
```

Theoretically, you could invoke the script before or after the Markdown to HTML conversion.
It was designed to run before the HTML conversion, since otherwise some features such as table detection and code block detection will be broken.

The disadvantage of using it before Markdown conversion is that it modifies the source files, so you may want to copy (or backup) the source files if you run it locally.
If you use CI pipelines (which operate on a copy of your data) that should not be necessary.
One thing I am not sure about is how Zensical or other site generators handle Markdown that is in HTML tags.
For example, the plugin keeps Markdown links you add inside badges so that you can use custom linking plugins.


## Including resources

When you include the `--copy-resources` flag, the JavaScript and CSS needed for badges are copied to your docs directory. The default paths are:

- `assets/javascripts/badge.js`, can be changed with `--js-path`. Only needed if you use copy badges.
- `assets/stylesheets/badge.css`, can be changed with `--css-path`. Needed for all badge types.

You should then reference the files on every page. In `mkdocs` and `properdocs` this can be done using:

```yaml title="mkdocs.yml"
extra_css:
- assets/stylesheets/badge.css

extra_javascript:
- assets/javascripts/badge.js
```

For any other static site generator you want to somehow include the following HTML in each page, preferably in the HTML `<head>` section:
```html title="Include this in the HTML <head> tag"
<script src="assets/javascripts/badge.js"></script>
<style src="assets/stylesheets/badge.css"></style>
```

This could for example be achieved by modifying the basic template, but most site generators should have easier ways.
Please consult the documentation of the software you use.

## Known Issues

### Tag badges do not add tags

Since tags are site generator specific, I can not modify/set them.
While theoretically I could try to write something into the frontmatter (part between `---` and `---` lines at the front of the file), I am not sure if it would cause issues with site generators that do not understand it.
If you have a specific generator that should work with frontmatter, feel free to open an issue and I will check if I can add a switch for that generator.

### Table Detection and Code Listing Detection Do Not Work in HTML Mode

This is to be expected, as the current code looks for Markdown table syntax like table headers (`---|---`) or code listings (indention or ` ``` `).
Doing HTML parsing might be possible with beautifulsoup, but would require extra external dependencies.
If you really need this feature, open an issue and I will see how hard it is to implement.
Or implement it yourself and send me a PR :)
