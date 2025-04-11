# Tests: GitHub Issues

## Issue 7

```
|Simplified hostname demo|[Simplified hostname demo](https://www.example.com)|

|Simplified hostname demo 2|Simplified hostname demo|l:https://example.com|
```

<!-- L|Simplified hostname demo|[Simplified hostname demo](https://www.example.com)| -->
|Simplified hostname demo|[Simplified hostname demo](https://www.example.com)|

|Simplified hostname demo 2|Simplified hostname demo|l:https://example.com|

---

```
R|reflink badge|example_ref|
|normal badge with reflink|should work|r:example_ref|

[this should be converted to a link][example_ref]

[example_ref]: https://www.example.com
```

R|reflink badge|example_ref|
|normal badge with reflink|should work|r:example_ref|

[this should be converted to a link][example_ref]

[example_ref]: https://www.example.com

---

```markdown
|[Link A](https://duckduckgo.com/)|[Simplified hostname demo](https://www.example.com)|
```

|[Link A](https://duckduckgo.com/)|[Simplified hostname demo](https://www.example.com)|

---

### Badges With Optional Angle Brackets

```
|Custom Badge With Angle Brackets|Simplified hostname demo|l:<https://github.com/six-two/mkdocs-badges>|
L|Link Badge With Angle Brackets|<https://github.com/six-two/mkdocs-badges>|
|Normal Badge With Angle Brackets|<https://github.com/six-two/mkdocs-badges>|
```

|Custom Badge With Angle Brackets|Simplified hostname demo|l:<https://github.com/six-two/mkdocs-badges>|
L|Link Badge With Angle Brackets|<https://github.com/six-two/mkdocs-badges>|
|Normal Badge With Angle Brackets|<https://github.com/six-two/mkdocs-badges>|
