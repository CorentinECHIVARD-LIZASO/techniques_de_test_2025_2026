from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid

from src.point import Point
from src.pointSet import PointSet
from src.triangulator import Triangulator


class TestTriangulation:

    @patch('src.triangulator.Triangulator.fetch_pointset')
    def test_triangulation_nominal(self, mock_fetch_pointset):
        triangulator_instance = Triangulator()
        point_set_id = str(uuid.uuid4())
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        mock_fetch_pointset.return_value = PointSet(points)
        
        result, status_code = triangulator_instance.triangulation(point_set_id)
        
        mock_fetch_pointset.assert_called_once_with(point_set_id)
        assert status_code == 200
        assert isinstance(result, bytes)
        assert len(result) > 0
    
    @patch('src.triangulator.Triangulator.fetch_pointset')
    def test_triangulation_pointset_not_found(self, mock_fetch_pointset):
        triangulator_instance = Triangulator()
        point_set_id = str(uuid.uuid4())
        mock_fetch_pointset.return_value = None
        
        result, status_code = triangulator_instance.triangulation(point_set_id)
        
        mock_fetch_pointset.assert_called_once_with(point_set_id)
        assert status_code == 404
        assert "not found" in result['message'].lower()
    
    def test_triangulation_bad_pointset_id_format(self):
        triangulator_instance = Triangulator()
        malformed_id = "not-an-int"
        
        result, status_code = triangulator_instance.triangulation(malformed_id)
        
        assert status_code == 400
        assert "malformed" in result['message'].lower()
    
    @patch('src.triangulator.Triangulator.fetch_pointset')
    def test_triangulation_with_insufficient_points(self, mock_fetch_pointset):
        triangulator_instance = Triangulator()
        point_set_id = 2
        points = [Point(0, 0), Point(1, 1)]
        mock_fetch_pointset.return_value = PointSet(points)
        
        result, status_code = triangulator_instance.triangulation(point_set_id)
        
        mock_fetch_pointset.assert_called_once_with(point_set_id)
        assert status_code == 422 # Unprocessable Entity
        assert "insufficient points" in result['message'].lower()