# Badge types

There are multiple different badge types, which different syntaxes.
All badges need to be in their now line and have no indent / leading whitespaces.
Badges inside (fenced) code bocks are also not interpreted.

## Simple badges

Simple badges are just a badge that does not react to clicks.

### Example 1

Markdown code:
```
|"Example badge":works|
```

Result:

<div class=result>
|"Example badge":works|
</div>


## Install badges

Install badges are designed to make it easy for users to install software.
Sadly they are a bit unintuitive to use.
Clicking on the badge title (left side) will copy the command to install the software (`git clone ...`, `pip install ...`, `sudo apt install ...`, etc) to the user's clipboard.
To show them that this is possible, the cursor takes the form of a question mark.
To show them what has happened, a popup is shown once they clicked.

The right side is a link to the software on the given platorrm (github repo, PyPI page, linux package tracker, etc).


### Example 1

Markdown code:
```
|@github:six-two/mkdocs-badges|
|@pypi:mkdocs|
```

Result:

<div class=result>
|@github:six-two/mkdocs-badges|
|@pypi:mkdocs-badges|
</div>

## Advanced badges

Advanced badges offer all features supported by the other badge types.
They have however a more verbose syntax.
Compared to the install badges, the link and text to copy are not automatically generated.
Instead you can supply them.
If you do not supply them, an advanced badge will behave like a simple badge.

### Example 1

The following is the advanced badge equivalent of the `|"Example badge":works|` simple badge:

```markdown
|t:Example badge|v:works|
```

Result:

<div class=result>
|t:Example badge|v:works|
</div>

### Example 2

The following is the advanced badge equivalent of the `|@github:six-two/mkdocs-badges|` install badge.
As you can see it is a much longer and more verbose format with quite a bit of redundant information:


```markdown
|t:github|c:git clone https://github.com/six-two/mkdocs-badges.git|v:six-two/mkdocs-badges|l:https://github.com/six-two/mkdocs-badges.git|
```

Result:

<div class=result>
|t:github|c:git clone https://github.com/six-two/mkdocs-badges.git|v:six-two/mkdocs-badges|l:https://github.com/six-two/mkdocs-badges.git|
</div>

### Example 3

You can also create advanced badges that only copy thex when clicked or that only link to a webpage.
When only one action is defined, clicking anywhere on the badge will trigger it:

```markdown
|t:Copy text when clicked|c:Value to copy|v:Value to show|
|t:Badge with link to|v:wikipedia|l:https://www.wikipedia.org/|
```

Result:

<div class=result>
|t:Copy text when clicked|c:Value to copy|v:Value to show|
|t:Badge with link to|v:wikipedia|l:https://www.wikipedia.org/|
</div>

