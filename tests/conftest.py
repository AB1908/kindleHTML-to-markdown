from pathlib import Path
from bs4 import BeautifulSoup
from pprint import pprint
import pytest
from src import kindle

@pytest.fixture()
def test_soup():
    filename = "sample.html"
    source = Path("./{}".format(filename))
    file_content = source.read_text(encoding="UTF-8")
    soup = BeautifulSoup(file_content, 'html.parser')
    return soup

@pytest.fixture()
def test_note_divs(test_soup):
    return test_soup.findAll("div", {'class': ["noteHeading","noteText"]})

@pytest.fixture()
def example_highlight(test_note_divs):
    def _example_highlight():
        note_headers = test_note_divs[0].text.partition('-')
        location_metadata = note_headers[2].partition('>')
        test_highlight = kindle.Highlight(location_metadata[0].strip(), location_metadata[2].strip(), kindle.HighlightColor.get_color(test_note_divs[0].span.text.strip()) , test_note_divs[1].text.strip())
        return test_highlight
    return _example_highlight
    
@pytest.fixture()
def example_note(test_note_divs):
    def _example_note():
        note_headers = test_note_divs[2].text.partition('-')
        location_metadata = note_headers[2].partition('>')
        return kindle.Note(location_metadata[0].strip(), location_metadata[2].strip(), test_note_divs[3].text.strip())
    return _example_note

@pytest.fixture()
def example_chapter(example_highlight, example_note, test_note_divs):
    def _example_chapter():
        note_headers = test_note_divs[2].text.partition('-')
        test_chapter_name = note_headers[2].strip().partition('>')[0].strip()
        test_chapter = kindle.Chapter(test_chapter_name)
        test_chapter.kindle_highlights.append(example_highlight())
        test_chapter.kindle_highlights.append(example_note())
        return test_chapter
    return _example_chapter

@pytest.fixture()
def example_parsed_chapter(example_highlight, example_note, test_note_divs):
    def _example_parsed_chapter():
        note_headers = test_note_divs[2].text.partition('-')
        test_chapter_name = note_headers[2].strip().partition('>')[0].strip()
        test_parsed_chapter = kindle.Chapter(test_chapter_name)
        test_highlight = example_highlight()
        test_highlight.notes.append(example_note())
        test_parsed_chapter.kindle_highlights.append(test_highlight)
        return test_parsed_chapter
    return _example_parsed_chapter

@pytest.fixture()
def example_parsed_highlights(example_highlight, example_note):
    example_highlight = example_highlight()
    example_highlight.notes.append(example_note())
    yield example_highlight