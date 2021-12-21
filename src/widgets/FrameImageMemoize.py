class RectsMemoized(object):
    def __init__(self) -> None:
        """
        Memoize every rects in the application
        """
        self.RECTS: dict = {}
