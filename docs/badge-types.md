---
hide:
- tags
---

# Badge Types

There are multiple different badge types, which different syntaxes.
All badges need to be in their now line and have no indent / leading whitespace.
Badges inside (fenced) code blocks are also not interpreted.

If multiple consecutive lines contain badges, they will be displayed next to each other (if space permits it).
If you want each badge to be on its own line, add an empty line between the badges.

## Simple badges

|Required version|0.3.0+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

Simple badges are just a badge that has no special behavior.

Example markdown:

```
|Example badge|works|
```

Result:

<div class=result>
|Example badge|works|
</div>

### Simple badge with link

The left or right side of the badge can also contain valid HTML or markdown content.
So if you want to make a badge that shows a full URL (unlike a `L` badge, which will only show the hostname), you can do something like:
```markdown
|Simple badge with link|<https://github.com/six-two/mkdocs-badges>|
```

Result:

|Simple badge with link|<https://github.com/six-two/mkdocs-badges>|

### Simple badge with multiple links

You can also use normal link syntax and you can put links on both sides of the badge:
```
|[UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)|[f180147f-7c2e-4e4d-bd4e-f4420b90dea0](https://www.uuidtools.com/api/decode/f180147f-7c2e-4e4d-bd4e-f4420b90dea0)|
```

Result:

