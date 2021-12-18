# coding=utf-8

import src.kindle as kindle

# TODO: Look into test rewrites to properly unit test

def test_example_chapter(example_chapter, example_highlight, example_note):
    test_chapter = kindle.Chapter(example_highlight().chapter)
    test_chapter.kindle_highlights.append(example_highlight())
    test_chapter.kindle_highlights.append(example_note())
    assert example_chapter() == test_chapter

def test_create_highlight_from_div(test_note_divs, example_highlight, highlight_index):
    actual_highlight = kindle.KindleHighlights().create_text_highlight(test_note_divs[highlight_index], test_note_divs[highlight_index+1])
    assert example_highlight() == actual_highlight

def test_create_new_note_from_div(test_note_divs, example_note, note_index):
    actual_note = kindle.KindleHighlights().create_new_note(test_note_divs[note_index], test_note_divs[note_index+1])
    assert example_note() == actual_note

def test_highlight_with_notes_equality(example_highlight, example_note):
    example_highlight_copy = example_highlight().notes.append(example_note())
    example_highlight = example_highlight().notes.append(example_note())
    assert example_highlight == example_highlight_copy

def test_highlight_equality(example_highlight):
    example_highlight_copy = example_highlight()
    assert example_highlight() == example_highlight_copy

def test_highlight_inequality(example_highlight):
    example_highlight_copy = example_highlight()
    example_highlight_copy.text = "New text here" 
    assert example_highlight() != example_highlight_copy

def test_note_inequality(example_note):
    example_note_copy = example_note()
    example_note_copy.text = "New text here" 
    assert example_note() != example_note_copy
