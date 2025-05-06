# Badge syntax

A badge generally consists of separators (`|`) surrounding a title and a value like this:
```
|title|value|
```

Some special [types of badges](badge-types.md) have a type prefix before the first separator like:
```
L|Link badge|https://example.com|
```

Badges should not have any leading or trailing space (except when in [tables](#badges-in-tables)).
Badges should normally be the only thing in its line or table cell, but starting from version 0.4.6 there is a [new inline syntax](#badges-in-markdown-inline-badges), which allows you to have other contents before or after a badge.

## Badge grouping

If you put multiple badges into consecutive lines, they will be grouped together.
When grouped together, badges are shown in a single line from left to right:

Grouped badges example:
```markdown
|first|badge|
|second|badge|
|third|badge|
```

Result:

<span class=result>
|first|badge|
|second|badge|
|third|badge|
</span>

### Ungrouped badges

If you do not want this behavior, you can add an empty line between the badges.
This will cause every badge to be on its own line:

```markdown
|first|badge|

|second|badge|

|third|badge|
```

Result:

<span class=result>
|first|badge|

|second|badge|

|third|badge|
</span>


## Custom separators

|Required version|0.4.5+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

As shown on the [badge types](badge-types.md) page, badges normally look like `|Title|Value|`.

If you do not like the default separator character (`|`), you can change it in your `mkdocs.yml`:
```yaml
plugins:
- badges:
    separator: "$"
```

Then you can write all badge types shown above this section badges using that character instead of `|`.
Ideally you choose an character that never appears in any badge text or value.
If it does, you can escape it by prefixing it with a backslash like `\$`.

Example markdown:
```
$Example badge$works$
I$github$six-two/mkdocs-badges$
S$Single element badge$$
$Styled differently$by custom HTML classes$class:version$
$Price$5\$$
```

Result:

<!-- Yeah, this is cheating, but I can not change the separator for a piece of a page -->
<span class=result>
|Example badge|works|
I|github|six-two/mkdocs-badges|
S|Single element badge||
|Styled differently|by custom HTML classes|class:version|
|Price|5$|
</span>


## Badges in tables

|Required version|0.4.5+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

Badges in tables work similar to normal badges, but use a different separator (`^` instead of `|`) by default.
This is to prevent conflict with the markdown table syntax, which also uses the `|` character.
You can change the separator character with the `table_separator` property in your `mkdocs.yml`:
```yaml
plugins:
- badges:
    table_separator: "+"
```

Due to the current implementation a badge has to be alone in a cell.
If you add any non-whitespace before or after the badge, it will not be parsed.

If you want to use literal `^` or `|` characters inside a badge in a table, you need to backslash escape them (`\^` or `\|`).

Example markdown:
```markdown
| Some                                   | Markdown                     | Table       |
| -------------------------------------- | ---------------------------- | ----------- |
| some row                               | without                      | badges      |
| ^badge^normal^                         | L^badge^https://example.com^ | normal cell |
| text before ^badge^will break badge^   | ^badge with carets^\^_\^^    | normal cell |
| ^badge^will break^ with trailing text  | ^badge with pipes^a \|\| b^  | normal cell |
```

Result:

| Some                                   | Markdown                     | Table       |
| -------------------------------------- | ---------------------------- | ----------- |
| some row                               | without                      | badges      |
| ^badge^normal^                         | L^badge^https://example.com^ | normal cell |
| text before ^badge^will break badge^   | ^badge with carets^\^_\^^    | normal cell |
| ^badge^will break^ with trailing text  | ^badge with pipes^a \|\| b^  | normal cell |

<!-- Link references -->
[example_ref]: https://www.example.com

<!-- Footnotes -->
[^1]: There is a difference, in that a badge like a link (L) or reflink (R) badge have the link cover the entire badge. So it will also trigger, if you click the left side. For the similar normal badges, only the right side is part of the link.

## Badges in Markdown (inline badges)

|Required version|0.4.6+|link:https://github.com/six-two/mkdocs-badges#notable-changes|.version|

By default, badges are only parsed if they are the only thing in its line (or table cell).
This causes problems if you want multiple badges inside a table cell or if you want to use badges in Markdown syntax like lists, links, etc.

If you want to use badges in such a situation, you can use the inline badge syntax.
It works by putting a special prefix before the start of the badge and a special syntax after the end of the badge.
By default, the prefix is `[` and the suffix is `]`, so an inline badge would look like:

```
Text before badge, [|Inline|badge|], and some trailing text.
```

<span class=result>
Text before badge, [|Inline|badge|], and some trailing text.
</span>

This allows you to for example use multiple badges in a single table cell or use badges in Markdown lists:

```
- [|first|badge|] [|second|badge|]
- [L|third badge|https://example.com|]
- [[|manual link badge|https://trustworthy.com|]](https://evil.example.com)

Some|Table
---|---
soccer | [^game length^90min^] [^most common score^0:0^] [L^Wikipedia^https://en.wikipedia.org/wiki/Association_football^]
```

- [|first|badge|] [|second|badge|]
- [L|third badge|https://example.com|]
- [[|manual link badge|https://trustworthy.com|]](https://evil.example.com)

Some|Table
---|---
soccer | [^game length^90min^] [^most common score^0:0^] [L^Wikipedia^https://en.wikipedia.org/wiki/Association_football^]

### Custom prefix and suffix

The brackets may conflict with some Markdown syntax.
If it does, you can change the prefix and suffix strings with the following properties in your `mkdocs.yml`:
```yaml
plugins:
- badges:
    inline_badge_start: "<"
    inline_badge_end: ">"
```

Then you can make badges like:
```
- <|Inline badge|with different prefix and suffix|>
```

<!-- I have to cheat again, but the tests page checks these cases sometimes -->
- [|Inline badge|with different prefix and suffix|]

## Badges in Listings

Are not supported by design.

