# Migration

## 0.2.x -> 0.3.0

Badge type | 0.2.x syntax | 0.3.0 syntax
---|---|---
Normal badge | `|"title":value|` | `|title|value|`
Install badge | `|@pypi:example|` | `I|pypi|example|`
Link badge | `|&link:www.example.com|` | `L|link|www.example.com|`
Reference link badge | Not supported | `R|link|example_ref|`
Copy badge | Only via custom badge | `C|title|text to show and copy|`
Custom badge | `|t:title|c:text to copy|v:text to show|l:https://example.com|end` | `|title|text to show|c:text to copy|l:https://example.com|`
