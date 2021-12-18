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


    def chapter_from_div(self, note_divs):
        return note_divs[0].text.partition('-')[2].partition('>')[0].strip()

    def parse_HTML(self, soup):
        # TODO: refactor
        try:
            note_divs = soup.findAll("div", {'class': ["noteHeading","noteText"]})
            # TODO: Book handling?
            book_title = soup.select_one('.bookTitle').contents[0].strip()
            current_chapter = None
            chapters = []
            for i in range(len(note_divs)-1):
                note_type = note_divs[i]
                note_text = note_divs[i+1]
                extracted_chapter_name = self.chapter_from_div(note_divs)
                KindleHighlights = kindle.KindleHighlights()
                if current_chapter is None or current_chapter.name != extracted_chapter_name:
                    # DONE: parse note/highlight?
                    chapter = kindle.Chapter(extracted_chapter_name)
                    chapters.append(current_chapter)
                    current_chapter = chapter

                if 'noteHeading' in note_type.attrs['class']:
                    note_headers = note_type.text.partition('-')
                    # TODO: chapter info?
                    note_type_text = note_headers[0].strip().split(" ")[0].strip()

                    # Highlight (pink)
                    # DONE: send all metadata to factory method or parse here and create there? IMO better to parse here since we explicitly want to decouple
                    # the parsing from the object creation
                    # if elem.text.strip().startswith("Highlight"):
                    if note_type_text == "Highlight":
                        # DONE: handle highlight
                        # highlight_metadata_array = note_headers
                        # DONE: div validation here?
                        parsed_highlight = KindleHighlights.create_text_highlight(note_type, note_text)

                    else:
                        # div type is a note then. need additional logic to categorise note location.
                        # DONE: offload logic to separate class?
                        parsed_highlight = KindleHighlights.create_new_note(note_type, note_text)
                    current_chapter.kindle_highlights.append(parsed_highlight)
            chapters.append(current_chapter)
            return chapters[1:] # TODO: first chapter is none for some reason
            # DONE: split object parsing into own function

        except AttributeError as e:
            print(f'Error parsing file: {e}')
            exit(1)

    def parse_chapters(self, chapters):
        def extract_location(kindle_highlight):
            return int(kindle_highlight.location.split(" ")[1])

        for chapter in chapters:
            # TODO chapterwise note parsing
            # Cases:
            # 1. Independent note
            # 2. Note with highlight
            # 3. Independent highlight
            # 4. Highlight with multiple notes
            # TODO: location aware parsing?
            cursor = None
            parsed_kindle_highlights = []

            for i, kindle_highlight in enumerate(chapter.kindle_highlights):
                # TODO: expose controllable location difference?
                # TODO: calculate location difference using highlight text length? a good approximation would be nice in place of an arbitrary value
                # DONE: Better class checking
                if i == 0:
                    cursor = kindle_highlight
                    continue
                if isinstance(kindle_highlight,kindle.Note) and isinstance(cursor, kindle.Highlight) and extract_location(kindle_highlight) - extract_location(cursor) < 4: # cond 2
                    cursor.notes.append(kindle_highlight)
                    continue
                # else:
                parsed_kindle_highlights.append(cursor)
                cursor = kindle_highlight
                # TODO location parsing?
                # if True:
                #     location_marker = extract_location(kindle_highlight)
                #     # TODO: new note?
                #     pass
            # last object left if not condition 2
            parsed_kindle_highlights.append(cursor)
            chapter.kindle_highlights = parsed_kindle_highlights
        return chapters

    def output():
    #TODO: output to file
        # try:
        #     output = output.rstrip('\n')
        #     dest.write_text(output, encoding='UTF-8')
        # except OSError as e:
        #     print(f'Failed to write file: {e}')
        #     exit(1)
        # print(f'Written to: {dest_name}')
        pass

if __name__ == '__main__':
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