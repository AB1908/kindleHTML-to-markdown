#!/usr/bin/env python3
#
# This script gets a HTML annotations file exported from the Kindle app
# and convert it to markdown.

# TODO: DRY it up to use across other ereaders?? This would essentially create a self-hosted readwise
# TODO: Create a chapters class for chapters > highlight hierarchy?
# TODO: Edge cases
#       - notes/highlights before a chapter def??
#       - notes/highlights on chapter heading
#       - 
#       - 
# TODO: testing setup


from pathlib import Path
from os.path import basename, splitext
from sys import argv, exit
from bs4 import BeautifulSoup
import kindle


class HighlightsExtract:

    def file_handler():
        pass

    # try:
    #     file_content = source.read_text(encoding='UTF-8')
    # except OSError as e:
    #     print(f'Failed to read file: {e}.')
    #     exit(1)

    # soup = BeautifulSoup(file_content, 'html.parser')

    def chapter_from_div(self, note_divs):
        return note_divs[0].text.partition('-')[2].partition('>')[0].strip()

    def parse_HTML(self, soup):
        # TODO: refactor
        try:
            note_divs = soup.findAll("div", {'class': ["noteHeading","noteText"]})
            book_title = soup.select_one('.bookTitle').contents[0].strip()
            current_chapter = None

            kindle_notes = kindle.KindleHighlights()

            # chapter_marker = chapter_init(kindle_notes, note_divs[0].text.partition('-')[2].partition('>'))

            chapters = []
            for i in range(len(note_divs)):
                elem = note_divs[i]
                extracted_chapter_name = self.chapter_from_div(note_divs)
                KindleHighlights = kindle.KindleHighlights()

                # if current_chapter is None:
                #     chapter = kindle.Chapter(extracted_chapter_name)
                #     current_chapter = chapter
                if current_chapter is None or current_chapter.name != extracted_chapter_name:
                    # TODO: parse note/highlight?
                    chapter = kindle.Chapter(extracted_chapter_name)
                    chapters.append(current_chapter)
                    current_chapter = chapter

                if 'noteHeading' in elem.attrs['class']:
                    note_headers = elem.text.partition('-')
                    # [Highlight (<span class="highlight_pink">pink</span>), -, PREFACE TO THE CHARLES DICKENS EDITION >  Location 103]
                    location_metadata = note_headers[2].partition('>')
                    # [chapter_heading, >, location]
                    # TODO: chapter info?
                    note_location = location_metadata[2].strip()
                    div_type = note_headers[0].strip().split(" ")[0].strip()

                    # Highlight (pink)
                    # TODO: send all metadata to factory method or parse here and create there? IMO better to parse here since we explicitly want to decouple
                    # the parsing from the object creation
                    # if elem.text.strip().startswith("Highlight"):
                    if div_type == "Highlight":
                        # TODO: handle highlight
                        # highlight_metadata_array = note_headers
                        # TODO: div validation here?
                        parsed_highlight = KindleHighlights.create_text_highlight(elem, note_divs[i+1])

                    else: # div type is a note then. need additional logic to categorise note location.
                        # offload logic to separate class?
                        # TODO: handle note cases
                        parsed_highlight = KindleHighlights.create_new_note(elem, note_divs[i+1])
                    current_chapter.kindle_highlights.append(parsed_highlight)
            chapters.append(current_chapter)
            return chapters[1:]
            # TODO: split object parsing into own function

        except AttributeError as e:
            print(f'Error parsing file: {e}')
            exit(1)

    def output():
        output = f'# {book_title}\n\n'
        pandoc_div = ":::"
        for chapter_marker in kindle_notes:
            output += f'## {chapter_marker}\n\n'
            for kindle_highlight in kindle_notes[chapter_marker]:
                entry = pandoc_div
                if kindle_highlight["type"] == "note":
                    entry += 'standalone\n\n'
                    entry += f'Note: {kindle_highlight["text"]}\n\n'
                if kindle_highlight["type"] == "highlight":
                    entry += f'{kindle_highlight["color"].lower()}\n\n'
                    entry += f'{kindle_highlight["location"]}\n\n'
                    entry += f'> {kindle_highlight["text"]}\n\n'
                    for note_text in kindle_highlight["notes"]:
                        entry += f'{note_text}\n\n'
                entry += pandoc_div + "\n"
                output += entry + "\n"

        try:
            output = output.rstrip('\n')
            dest.write_text(output, encoding='UTF-8')
        except OSError as e:
            print(f'Failed to write file: {e}')
            exit(1)
        print(f'Written to: {dest_name}')


if __name__ == __main__:
    script_name = basename(__file__)
    if len(argv) != 2:
        print(f'Usage: {script_name} html_file')
        exit(1)

    source_name = argv[1]
    dest_name = splitext(source_name)[0] + '.md'

    source = Path(source_name)
    dest = Path(dest_name)

    if dest.exists():
        print(f'Destination file "{dest}" already exists.')
        answer = input('Overwrite? [y/n] ')
        if answer.lower().strip() != 'y':
            exit(1)