# Custom badge styles

You can create custom styles for badges by following these steps.

## Decide which class(es) to style

- If you want to only style certain badges, assign them an extra class (say `custom-class`):
    ```
    |Badge with|custom class|.custom-class|
    ```

- If you want to restyle all badges, use only `badge`
- If you only want to restyle specific badge types (say only install badges), check the following table:

    Badge type | Type Letter | Class
    ---|---|---
    Normal / Custom | | badge-normal
    Link | L | badge-link
    Reflink | R | badge-reflink
    Install | I | badge-install
    Copy | C | badge-copy
    Tag | T | badge-tag
    Single element | S | badge-single


## Write your custom CSS

You can either extend the default style (generally recommended) or if that is not powerful enough, you can replace the whole default style.

### Extend the default style

Create a file where you store your custom CSS and tell MkDocs to use it.

For example create `docs/assets/stylesheets/custom.css`.
Then add the following lines to your `mkdocs.yml`:

```yaml
extra_css:
- assets/stylesheets/custom.css
```

Make sure to be as specific as possible (by using `.badge.<targetclass>`) so that your styles will have a higher priority than default style.
The elements you want to style are:

- The `.title`: left side of the badge (or the whole badge, if it is a single element badge)
- The `.value`: right side of the badge

Example CSS:
```css
.badge.custom-class .title {
    background-color: black;
}

.badge.custom-class .value {
    background-color: green;
}
```

### Replace the default style

!!! warning
    If you do this, it is your job to properly format the badges.
    I am no longer responsible, if it looks bad or causes (display) bugs.


Create a file where you store your custom CSS.
For example create `docs/assets/stylesheets/custom.css`.

Then tell this plugin, to use this file instead of the default CSS file:

```yaml
plugins:
- badges:
    badge_css: assets/stylesheets/custom.css
```

Afterwards write your custom CSS to the file.
You can of course let yourself be inspired by the default style (look at [`src/mkdocs_badges/assets/badge.css`](https://github.com/six-two/mkdocs-badges/blob/main/src/mkdocs_badges/assets/badge.css) in this repo).
