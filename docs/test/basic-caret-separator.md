# Tests: Basic with different separator

This page uses the caret (`^`) separator and is used to test custom separators.

<style>
    /* For for debugging the layout  */
    .badge-group {
        border: 1px solid red;
    }
</style>


## Badge types without properties

^normal 1^test^
L^link 1^https://example.com^
C^copy 1^Text to copy^
I^pypi^mkdocs^

## Properties

^with properties 1^test^c:text to copy^l:https://example.com^.html-class^class:html-class2^

## Layout (overflow) tests

Singel tag:
^This text is very long. This text is even longer.^This value is the longest test value on this page at this time^

Long list of tags:
^aaaaa^bbbbb^
^ccccc^ddddd^
^eeeee^fffff^
^ggggg^hhhhh^
^iiiii^jjjjj^
^kkkkk^lllll^
^mmmmm^nnnnn^
^ooooo^ppppp^
^qqqqq^rrrrr^
^sssss^ttttt^
^uuuuu^vvvvv^
^wwwww^xxxxx^
^yyyyy^zzzzz^
^aaaaa^bbbbb^
^ccccc^ddddd^
^eeeee^fffff^
^g^hhhhhh^
^iiiii^jjjjj^

Overlong element in long list:
^aaaaa^bbbbb^
^This text is very long. This text is even longer.^This value is the longest test value on this page at this time^
^ccccc^ddddd^
^eeeee^fffff^
^ggggg^hhhhh^


## special cases

^emoji badge, should work^👍^
^image too big^<img src="/assets/img/test.png">^
^image small^<img src="/assets/img/test.png" width=50 height=15>^
^<img src="/assets/img/test.png" width=50 height=15>^<img src="/assets/img/test.png" width=50 height=15>^
^<svg width="35" height="35"><circle cx="10" cy="10" r="9" stroke="green" stroke-width="2" fill="yellow" /></svg>^SVG as key (see issue #2)^
^circle^<svg width="15" height="15"><circle cx="7" cy="7" r="7" stroke="green" stroke-width="2" fill="yellow" /></svg>^
^Very large image^<svg width="100" height="100"><circle cx="50" cy="50" r="48" stroke="red" stroke-width="2" fill="orange" /></svg>^




^text contains a backslash and a \^ pipe symbol^value^
^text contains two backslashes and a \\^ pipe symbol^
^text contains three backslashes and a \\\^ pipe symbol^value^
^text contains four backslashes and a \\\\^ pipe symbol^
^text contains \*escaped\* \`code\` \[link\](http://example.com) markup \^ pipe symbol^

### Tables

Since this format matches the markdown tables format, I need to make sure that no header comes before any of my values

^Markdown^Table^
^---^---^
^table rows^should not be parsed^
table row without outer pipes^should not be parsed

^not part of the table^should be parsed^

But badges in tables should be allowed

But badges in tables should be allowed

|Markdown|Table||
|---|---|---|
|table cells| L+Should be parsed+https://example.com+ |test|
|+test 1+should be parsed+| +test 2+should be parsed+ |+test 3+should be parsed+|
|+should+be \| parsed+ | +\\Test\+a+\|123+ | L+Should not be parsed+https://example.com+a ||

+outside of a table+this should not be parsed+


### Reflink badges

R^reflink badge^example_ref^

^normal badge with reflink^should work^r:example_ref^

[example_ref]: https://www.example.com


### Tag badges

T^tag^value^
T^special!%#^chars__in.value*()^


### Single element badges

S^Reference link^^reflink:example_ref^

S^^This is a <img src="/assets/img/test.png" width=50 height=15>^


