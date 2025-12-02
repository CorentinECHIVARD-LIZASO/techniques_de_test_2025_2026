from flask import Flask
from src import triangulator

app = Flask(__name__)


@app.route('/triangulation/<pointSetId>', methods=['GET'])
def get_triangulation_route(pointSetId):
    """
        Calculate triangulation for a PointSet

        Requests the triangulation for a given PointSetID.
        The service will internally fetch the PointSet from the
        PointSetManager, compute the triangulation, and return
        the 'Triangles' structure in binary format.

        Args:
            pointSetId (int): The UUID of the PointSet to triangulate.
        Returns:
            200 -> Triangulation successful.
                -> Return the Triangles structure in binary format.
        Errors : "TRIANGULATION_FAILED - Triangulation could not be computed for the given point set. : {reason}"
            400 -> Bad request, e.g., invalid PointSetID format.
            404 -> The specified PointSetID was not found (as reported by the PointSetManager).
            500 -> Internal server error, e.g., triangulation algorithm failed.
            503 -> Service unavailable, e.g.  communication with PointSetManager failed.
    """
    
    triangulator_instance = triangulator.Triangulator()
    result, status_code = triangulator_instance.triangulation(pointSetId)
    return result, status_code