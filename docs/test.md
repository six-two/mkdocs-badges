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

Images in both values:
|<img src="/assets/img/test.png" width=50 height=15>|<img src="/assets/img/test.png" width=50 height=15>|

SVG as key (see issue #2):
|<svg width="35" height="35"><circle cx="10" cy="10" r="9" stroke="green" stroke-width="2" fill="yellow" /></svg>|circle|

|circle|<svg width="15" height="15"><circle cx="7" cy="7" r="7" stroke="green" stroke-width="2" fill="yellow" /></svg>|



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


#### Tags list

<!-- For some reason the tags defined on this page do not appear on this page. @TODO investigate -->

[TAGS]


### Single element badges

S|Reference link||reflink:example_ref|

Should cause an error:
S|||

S|Should cause|an error|

S|Should cause an error||c:error|l:error|

S|Should cause an error||c:error|r:example_ref|

S||This is a <img src="/assets/img/test.png" width=50 height=15>|


