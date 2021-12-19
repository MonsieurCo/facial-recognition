import json

from PySide6.QtCore import QPoint


class Annotation(object):
    def __init__(
            self,
            id: str,
            begin: QPoint,
            destination: QPoint,
            categorie: str,
            fPath: str,
            categorie_id: int,
            width: int,
            height: int):
        self.id = id
        self.coords = (begin, destination)
        self.categorie = categorie
        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        self.categorie_id = categorie_id
        self.size = (width, height)


class AnnotateManager(object):
    annotations = {}

    @staticmethod
    def addAnnotation(fName, annotation: Annotation):
        if fName not in AnnotateManager.annotations:
            AnnotateManager.annotations[fName] = {
                "annotations": []
            }
        AnnotateManager.annotations[fName]["annotations"].append({
            "id": annotation.id,
            "path": annotation.fPath,
            "categorie": annotation.categorie,
            "categorie_id": annotation.categorie_id,
            "coords": {
                "beginX": annotation.coords[0].x(),
                "beginY": annotation.coords[0].y(),
                "destinationX": annotation.coords[1].x(),
                "destinationY": annotation.coords[1].y()
            },
            "img-size": {
                "width": annotation.size[0],
                "height": annotation.size[1]
            }
        })

    @staticmethod
    def exportToJson(name):
        print("Saving annotated images as json...")
        with open(name, "w+") as f:
            f.write(json.dumps(AnnotateManager.annotations, indent=2))

    @staticmethod
    def reset():
        AnnotateManager.annotations = {}

    @staticmethod
    def deleteAnnotation(catName):
        annotationToDelete = []
        for k, v in AnnotateManager.annotations.items():
            for kAnnot, vAnnot in v.items():
                for annotation in vAnnot:
                    if annotation["categorie"] == catName:
                        annotationToDelete.append(annotation)
                for annatToDelete in annotationToDelete:
                    vAnnot.remove(annatToDelete)

    @staticmethod
    def changeAnnotation(catName, oldName):
        for k, v in AnnotateManager.annotations.items():
            for kAnnot, vAnnot in v.items():
                for annotation in vAnnot:
                    if annotation["categorie"] == oldName:
                        annotation["categorie"] = catName

    @staticmethod
    def deleteAnnotationByCoord(XBegin, YBegin):
        annotationToDelete = []
        for k, v in AnnotateManager.annotations.items():
            for kAnnot, vAnnot in v.items():
                for annotation in vAnnot:
                    if annotation["coords"]["beginX"] == XBegin and annotation["coords"]["beginY"] == YBegin:
                        annotationToDelete.append(annotation)
                for annatToDelete in annotationToDelete:
                    vAnnot.remove(annatToDelete)
