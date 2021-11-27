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

    def create(self):
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