|[UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)|[f180147f-7c2e-4e4d-bd4e-f4420b90dea0](https://www.uuidtools.com/api/decode/f180147f-7c2e-4e4d-bd4e-f4420b90dea0)|

### Simple badge with image

You can also add HTML or markdown syntax like images as part of a badge.
Example badge markdown:

```
|<img src="https://en.wikipedia.org/favicon.ico" width=15 height=15> Wikipedia page|<a href="https://en.wikipedia.org/wiki/MkDocs">MkDocs</a>|

|Have You Tried|![](https://cdn.sstatic.net/Sites/stackoverflow/Img/favicon.ico) StackOverflow?|
```

|<img src="https://en.wikipedia.org/favicon.ico" width=15 height=15> Wikipedia page|<a href="https://en.wikipedia.org/wiki/MkDocs">MkDocs</a>|

|Have You Tried|![](https://cdn.sstatic.net/Sites/stackoverflow/Img/favicon.ico) StackOverflow?|


## Link badges (L)

|Required version|0.3.0+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|
|Required version for angle brackets|0.4.5+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

Link badges are basically a shortcut for links with badges.
They differ from normal badges with links in that the link's visible text is a (simplified version of) the hostname of the URL.
On the right hand side, you have to specify an URL, optionally surrounded by angle brackets (`<` and `>`), otherwise an error will be thrown.

Example link badges:

```markdown
L|Bug Tracker|https://github.com/six-two/mkdocs-badges/issues|
L|Simplified hostname demo|<https://www.example.com>|
```

This is similar[^1] to the following normal badges:
```markdown
|Bug Tracker|[github.com](https://github.com/six-two/mkdocs-badges/issues)|
|Simplified hostname demo|[example.com](https://www.example.com)|
```

Result:

<div class=result>
L|Bug Tracker|https://github.com/six-two/mkdocs-badges/issues|
L|Simplified hostname demo|<https://www.example.com>|
</div>

## Reference link badges (R)

|Required version|0.3.0+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

Reference link badges (R) are another shortcut, similar to link badges (L).
They differ in that they use reference syntax and show the reference name (not the host name) as value.

Example reflink badge:

```markdown
R|reflink badge|example_ref|

[example_ref]: https://www.example.com
```

This is similar[^1] to the following normal badge:
```markdown
|reflink badge|[example_ref][example_ref]|
```

Result:

<span class=result>
R|reflink badge|example_ref|
</span>

**Warning**: Reference links rely on the underlying markdown parser.
Thus, there badges may not work correctly when inside HTML (like a `<div>` element).
To work around this, make sure markdown parsing inside HTML is enabled, or only put he badges in `<span>` elements, which do (to my knowledge) not prevent the parsing of Markdown contents. If the parsing of reference links fails, the result will look like the following:

<span class=result>
R|reflink badge with non-existing target|example_ref_undefined|
</span>


## Copy badges (C)

|Required version|0.3.0+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

Copy badges copy their value (right side) to the user's clipboard when clicked upon.

Example markdown:

```markdown
C|Password|monkey123|
C|Linux check ethernet settings|ip a s eth0|
```

Result:

<span class=result>
C|Password|monkey123|
C|Linux check ethernet settings|ip a s eth0|
</span>


## Install badges (I)

|Required version|0.3.0+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

Install badges are designed to make it easy for users to install software.
Sadly they are a bit unintuitive to use.
Clicking on the badge title (left side) will copy the command to install the software (`git clone ...`, `pip install ...`, `sudo apt install ...`, etc) to the user's clipboard.
To show them that this is possible, the cursor takes the form of a question mark.
To show them what has happened, a popup is shown once they clicked.

The right side is a link to the software on the given platform (GitHub repo, PyPI page, linux package tracker, etc).

Example markdown:

Markdown code:
```
I|github|six-two/mkdocs-badges|
I|pypi|mkdocs|
```

Result:

<span class=result>
I|github|six-two/mkdocs-badges|
I|pypi|mkdocs|
</span>

### Customizing

A list of currently supported badge types can be found in the `Builtin` section of the [tests page](test/install.md#builtin).
You can define your own install badge types by creating a JSON like the following:
```json
{
    "name_to_use_in_markdown": {
        "title": "Shown name on the badge",
        "link_template": "https://url-that-is-opened/when-the-user-clicks-the-right-side-of-the-badge?value={{value}}",
        "command_template": "install command {{value}}"
    },
    "custom_test": {
        "title": "Custom Install Badge",
        "link_template": "https://example.com/#{{value}}",
        "command_template": "echo '{{value}}'"
    }
}
```

The `{{value}}` placeholder in the `link_template` and `command_template` fields will be replaced with the value that is specified in the markdown.
So for example `I|custom_test|demo_value|` would have the link `https://example.com/#demo_value` and the command to copy `echo 'demo_value'`.

You then use the `install_badge_data` option for the plugin, by setting the following in your `mkdocs.yml`:
```yaml
plugins:
- badges:
    install_badge_data: path/to/your-custom-install-badges.json
```

## Tag badges (T)

|Required version|0.3.3+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

!!! note "Requirements"
    This will likely requires you to use Mkdocs Material and [enabling it's `tags` plugin](https://squidfunk.github.io/mkdocs-material/setup/setting-up-tags/).
    I haven't tested it, but strongly assume that the badges `plugin` will need to be before the `tags` plugin to function properly.

Tag badges add a tag to the page it apears on.
The tags name is derived from the badge's values.
Clicking the badge should open the tags list page at the location where all pages with this tag are listed (assuming ``)

For example the following badge would add the `programming_language_python` tag:
```
T|Programming language|Python|
```

<span class=result>
T|Programming language|Python|
</span>


## Custom badges

|Required version|0.3.0+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

Custom badges offer all features supported by the other badge types (except tag badges).
They have however a more verbose syntax.
On the upside you are in total control about the supplied values, since none of them are automaticaly generated.

Short prefix | Long prefix | Conflicts with | Description
--- | --- | --- | ---
`.` | `class:` | - | Add a class to the badge, which can be used for custom styling. Can be specified multiple time to add multiple classes. Can also be used with any other badge type
`c:` | `copy:` | reflink | Copy the given text when the badge is clicked
`l:` | `link:` | reflink | Clicking on the badge will direct the user to the given URL
`r:` | `reflink:` | copy, link | Similar to link, but instead it uses the reference link syntax

Example markdown:

```markdown
|Link badge equivalent|example.com|link:https://www.example.com|
|Copy badge equivalent|text to show|copy:text to copy|
|Styled differently|by custom HTML classes|class:version|
|Install badge equivalent|mkdocs-badge|link:https://github.com/six-two/mkdocs-badges|copy:git clone https://github.com/six-two/mkdocs-badges.git|
|Reflink badge equivalent|example.com|r:example_ref|
```

Result:

<span class=result>
|Link badge equivalent|example.com|link:https://www.example.com|
|Copy badge equivalent|text to show|copy:text to copy|
|Styled differently|by custom HTML classes|class:version|
|Install badge equivalent|mkdocs-badge|link:https://github.com/six-two/mkdocs-badges|copy:git clone https://github.com/six-two/mkdocs-badges.git|
|Reflink badge equivalent|example.com|r:example_ref|
</span>


## Single element badge

|Required version|0.3.4+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

This badge only contains a single element (the title) and has no second element (the value).
The same extra attributes that can be set for custom badges can also be used here.
However, you can not use a (ref-)link and a text to copy for the same badge, since only one element exists.

Example markdown:
```
S|Single element badge||
S||You can also define the value here|
S|Single element with link||link:https://example.com|
S|Single element with text to copy||copy:single element|
```

Result:

<span class=result>
S|Single element badge||
S||You can also define the value here|
S|Single element with link||link:https://example.com|
S|Single element with text to copy||copy:single element|
</span>
