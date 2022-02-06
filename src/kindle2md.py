#!/usr/bin/env python3
#
# This script gets a HTML annotations file exported from the Kindle app
# and convert it to markdown.

# TODO: DRY it up to use across other ereaders?? This would essentially create a self-hosted readwise
# TODO: Create a chapters class for chapters > highlight hierarchy?
# DONE: testing setup

from pathlib import Path
from os.path import basename, splitext
from sys import argv, exit
from src import kindle
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
env = Environment(loader=FileSystemLoader('templates'),trim_blocks=True,lstrip_blocks=True)
template = env.get_template('default.jinja')

class HighlightsExtract:

    def file_handler():
        # TODO
        # try:
        #     file_content = source.read_text(encoding='UTF-8')
        # except OSError as e:
        #     print(f'Failed to read file: {e}.')
        #     exit(1)

        # soup = BeautifulSoup(file_content, 'html.parser')
        pass


    def chapter_from_div(self, note_type):
        return note_type.text.partition('-')[2].partition('>')[0].strip()

    def parse_HTML(self, soup):
        # TODO: refactor
        try:
            note_divs = soup.findAll("div", {'class': ["noteHeading","noteText"]})
            book_title = soup.select_one('.bookTitle').contents[0].strip()
            book = kindle.Book(book_title)
            current_chapter = None
            chapters = []
            for i in range(0,len(note_divs)-1,2):
                note_type = note_divs[i]
                note_text = note_divs[i+1]
                extracted_chapter_name = self.chapter_from_div(note_type)
                KindleAnnotations = kindle.KindleAnnotations()
                if current_chapter is None or current_chapter.name != extracted_chapter_name:
                    # DONE: parse note/highlight?
                    chapter = kindle.Chapter(extracted_chapter_name)
                    chapters.append(current_chapter)
                    current_chapter = chapter

                if 'noteHeading' in note_type.attrs['class']:
                    note_headers = note_type.text.partition('-')
                    # TODO: chapter info?
                    note_type_text = note_headers[0].strip().split(" ")[0].strip()
                    if note_type_text == "Highlight":
                        parsed_highlight = KindleAnnotations.create_text_highlight(note_type, note_text)
                    else:
                        parsed_highlight = KindleAnnotations.create_new_note(note_type, note_text)
                    current_chapter.annotations.append(parsed_highlight)
            chapters.append(current_chapter)
            book.chapters = chapters[1:] # TODO: first chapter is none for some reason
            return book

        except AttributeError as e:
            print(f'Error parsing file: {e}')
            exit(1)

    def parse_chapters(self, book):
        def extract_location(kindle_highlight):
            return int(kindle_highlight.location.split(" ")[1])

        for chapter in book.chapters:
            # TODO: location aware parsing?
            cursor = None
            parsed_kindle_highlights = []
            for i, kindle_highlight in enumerate(chapter.annotations):
                # TODO: expose controllable location difference?
                # TODO: calculate location difference using highlight text length? a good approximation would be nice in place of an arbitrary value
                # DONE: Better class checking
                if i == 0:
                    cursor = kindle_highlight
                    continue
                if isinstance(kindle_highlight,kindle.Note) and isinstance(cursor, kindle.Highlight) and extract_location(kindle_highlight) - extract_location(cursor) < 4: # cond 2
                    cursor.notes.append(kindle_highlight)
                    continue
                parsed_kindle_highlights.append(cursor)
                cursor = kindle_highlight
            # last object left if not condition 2
            parsed_kindle_highlights.append(cursor)
            chapter.annotations = parsed_kindle_highlights
        return book

    # def output():
    #TODO: output to file

if __name__ == '__main__':
    script_name = basename(__file__)
    if len(argv) != 2:
        print(f'Usage: {script_name} html_file')
        exit(1)

    source_name = argv[1]
    dest_name = splitext(source_name)[0] + '.md'
    dest_name = splitext(source_name)[0] + '.md'

    source = Path(source_name)
    dest = Path(dest_name)

    if dest.exists():
        print(f'Destination file "{dest}" already exists.')
        answer = input('Overwrite? [y/n] ')
        if answer.lower().strip() != 'y':
            exit(1)
    file_content = source.read_text(encoding="UTF-8")
    soup = BeautifulSoup(file_content, 'html.parser')
    kindle_book = HighlightsExtract().parse_HTML(soup)
    kindle_book = HighlightsExtract().parse_chapters(kindle_book)
    try:
        rendered_output = template.render(book=kindle_book)
        dest.write_text(rendered_output, encoding='UTF-8')
    except OSError as e:
        print(f'Failed to write file: {e}')
        exit(1)
    print(f'Written to: {dest_name}')