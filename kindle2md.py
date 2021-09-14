#!/usr/bin/env python3
#
# This script gets a HTML annotations file exported from the Kindle app
# and convert it to markdown.


from pathlib import Path
from os.path import basename, splitext
from sys import argv, exit
from bs4 import BeautifulSoup

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

try:
    file_content = source.read_text(encoding='UTF-8')
except OSError as e:
    print(f'Failed to read file: {e}.')
    exit(1)

soup = BeautifulSoup(file_content, 'html.parser')

def consume_highlight(text_div, header_div, location_data):
    color = header_div.span.text.title()
    highlight_location = location_data[2].strip()
    highlight_text = text_div.text.strip()
    kindle_highlight = {"type": "highlight", "color": color, "text": highlight_text, "location": highlight_location, "notes": []}
    return kindle_highlight

def chapter_init(notes, location_data):
    chapter_marker = location_data[0].strip()
    notes.setdefault(chapter_marker,[])
    return chapter_marker

def create_new_note(notes, chapter_marker, kindle_highlight, location, note):
    notes[chapter_marker].append(kindle_highlight)
    kindle_highlight = {"type": "note", "text": note, "location": location}
    return kindle_highlight

try:
    note_divs = soup.findAll("div", {'class': ["noteHeading","noteText"]})
    book_title = soup.select_one('.bookTitle').contents[0].strip()
    kindle_notes = {}
    chapter_marker = chapter_init(kindle_notes, note_divs[0].text.partition('-')[2].partition('>'))
    kindle_highlight = {}
    for i in range(len(note_divs)):
        elem = note_divs[i]
        if 'noteHeading' in elem.attrs['class']:
            note_headers = elem.text.partition('-')
            location_data = note_headers[2].partition('>')
            note_location = location_data[2].strip()
            if elem.text.strip().startswith("Highlight"):
                if kindle_highlight:
                    kindle_notes[chapter_marker].append(kindle_highlight)
                    chapter_marker = chapter_init(kindle_notes, location_data)
                kindle_highlight = consume_highlight(note_divs[i+1], elem, location_data)
            else:
                note_chapter = location_data[0].strip()
                note_text = note_divs[i+1].text.strip()
                if note_chapter != chapter_marker:
                    kindle_highlight = create_new_note(kindle_notes, chapter_marker, kindle_highlight, note_location, note_text)
                    chapter_marker = chapter_init(kindle_notes, location_data)
                elif kindle_highlight["type"] == "highlight":
                    kindle_highlight["notes"].append(note_text)
                elif kindle_highlight["type"] == "note":
                    kindle_highlight = create_new_note(kindle_notes, chapter_marker, kindle_highlight, note_location, note_text)
                else:
                    raise Exception
    kindle_notes[chapter_marker].append(kindle_highlight)

except AttributeError as e:
    print(f'Error parsing file: {e}')
    exit(1)

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