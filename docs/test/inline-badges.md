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

