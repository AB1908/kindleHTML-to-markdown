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
    for i in range(len(actual_chapter.annotations)):
        assert vars(example_chapter.annotations[i]) == vars(actual_chapter.annotations[i])

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

def generate_divs_from_file(testfile):
    source = Path("./{}.html".format(testfile))
    file_content = source.read_text(encoding="UTF-8")
    test_soup = BeautifulSoup(file_content, 'html.parser')
    return test_soup.findAll("div", {'class': ["noteHeading","noteText"]})

def extract_highlight(note_divs, highlight_index):
    note_headers = note_divs[highlight_index].text.partition('-')
    location_metadata = note_headers[2].partition('>')
    extracted_highlight = kindle.Highlight(location_metadata[0].strip(), location_metadata[2].strip(), kindle.HighlightColor.get_color(note_divs[highlight_index].span.text.strip()) , note_divs[highlight_index+1].text.strip())
    return extracted_highlight

def extract_note(note_divs, note_index):
    note_headers = note_divs[note_index].text.partition('-')
    location_metadata = note_headers[2].partition('>')
    return kindle.Note(location_metadata[0].strip(), location_metadata[2].strip(), note_divs[note_index+1].text.strip())

def extract_all_annotations(test_filename, test_note_divs):
    extracted_kindle_highlights = []
    for i,k in enumerate(test_filename):
        if k == "H":
            extracted_kindle_highlights.append(extract_highlight(test_note_divs, i*2))
        elif k == "N":
            extracted_kindle_highlights.append(extract_note(test_note_divs, i*2))
    return extracted_kindle_highlights

@pytest.mark.parametrize("test_filename", test_data.keys())
def test_parsing_logic(test_filename):
     # TODO: REFACTOR!!!!
    test_note_divs = generate_divs_from_file(test_filename)
    note_headers = test_note_divs[2].text.partition('-')
    test_chapter_name = note_headers[2].strip().partition('>')[0].strip()
    test_chapter = kindle.Chapter(test_chapter_name)
    extracted_kindle_highlights = extract_all_annotations(test_filename, test_note_divs)
    test_chapter.annotations += extracted_kindle_highlights
    # test output setup begins
    example_parsed_chapter = deepcopy(test_chapter)
    if test_filename in ("HN","HNH","HNN"):
        example_parsed_chapter.annotations[0].notes.append(example_parsed_chapter.annotations[1])
        del example_parsed_chapter.annotations[1]
    elif test_filename == "HHN":
        example_parsed_chapter.annotations[1].notes.append(example_parsed_chapter.annotations[2])
        del example_parsed_chapter.annotations[2]
    test_book = kindle.Book("David Copperfield")
    test_book.chapters = [test_chapter]
    actual_parsed_book = kindle2md.HighlightsExtract().parse_chapters(test_book)
    assert actual_parsed_book == test_book

def test_multiple_chapter_parsing(testfile = "1HNH2HNNH"):
    # TODO: Chapterwise test cases
    test_note_divs = generate_divs_from_file(testfile)
    test_book = kindle.Book("David Copperfield")
    test_book.chapters.append(kindle.Chapter("CHAPTER 5. I AM SENT AWAY FROM HOME"))
    test_book.chapters.append(kindle.Chapter("CHAPTER 6. I ENLARGE MY CIRCLE OF ACQUAINTANCE"))
    # create highlights
    extracted_kindle_highlights = extract_all_annotations("HNHHNNH", test_note_divs)
    # manually order chapter highlights
    test_book.chapters[0].annotations += extracted_kindle_highlights[:3]
    test_book.chapters[1].annotations += extracted_kindle_highlights[3:]
    test_book.chapters[0].annotations[0].notes.append(test_book.chapters[0].annotations[1])
    del test_book.chapters[0].annotations[1]
    test_book.chapters[1].annotations[0].notes.append(test_book.chapters[1].annotations[1])
    del test_book.chapters[1].annotations[1]
    actual_parsed_book = kindle2md.HighlightsExtract().parse_chapters(test_book)
    assert actual_parsed_book == test_book