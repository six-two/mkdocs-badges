# Badge types

There are multiple different badge types, which different syntaxes.
All badges need to be in their now line and have no indent / leading whitespaces.
Badges inside (fenced) code bocks are also not interpreted.

## Simple badges

Simple badges are just a badge that does not react to clicks.

Example markdown:

```
|Example badge|works|
```

Result:

<div class=result>
|Example badge|works|
</div>


## Link badges

Link badges link to a given URL.
They only have the (simplified version of) the hostname specified in the link as visible value

Example markdown:

```markdown
L|Bug Tracker|https://github.com/six-two/mkdocs-badges/issues|
L|Simplified hostname demo|https://www.example.com|
```

Result:

<div class=result>
L|Bug Tracker|https://github.com/six-two/mkdocs-badges/issues|
L|Simplified hostname demo|https://www.example.com|
</div>

## Reference link badges

Reference link badges link to a given URL using reference links.
They are similar to link badges, but display the reference name as value

Example markdown:

```markdown
R|reflink badge|example_ref|
|normal badge with reflink|should work|r:example_ref|

[example_ref]: https://www.example.com
```

Result:

<!-- Can not be inside HTML, since it contains markdown that needs to be parsed for the link to work -->
<!-- <div class=result> -->
R|reflink badge|example_ref|
|normal badge with reflink|should work|r:example_ref|
<!-- </div> -->



## Copy badges

Copy badges copy their value to the users clipboard when clicked upon

Example markdown:

```markdown
C|Password|monkey123|
C|Linux check ethernet settings|ip a s eth0|
```

Result:

<div class=result>
C|Password|monkey123|
C|Linux check ethernet settings|ip a s eth0|
</div>


## Install badges

Install badges are designed to make it easy for users to install software.
Sadly they are a bit unintuitive to use.
Clicking on the badge title (left side) will copy the command to install the software (`git clone ...`, `pip install ...`, `sudo apt install ...`, etc) to the user's clipboard.
To show them that this is possible, the cursor takes the form of a question mark.
To show them what has happened, a popup is shown once they clicked.

The right side is a link to the software on the given platorrm (github repo, PyPI page, linux package tracker, etc).


Example markdown:

Markdown code:
```
I|github|six-two/mkdocs-badges|
I|pypi|mkdocs|
```

Result:

<div class=result>
I|github|six-two/mkdocs-badges|
I|pypi|mkdocs|
</div>


## Custom badges

Custom badges offer all features supported by the other badge types.
They have however a more verbose syntax.
On the upside you are in total control about the supplied values, since none of them are automaticaly generated.

Example markdown:

```markdown
|Link badge equivalent|example.com|link:https://www.example.com|
|Copy badge equivalent|text to show|copy:text to copy|
|Install badge equivalent|mkdocs-badge|link:https://github.com/six-two/mkdocs-badges|copy:git clone https://github.com/six-two/mkdocs-badges.git|
|Reflink badge equivalent|example.com|r:example_ref|
```

Result:

<div class=result>
|Link badge equivalent|example.com|link:https://www.example.com|
|Copy badge equivalent|text to show|copy:text to copy|
|Install badge equivalent|mkdocs-badge|link:https://github.com/six-two/mkdocs-badges|copy:git clone https://github.com/six-two/mkdocs-badges.git|
</div>
|Reflink badge equivalent|example.com|r:example_ref|


<!-- Link references -->
[example_ref]: https://www.example.com

