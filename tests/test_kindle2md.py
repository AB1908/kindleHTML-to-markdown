from src import kindle2md
from pathlib import Path
from bs4 import BeautifulSoup
import pytest
from src import kindle
from copy import deepcopy
import pytest

def test_parse_HTML_to_highlight_with_note(test_soup, example_chapter):
    actual_chapter = kindle2md.HighlightsExtract().parse_HTML(test_soup).chapters[0]
    example_chapter = example_chapter()
    for i in range(len(actual_chapter.kindle_highlights)):
        assert vars(example_chapter.kindle_highlights[i]) == vars(actual_chapter.kindle_highlights[i])

# def test_parse_chapters(example_parsed_chapter, example_chapter):
#     # TODO: Rewrite
#     actual_parsed_chapter = kindle2md.HighlightsExtract().parse_chapters([example_chapter()])
#     assert actual_parsed_chapter == [example_parsed_chapter()]

test_data = {
        "HN" : {"highlight": [0], "note": [2]},
        "NH" : {"highlight": [2], "note": [0]},
        "HNH": {"highlight": [0,4], "note": [0]},
        "NNH": {"highlight": [4], "note": [0,2]},
        "HHH": {"highlight": [0,2,4], "note": []},
        "HHN": {"highlight": [0,2], "note": [4]},
        "HNN": {"highlight": [0], "note": [2,4]},
    }

@pytest.mark.parametrize("test_filename", test_data.keys())
def test_parsing_logic(test_note_divs, test_filename):
     # TODO: Chapterwise test cases
     # TODO: REFACTOR!!!!

    source = Path("./{}.html".format(test_filename))
    file_content = source.read_text(encoding="UTF-8")
    test_soup = BeautifulSoup(file_content, 'html.parser')
    # return soup

    test_note_divs = test_soup.findAll("div", {'class': ["noteHeading","noteText"]})
    # kh_ordering = [k.split("") for k in test_data.keys()]
    kh_ordering = test_filename

    def extract_highlight(note_divs, highlight_index):
        note_headers = note_divs[highlight_index].text.partition('-')
        location_metadata = note_headers[2].partition('>')
        extracted_highlight = kindle.Highlight(location_metadata[0].strip(), location_metadata[2].strip(), kindle.HighlightColor.get_color(note_divs[highlight_index].span.text.strip()) , note_divs[highlight_index+1].text.strip())
        return extracted_highlight

    def extract_note(note_divs, note_index):
        note_headers = note_divs[note_index].text.partition('-')
        location_metadata = note_headers[2].partition('>')
        return kindle.Note(location_metadata[0].strip(), location_metadata[2].strip(), note_divs[note_index+1].text.strip())

    # highlight_indices = test_data[filename]["highlight"]
    extracted_kindle_highlights = []
    note_headers = test_note_divs[2].text.partition('-')
    test_chapter_name = note_headers[2].strip().partition('>')[0].strip()
    test_chapter = kindle.Chapter(test_chapter_name)
    # example_parsed_chapter = deepcopy(test_chapter)

    for i,k in enumerate(kh_ordering):
        if k == "H":
            extracted_kindle_highlights.append(extract_highlight(test_note_divs, i*2))
        elif k == "N":
            extracted_kindle_highlights.append(extract_note(test_note_divs, i*2))
    test_chapter.kindle_highlights += extracted_kindle_highlights
    # parsedHTML setup complete
    # test output setup begins

    example_parsed_chapter = deepcopy(test_chapter)
    if test_filename == "HN":
        example_parsed_chapter.kindle_highlights[0].notes.append(example_parsed_chapter.kindle_highlights[1])
        del example_parsed_chapter.kindle_highlights[1]
    elif test_filename == "HNH":
        example_parsed_chapter.kindle_highlights[0].notes.append(example_parsed_chapter.kindle_highlights[1])
        del example_parsed_chapter.kindle_highlights[1]
    elif test_filename == "HHN":
        example_parsed_chapter.kindle_highlights[1].notes.append(example_parsed_chapter.kindle_highlights[2])
        del example_parsed_chapter.kindle_highlights[2]
    elif test_filename == "HNN":
        example_parsed_chapter.kindle_highlights[0].notes.append(example_parsed_chapter.kindle_highlights[1])
        del example_parsed_chapter.kindle_highlights[1]

    test_book = kindle.Book("David Copperfield")
    test_book.chapters = [test_chapter]
    actual_parsed_book = kindle2md.HighlightsExtract().parse_chapters(test_book)
    assert actual_parsed_book.chapters == [example_parsed_chapter]