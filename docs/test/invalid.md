# Tests: Invalid badges

!!! note
    The badges on this page are malformed and should not be rendered.
    Some should also produce a warning during the build process.

|missing value, should not be rendered|

I|missing value|should not be rendered

## Tables

|Markdown|Table|
|---|---|
|table rows|should not be parsed|
table row without outer pipes|should not be parsed

Problematic table from [#4](https://github.com/six-two/mkdocs-badges/issues/4):

| 🔗 | information (count) | grouping |
| - | ------------------- | :------: |
| [🔗](#foo) | server |

Same table with three dashes:

| 🔗 | information (count) | grouping |
| --- | ------------------- | :------: |
| [🔗](#foo) | server |


## Code blocks

And code blocks should also not be parsed:

```
|fenced code|should not be parsed|
```

    |indented code|should not be parsed|

## Other invalid stuff

X|invalid type|should not be parsed|
xyz|invalid type|should not be parsed|

|trailing stuff|should not be parsed|trailing

|repeated attribute|should not be parsed|c:text to copy|c:https://example.com||c:html-class2|

||Badge with empty title, should fail|

|Badge with empty value, should fail||

Should cause an error:
S|||

S|Should cause|an error|

S|Should cause an error||c:error|l:error|

S|Should cause an error||c:error|r:example_ref|
