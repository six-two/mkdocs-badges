# Migration

## 0.2.x -> 0.3.0

### Syntax changes

Badge type | 0.2.x syntax | 0.3.0 syntax
---|---|---
Normal badge | `|"title":value|` | `|title|value|`
Install badge | `|@pypi:example|` | `I|pypi|example|`
Link badge | `|&link:www.example.com|` | `L|link|www.example.com|`
Reference link badge | Not supported | `R|link|example_ref|`
Copy badge | Only via custom badge | `C|title|text to show and copy|`
Custom badge | `|t:title|c:text to copy|v:text to show|l:https://example.com|end` | `|title|text to show|c:text to copy|l:https://example.com|`

### Useful commands

Some of the badges can be updated with th following sed commands.
Please commit / back up your files before attemting this, since the potential of corrupting your files may exist.

Use the following sed command, to update all markdown files at once.
The command must be repeated for each `<pattern>`:
```bash
find ./docs/ -iname "*.md" -exec sed -i <pattern> '{}' \;
```

- Normal badge pattern: `'s/^|"\(.\+\?\)":/|\1|/'`
- Install badge pattern: `'s/^|@\(aur\|gem\|github\|gitlab\|kali\|pacman\|pypi\):/I|\1|/'`
- Link badge pattern: `'s/^|&\([^:]\+\):\s*/L|\1|/'`

Special badges are harder to replace.
You can find them with the following command and then replace them manually:

```bash
find ./docs/ -iname "*.md" -exec grep -nH -e '|t:.\+|v:.\+|' '{}' \;
```
