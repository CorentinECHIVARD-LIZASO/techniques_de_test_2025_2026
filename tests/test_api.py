import pytest
from unittest.mock import patch
import uuid
from src.api import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.testing = True
    with app.test_client() as client:
        yield client


class TestApi:

    @patch('src.api.triangulator.Triangulator.triangulation')
    def test_api_nominal(self, mock_get_triangulation, client):
        binary_string = "0000000100000000000000000000000000000011000000000000000000000000000000001000000000111111000000000000000001000000000000000100000001000000000000001000000001000000000000001010000001000000000000001100000001000000"
        binary_triangles = bytes(binary_string, 'utf-8')
        mock_get_triangulation.return_value = (binary_triangles, 200)
        
        point_set_id = str(uuid.uuid4())
        response = client.get(f'/triangulation/{point_set_id}')

        mock_get_triangulation.assert_called_once_with(point_set_id)
        assert response.status_code == 200
        assert response.data == binary_triangles

    @patch('src.api.triangulator.Triangulator.triangulation')
    def test_api_pointset_inexistant(self, mock_get_triangulation, client):
        error_response = {"code": "NOT_FOUND", "message": "The specified PointSetID was not found."}
        mock_get_triangulation.return_value = (error_response, 404)

        point_set_id = str(uuid.uuid4())
        response = client.get(f'/triangulation/{point_set_id}')
        
        assert response.status_code == 404
        assert response.is_json
        assert response.get_json() == error_response

    @patch('src.api.triangulator.Triangulator.triangulation')
    def test_api_pointset_manager_indisponible(self, mock_get_triangulation, client):
        error_response = {"code": "SERVICE_UNAVAILABLE", "message": "Communication with PointSetManager failed."}
        mock_get_triangulation.return_value = (error_response, 503)

        point_set_id = str(uuid.uuid4())
        response = client.get(f'/triangulation/{point_set_id}')
        
        assert response.status_code == 503
        assert response.is_json
        assert response.get_json() == error_response

    @patch('src.api.triangulator.Triangulator.triangulation')
    def test_api_pointset_id_mal_formate(self, mock_get_triangulation, client):
        error_response = {"code": "BAD_REQUEST", "message": "Invalid PointSetID format."}
        mock_get_triangulation.return_value = (error_response, 400)

        response = client.get('/triangulation/not-a-valid-uuid')

        assert response.status_code == 400
        assert response.is_json
        assert response.get_json() == error_response

    def test_api_methode_non_autorisee(self, client):
        point_set_id = str(uuid.uuid4())
        
        response_put = client.put(f'/triangulation/{point_set_id}')
        assert response_put.status_code == 405

        response_delete = client.delete(f'/triangulation/{point_set_id}')
        assert response_delete.status_code == 405