class AnnotationObject:

    def __init__(self, chapter, location, text):
        this.text = text
        this.location = location
        this.chapter = chapter

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
    kindle_highlight = {"type": "highlight", "color": color, "text": highlight_text, "location": highlight_location, "notes": []}

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