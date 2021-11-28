from PySide6.QtCore import QPoint


class Annotation(object):
    def __init__(
            self,
            begin: QPoint,
            destination: QPoint,
            categorie: str,
            fPath: str):
        self._coords = (begin, destination)
        self.categorie = categorie
        self.fPath = fPath

    @property
    def categorie(self):
        return self.categorie

    @property
    def fPath(self):
        return self.fPath

    @property
    def coords(self):
        return self._coords


class AnnotateManager(object):
    def __init__(self):
        self.annotations = []

    def addAnnotation(self, annotation: Annotation):
        self.annotations.append(annotation)

    @property
    def annotations(self):
        return self.annotations

    def exportToJson(self):
        dic = {}
        for annotation in self.annotations:
            # dic[]
            pass
