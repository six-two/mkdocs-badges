# Test (please ignore me)

This is my experimental new format (target for 0.3 release):
(type)?|title|value|(property|)*

## Badge types without properties

|normal 1|test|
L|link 1|https://example.com|
C|copy 1|Text to copy|
I|pypi|mkdocs|

## Properties

|with properties 1|test|c:text to copy|l:https://example.com|.html-class|class:html-class2|

## special cases

|emoji badge, should work|👍|

|image too big|<img src="/assets/img/test.png">|

|image small|<img src="/assets/img/test.png" width=50 height=15>|


|text contains a \| pipe symbol|value|

|missing value, should not be rendered|

I|missing value|should not be rendered

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

||Badge with empty title, should fail|

|Badge with empty value, should fail||

### Reflink badges

R|reflink badge|example_ref|

|normal badge with reflink|should work|r:example_ref|

[example_ref]: https://www.example.com


### Tag badges

T|tag|value|
T|special!%#|chars__in.value*()|

## Tags list

<!-- For some reason the tags defined on this page do not appear on this page. @TODO investigate -->

[TAGS]
