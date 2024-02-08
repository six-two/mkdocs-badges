# Test: Theme specific

<style>
/* SEE https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/ */
@keyframes heart {
  0%, 40%, 80%, 100% {
    transform: scale(1);
  }
  20%, 60% {
    transform: scale(1.15);
  }
}
.heart {
  animation: heart 1000ms infinite;
}

</style>

## Emojis

Baseline test:

- Smiley emoji: :smile:
- Beating heart: :octicons-heart-fill-24:{ .heart }

Badges:
| :smile: | MkDocs Material Icons |
| MkDocs Material Icons |:octicons-heart-fill-24:{ .heart }|


