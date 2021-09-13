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
