from src import kindle2md

def test_parse_HTML_to_highlight_with_note(test_soup, example_chapter):
    actual_chapter = kindle2md.HighlightsExtract().parse_HTML(test_soup)[0]
    example_chapter = example_chapter()
    for i in range(len(actual_chapter.kindle_highlights)):
        assert vars(example_chapter.kindle_highlights[i]) == vars(actual_chapter.kindle_highlights[i])

def test_parse_chapters(example_parsed_chapter, example_chapter):
    actual_parsed_chapter = kindle2md.HighlightsExtract().parse_chapters([example_chapter()])
    assert actual_parsed_chapter == [example_parsed_chapter()]