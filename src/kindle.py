from enum import Enum

# TODO: Fix super() usage file wide

class HighlightColor(Enum):

    # Note that this is dependent on the app itself.
    PINK = 3
    ORANGE = 4
    BLUE = 2
    YELLOW = 1

    def __eq__(color1, color2):
        return color1.value == color2.value

    @staticmethod
    def get_color(color_text):
        if color_text == "pink":
            color = HighlightColor.PINK
        elif color_text == "blue":
            color = HighlightColor.BLUE
        elif color_text == "yellow":
            color = HighlightColor.YELLOW
        elif color_text == "orange":
            color = HighlightColor.ORANGE
        else:
            raise Exception("Undefined color")
        return color

class AnnotationObject:

    def __init__(self, chapter, location, text):
        self.text = text
        self.location = location
        self.chapter = chapter

    # The object's format and type is unknown so this must be implemented in derived class.
    def export_as_markdown(self):
        raise NotImplementedError("Implement this method")

class KindleMarkdown():
    # list of highlights?

    # TODO

    pass

class KindleHighlights:
    # Pass input to this class which parses
    # Also keep a separate export method for each class?
    # Allow overriding?
    # TODO: parse highlights

    def __eq__(kh1, kh2):
        from kindle import Highlight
        if isinstance(kh1, Highlight) and isinstance(kh2, Highlight):
            return True


    # TODO: offload responsibility of html parsing to parser class?
    def create_text_highlight(self, header_div, text_div):
        """Extract data to create a highlight and invoke constructor.

        Keyword arguments:
        real -- the real part (default 0.0)
        imag -- the imaginary part (default 0.0)
        """ 
        #TODO: add div ordering validation? Eg. noteText must come after noteHeading class
        location_metadata = header_div.text.partition('-')[2].partition('>')
        highlight_color = HighlightColor.get_color(header_div.span.text) 
        highlight_location = location_metadata[2].strip()
        # [Highlight (<span class="highlight_pink">pink</span>), -, PREFACE TO THE CHARLES DICKENS EDITION >  Location 103]
                    # [chapter_heading, >, location]
        highlight_text = text_div.text.strip()
        highlight_chapter = location_metadata[0].strip()
        # TODO: check chapter text and chapter object?
        # TODO: check chapter numbering and creation?
        return Highlight(highlight_chapter, highlight_location, highlight_color, highlight_text)

    def create_new_note(self, header_div, text_div):
        """Extract data to create a note and invoke constructor.

        Keyword arguments:
        text_div -- 
        location_metadata -- 
        """
        # notes[chapter_marker].append(kindle_highlight)
        # check div for chapter
        # depending on chapter, later parse
        # TODO standardise args for both funcs
        location_metadata = header_div.text.partition('-')[2].partition('>')
        chapter = location_metadata[0].strip()
        location = location_metadata[2].strip()
        text = text_div.text.strip()
        note = Note(chapter, location, text)
        return note

    def parse_notes(self):
        pass


class Highlight(AnnotationObject):
    def __init__(self, chapter, location, color, text):
        this.color = color
        this.text = text
        this.location = location
        this.chapter = chapter
        this.notes = []

    def export_as_markdown(self):
        # TODO
        return ""

class Note(AnnotationObject):
    #Note object that contains note data like location and text
    # Its relation to a highlight is best left to be determined in the KindleHighlight.
    # As of now, it is a mystery as to how a note is standalone or related.
    # Hence the highlight and note objects have been kept separate as it cannot be discerned from the source.
    # TODO: note.is_standalone()?
    # TODO: note structure testing

    def __init__(self, chapter, location, text):
        super(chapter, location, text)

    def export_as_markdown(self):
        # TODO
        pass