import json

from PySide6.QtCore import QPoint


class Annotation(object):
    def __init__(
            self,
            begin: QPoint,
            destination: QPoint,
            categorie: str,
            fPath: str):
        self.coords = (begin, destination)
        self.categorie = categorie
        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]


class AnnotateManager(object):
    annotations = {}

    @staticmethod
    def addAnnotation(fName, annotation: Annotation):
        if fName not in AnnotateManager.annotations:
            AnnotateManager.annotations[fName] = {
                "annotations": []
            }
        AnnotateManager.annotations[fName]["annotations"].append(
            {
                "path": annotation.fPath,
                "categorie": annotation.categorie,
                "coords": {
                    "beginX": annotation.coords[0].x(),
                    "beginY": annotation.coords[0].y(),
                    "destinationX": annotation.coords[1].x(),
                    "destinationY": annotation.coords[1].y()
                }
            }
        )

    @staticmethod
    def exportToJson(name):
        print("Saving annotated images as json...")
        with open(name, "w+") as f:
            f.write(json.dumps(AnnotateManager.annotations, indent=2))

    @staticmethod
    def reset():
        AnnotateManager.annotations = {}
