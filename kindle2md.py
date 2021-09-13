#!/usr/bin/env python3
#
# This script gets a HTML annotations file exported from the Kindle app
# and convert it to markdown.
#
# Instructions:
# 1. Download this script.
# 2. Be sure to have python installed.
# 3. Install python dependencies: pip3 install --user beautifulsoup4
# 4. Run the script: python3 kindle2md YOUR_FILE.html
#
# Copyright (C) 2021 Rafael Cavalcanti - rafaelc.org
# Licensed under GPLv3
#

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
    # Not providing encoding throws an error on Windows ("deferredreward")
    file_content = source.read_text(encoding='UTF-8')
except OSError as e:
    print(f'Failed to read file: {e}.')
    exit(1)

soup = BeautifulSoup(file_content, 'html.parser')

try:
    note_divs = soup.select("div")[6:]
    book_title = soup.select_one('.bookTitle').contents[0].strip()
    notes = {}
    div_type = None
    chapter = ""
    kindle_highlight = {}
    for i in range(len(note_divs)):
        elem = note_divs[i]
        if 'noteHeading' in elem.attrs['class']:
            note_headers = elem.text.partition('-')
            location_data = note_headers[2].partition('>')
            if elem.text.strip().startswith("Highlight"):
                if kindle_highlight:
                    notes[chapter].append(kindle_highlight)
                    div_type = None
                    chapter = ""
                    kindle_highlight = {}
                color = elem.span.text.title()
                chapter = location_data[0].strip()
                notes.setdefault(chapter,[])
                location = location_data[2].strip()
                div_type = note_headers[0].strip()
                highlight_text = note_divs[i+1].text.strip()
                kindle_highlight = {"type": "highlight", "color": color, "text": highlight_text, "location": location, "notes": []}
            else:
                note_chapter = location_data[0].strip()
                note = note_divs[i+1].text.strip()
                if note_chapter != chapter:
                    notes[chapter].append(kindle_highlight)
                    kindle_highlight = {"type": "note", "text": note, "location": location}
                    chapter = note_chapter
                    notes.setdefault(chapter,[])
                    notes[chapter].append(kindle_highlight)
                elif kindle_highlight["type"] == "highlight":
                    kindle_highlight["notes"].append(note)
                else:
                    notes[chapter].append(kindle_highlight)
    notes[chapter].append(kindle_highlight)

except AttributeError as e:
    print(f'Error parsing file: {e}')
    exit(1)

output = f'# {book_title}\n\n'
pandoc_div = ":::"
for chapter in notes:
    output += f'## {chapter}\n\n'
    for kindle_highlight in notes[chapter]:
        entry = pandoc_div
        if kindle_highlight["type"] == "note":
            entry += "\n"
            entry += f'> {kindle_highlight["text"]}\n'
        if kindle_highlight["type"] == "highlight":
            entry += f'{kindle_highlight["color"].lower()}\n\n'
            entry += f'> {kindle_highlight["text"]}\n\n'
            for note in kindle_highlight["notes"]:
                entry += f'{note}\n\n'
        entry += pandoc_div + "\n"
        output += entry + "\n"

try:
    dest.write_text(output, encoding='UTF-8')
except OSError as e:
    print(f'Failed to write file: {e}')
    exit(1)
print(f'Written to: {dest_name}')