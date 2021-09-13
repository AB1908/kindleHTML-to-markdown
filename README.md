# Kindle HTML To Markdown

The Kindle Mobile app lets you export notes from your Kindle Notebook as an HTML file. However, this doesn't seem to be properly exported without having to pass your data through yet another third-party service like Readwise or Clippings.io. Most scripts I came across didn't quite export data properly nor did they attempt to parse the notes into a usable format, instead opting to make a near 1-to-1 conversion. Because of the strange export format, passing it through pandoc doesn't seem to be of any use either. Hence, the custom script.

## Dependencies

- Python
  - [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/)

## Usage

Run using

```
python -m kindle2md path/to/export.html
```

## Example

In:

```html
<div class="noteHeading">
Highlight (<span class="highlight_pink">pink</span>) - PREFACE TO THE CHARLES DICKENS EDITION >  Location 103
</div>
<div class="noteText">
So true are these avowals at the present day, that I can now only take the reader into one confidence more. Of all my books, I like this the best. It will be easily believed that I am a fond parent to every child of my fancy, and that no one can ever love that family as dearly as I love them. But, like many fond parents, I have in my heart of hearts a favourite child. And his name is DAVID COPPERFIELD.
</div>
<div class="noteHeading">
Note - PREFACE TO THE CHARLES DICKENS EDITION >  Location 103
</div>
<div class="noteText">
This is a sample note and highlight from the 1869 Charles Dickens Edition of David Copperfield that is freely available on Gutenberg.
</div
```

Out:

```markdown
## PREFACE TO THE CHARLES DICKENS EDITION

:::pink

> So true are these avowals at the present day, that I can now only take the reader into one confidence more. Of all my books, I like this the best. It will be easily believed that I am a fond parent to every child of my fancy, and that no one can ever love that family as dearly as I love them. But, like many fond parents, I have in my heart of hearts a favourite child. And his name is DAVID COPPERFIELD.

This is a sample note and highlight from the 1869 Charles Dickens Edition of David Copperfield that is freely available on Gutenberg.

:::
```
