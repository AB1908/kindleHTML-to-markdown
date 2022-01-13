from enum import Enum

# DONE: Fix super() usage file wide

class HighlightColor(Enum):

    # DOC: Note that this is dependent on the app itself.
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
        header_div -- 
        text_div -- 
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
        # TODO: check chapter numbering and creation? maybe this should be offloaded to diff class
        return Highlight(highlight_chapter, highlight_location, highlight_color, highlight_text)

    def create_new_note(self, header_div, text_div):
        """Extract data to create a note and invoke constructor.

        Keyword arguments:
        header_div -- 
        text_div -- 
        """
        # DONE standardise args for both funcs
        location_metadata = header_div.text.strip().partition('-')[2].partition('>')
        chapter = location_metadata[0].strip()
        location = location_metadata[2].strip()
        text = text_div.text.strip()
        note = Note(chapter, location, text)
        return note

class Highlight(AnnotationObject):

    def is_highlight(self):
        return True

    def __eq__(highlight1, highlight2):
        if len(highlight1.notes) != len(highlight2.notes):
            return False
        for i in range(len(highlight2.notes)):
            if highlight1.notes[i] != highlight2.notes[i]:
                return False
        highlight1_dict = vars(highlight1)
        highlight2_dict = vars(highlight2)
        del highlight1_dict["notes"]
        del highlight2_dict["notes"]
        return highlight1_dict == highlight2_dict

    def __init__(self, chapter, location, color, text):
        self.color = color
        self.notes = []
        super().__init__(chapter, location, text)

class Note(AnnotationObject):
    #Note object that contains note data like location and text
    # Its relation to a highlight is best left to be determined in the KindleHighlight.
    # As of now, it is a mystery as to how a note is standalone or related.
    # Hence the highlight and note objects have been kept separate as it cannot be discerned from the source.
    # TODO: note.is_standalone()?
    # DONE: note structure testing

    def is_highlight(self):
        return False

    def __eq__(note1, note2):
        return vars(note1) == vars(note2)

    def __init__(self, chapter, location, text):
        super().__init__(chapter, location, text)

class Chapter():

    def __eq__(chap1, chap2):
        if len(chap1.kindle_highlights) != len(chap2.kindle_highlights):
            return False
        for i in range(len(chap1.kindle_highlights)):
            if chap1.kindle_highlights[i] != chap2.kindle_highlights[i]:
                return False
        chap1_dict = vars(chap1)
        chap2_dict = vars(chap2)
        del chap1_dict["kindle_highlights"]
        del chap2_dict["kindle_highlights"]
        return chap1_dict == chap2_dict
        # highlight1_dict = vars(highlight1)
        # highlight2_dict = vars(highlight2)
        # del highlight1_dict["notes"]
        # del highlight2_dict["notes"]
        # return highlight1_dict == highlight2_dict
        # if 
        # for i in range(len(chap1.kindle_highlights))
        # return chap1.name == chap2.name and chap1.kindle_highlights == chap2.kindle_highlights

    def __init__(self, chapter_name):
        self.kindle_highlights = []
        self.name = chapter_name.strip()
        # generate unique id from chapter name to avoid name collison?
        # TODO
        self.chapter_id = True
    
    def is_current_chapter(self, chapter_name):
        # TODO: potential edge case - same chapter names for two diff chapters
        """Check if the chapter heading points to the current chapter object"""
        return self.chapter_name == chapter_name

class Book():

    def __init__(self, title):
        self.chapters = []
        self.title = title.strip()