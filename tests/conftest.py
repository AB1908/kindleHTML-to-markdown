from pathlib import Path
from bs4 import BeautifulSoup
from pprint import pprint
import pytest
from src import kindle

hi = 0
ni = 2
test_data = {
    "HN": {"highlight": 0, "note": 2},
    "NH": {"highlight": 2, "note": 0},
    "HNH": {"highlight": [0,4], "note": [0]},
    }
    # H: for this case, we need a way to mark the downstream tests that should fail
    # HNHHNNNNNN
    # NNH
    # HHH
    # NNN
    # NHN
    # TODO: Refactor into actual tests
# TODO: Edge cases
#       - notes/highlights before a chapter def??
#       - notes/highlights on chapter heading
#       - 
#       - 

@pytest.fixture()
def highlight_index():
    return hi

@pytest.fixture()
def note_index():
    return ni

@pytest.fixture()
def test_soup():
    source = Path("./{}.html".format("HN"))
    file_content = source.read_text(encoding="UTF-8")
    soup = BeautifulSoup(file_content, 'html.parser')
    return soup

@pytest.fixture()
def test_note_divs(test_soup):
    return test_soup.findAll("div", {'class': ["noteHeading","noteText"]})

@pytest.fixture()
def example_highlight(test_note_divs, highlight_index):
    def _example_highlight():
        note_headers = test_note_divs[highlight_index].text.partition('-')
        location_metadata = note_headers[2].partition('>')
        test_highlight = kindle.Highlight(location_metadata[0].strip(), location_metadata[2].strip(), kindle.HighlightColor.get_color(test_note_divs[highlight_index].span.text.strip()) , test_note_divs[highlight_index+1].text.strip())
        return test_highlight
    return _example_highlight
    
@pytest.fixture()
def example_note(test_note_divs, note_index):
    def _example_note():
        note_headers = test_note_divs[note_index].text.partition('-')
        location_metadata = note_headers[2].partition('>')
        return kindle.Note(location_metadata[0].strip(), location_metadata[2].strip(), test_note_divs[note_index+1].text.strip())
    return _example_note

@pytest.fixture()
def example_chapter(example_highlight, example_note, test_note_divs):
    def _example_chapter():
        note_headers = test_note_divs[2].text.partition('-')
        test_chapter_name = note_headers[2].strip().partition('>')[0].strip()
        test_chapter = kindle.Chapter(test_chapter_name)
        test_chapter.annotations.append(example_highlight())
        test_chapter.annotations.append(example_note())
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
        test_parsed_chapter.annotations.append(test_highlight)
        return test_parsed_chapter
    return _example_parsed_chapter

@pytest.fixture()
def example_parsed_highlights(example_highlight, example_note):
    def _example_parsed_highlights():
        test_parsed_highlight = example_highlight()
        test_parsed_highlight.notes.append(example_note())
        return test_parsed_highlight
    return _example_parsed_highlights

@pytest.fixture()
def example_book(example_parsed_chapter):
    def _example_book():
        test_book = kindle.Book("David Copperfield")
        test_book.chapters.append(example_parsed_chapter())
        return test_book
    return _example_book