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
They are similar to link badges, but display the reference name as value.

**Warning**: Reference links rely on the underlying markdown parser.
Thus, there badges may not work correctly when inside HTML (like a `<div>` element).
To work araound this, make sure markdown parsing inside HTML is enabled, or only put he badges in `<span>` elements, which do (to my knowledge) not prevent the parsing of Markdown contents.

Example markdown:

```markdown
R|reflink badge|example_ref|
|normal badge with reflink|should work|r:example_ref|

[example_ref]: https://www.example.com
```

Result:

<span class=result>
R|reflink badge|example_ref|
|normal badge with reflink|should work|r:example_ref|
</span>



## Copy badges

Copy badges copy their value to the users clipboard when clicked upon

Example markdown:

```markdown
C|Password|monkey123|
C|Linux check ethernet settings|ip a s eth0|
```

Result:

<span class=result>
C|Password|monkey123|
C|Linux check ethernet settings|ip a s eth0|
</span>


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

<span class=result>
I|github|six-two/mkdocs-badges|
I|pypi|mkdocs|
</span>


## Custom badges

Custom badges offer all features supported by the other badge types.
They have however a more verbose syntax.
On the upside you are in total control about the supplied values, since none of them are automaticaly generated.

Short prefix | Long prefix | Conflicts with | Description
--- | --- | --- | ---
`.` | `class:` | - | Add a class to the badge, which can be used for custom styling. Can be specified multiple time to add multiple classes. Can also be used with any other badge type
`c:` | `copy:` | reflink | Copy the given text when the badge is clicked
`l:` | `link:` | reflink | Clicking on the badge will direct the user to the given URL
`r:` | `reflink:` | copy, link | Similar to link, but instead it uses the reference link syntax

Example markdown:

```markdown
|Link badge equivalent|example.com|link:https://www.example.com|
|Copy badge equivalent|text to show|copy:text to copy|
|Install badge equivalent|mkdocs-badge|link:https://github.com/six-two/mkdocs-badges|copy:git clone https://github.com/six-two/mkdocs-badges.git|
|Reflink badge equivalent|example.com|r:example_ref|
```

Result:

<span class=result>
|Link badge equivalent|example.com|link:https://www.example.com|
|Copy badge equivalent|text to show|copy:text to copy|
|Install badge equivalent|mkdocs-badge|link:https://github.com/six-two/mkdocs-badges|copy:git clone https://github.com/six-two/mkdocs-badges.git|
|Reflink badge equivalent|example.com|r:example_ref|
</span>

<!-- Link references -->
[example_ref]: https://www.example.com

