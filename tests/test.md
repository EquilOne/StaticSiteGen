# Heading level 1

This is a plain paragraph with no special formatting at all.

## Heading level 2

This paragraph mixes all inline styles: **bold text**, _italic text_, `inline code`, a [link to Boot.dev](https://www.boot.dev), and an image ![Test image](https://example.com/image.png).

### Heading level 3

Another paragraph with **bold containing `code` inside** and _italic containing **bold** inside_.

#### Heading level 4

##### Heading level 5

###### Heading level 6

This paragraph tests inline syntax edge cases: empty **bold**, a bare underscore character_like_this_that_should_not_be_italic, code with **fake bold** inside `backticks`, and a link [Boot.dev](https://www.boot.dev) followed by text.

An unordered list follows:

- First item
- Second item with **bold**
- Third item with `code`
- Fourth item
- Fifth item with [a link](https://www.boot.dev)

An ordered list follows:

1. First ordered item
2. Second ordered item with _italic_
3. Third ordered item

A blockquote follows:

> This is a blockquote.
> It spans multiple lines
> like a philosophical thought.

A code block follows:

```
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

A code block that looks like markdown follows:

```
# This is not a heading
## Neither is this
- not a list either
```

A short paragraph to finish the document. Everything above should be converted by the generator without errors.
