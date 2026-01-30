from werkzeug.routing import BaseConverter

# Make sure that routes are only valid if media type is tv or movie
class MediaTypeConverter(BaseConverter):
    def __init__(self, url_map):
        super().__init__(url_map)
        self.regex = "(tv|movie)"