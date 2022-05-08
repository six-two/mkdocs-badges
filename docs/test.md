# Test (please ignore me)

This is my experimental new format (target for 0.3 release):
(type)?|title|value|(property|)*

## Badge types without properties

|normal 1|test|
L|link 1|https://example.com|
C|copy 1|Text to copy|
I|pypi|mkdocs|

## Properties

c:|copy: | text to copy
l:|link: | link
.<name>|class:<name> | HTML class styling. Can be used multiple times

|with properties 1|test|c:text to copy|l:https://example.com|.html-class|class:html-class2|

## special cases

|text contains a \| pipe symbol|value
|missing value|
I|missing|value

Since this format matches the markdown tables format, I need to make sure that no header comes before ant of my values

|Markdown|Table|
|---|---|
|table rows|should not be parsed|
table row without outer pipes|should not be parsed

|not part of the table|should be parsed|

And code blocks should also not be parsed:

```
|fenced code|should not be parsed|
```

    |indented code|should not be parsed|

X|invalid type|should not be parsed|
xyz|invalid type|should not be parsed|

|trailing stuff|should not be parsed|trailing

|repeated attribute|should not be parsed|c:text to copy|c:https://example.com||c:html-class2|

