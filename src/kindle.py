from enum import Enum

class HighlightColor(Enum):

    # DOC: Note that this is dependent on the app itself.
    YELLOW = 1
    BLUE = 2
    PINK = 3
    ORANGE = 4

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

class KindleAnnotations:
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
        if len(chap1.annotations) != len(chap2.annotations):
            return False
        for i in range(len(chap1.annotations)):
            if chap1.annotations[i] != chap2.annotations[i]:
                return False
        chap1_dict = vars(chap1)
        chap2_dict = vars(chap2)
        del chap1_dict["annotations"]
        del chap2_dict["annotations"]
        return chap1_dict == chap2_dict

    def __init__(self, chapter_name):
        self.annotations = []
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