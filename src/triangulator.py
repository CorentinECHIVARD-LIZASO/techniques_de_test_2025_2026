from src.pointSet import PointSet
class Triangulator :


    def __init__(self):
        self.triangles = None
        self.pointset = PointSet

    def fetch_pointset(self, pointSetId: int) -> PointSet:
        """
            Récupère le PointSet depuis une source externe (ex: API, base de données, etc.) en utilisant l'identifiant `pointSetID`.
            Retourne un objet PointSet et met à jour l'attribut `self.pointset` de l'object.
        """
        pass

    def triangulation(self, pointSetId: int) -> tuple[bytes | dict, int]:
        """
            Triangule le PointSet en utilisant l'identifiant `pointSetID`.

            Args :
                - pointSetId (int) : L'identifiant du PointSet à trianguler.
            Returns :
                - 200 -> Triangulation successful.
                    -> Return the Triangulation structure in binary format.
                - 404 -> The specified PointSetID was not found (as reported by the PointSetManager).
                
        """
        pass