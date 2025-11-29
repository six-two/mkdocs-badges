# Tests: Inline badges

This works with the following values:
```yaml
separator: "|"
table_separator: "^"
inline_badge_start: "["
inline_badge_end: "]"
```

here is a [|inline|badge|] in the middle of a line

Here is a line that contains the same badge twice

badge 1 ([L|same badge|https://example.com|]), bagge 2 ([L|same badge|https://example.com|])

This is a list of badges:

- [|badge|one|]
- [|badge|two|]
- [|badge|three|]

Table|with|inline badges
---|---|---
cell 1 |cell 2 [^with inline^badge^] in it | cell3
cell 1 |cell 2 [\|with non-working\|inline badge\|] in it | cell3
cell 1 | [^two^badges^] [^one^cell^] | ^normal^badge^
^normal badge^with \| pipe^ | test [^inline^badges \| with \| pipes^] too | cell 3
^normal badge^with \^ caret^ | test [^inline^badges\| with \^ caret^] too | cell 3

!!! note "Admonition"

    L|normal badge|https://in-admonition.example.com/|
    [|inline badge|admonition1|]     [|inline badge|admonition2|]

    This text is part of the admonition


- List item 1 [|works|true|] 
    - List item 1.1 [|works|true|]

Code block:

    Indented code block. Normally should not work, but too hard to detect [|works|sadly yes|]

=== "Tab 1"

    |full badge|works|
    Inline badge [|works|too|]

=== "Tab 2"

    has no badges

## With different mkdocs.yml

This works with the following values:
```yaml
separator: ";"
table_separator: "$"
inline_badge_start: "<"
inline_badge_end: ">"
```

here is a <;inline;badge;> in the middle of a line

Here is a line that contains the same badge twice

badge 1 (<L;same badge;https://example.com;>), badge 2 (<L;same badge;https://example.com;>)

This is a list of badges:

- <;badge;one;>
- <;badge;two;>
- <;badge;three;>

Table|with|inline badges
---|---|---
cell 1 |cell 2 <$with inline$badge$> in it | cell3
cell 1 |cell 2 <\|with non working\|inline badge\|> in it | cell3
cell 1 | <$two$badges$> <$one$cell$> | $normal$badge$
$normal badge$with \| pipe$ | test <$inline$badges \| with \| pipes$> too | cell 3
$normal badge$with \$ dollar$ | test <$inline$badges\$ with \$ dollar$> too | cell 3

