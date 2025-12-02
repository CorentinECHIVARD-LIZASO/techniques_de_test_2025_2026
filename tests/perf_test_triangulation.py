import pytest
from unittest.mock import patch
import sys
import os
import uuid
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.point import Point
from src.pointSet import PointSet
from src.triangulator import Triangulator

def create_random_pointset(num_points):
    points = []
    for _ in range(num_points):
        points.append(Point(random.uniform(0, 1000), random.uniform(0, 1000)))
    return PointSet(points)

class TestTriangulationPerformance:

    @pytest.mark.parametrize("num_points", [100, 1000, 10000])
    @patch('src.triangulator.Triangulator.fetch_pointset')
    def test_triangulation_performance(self, mock_fetch_pointset, benchmark, num_points):
        triangulator_instance = Triangulator()
        point_set_id = str(uuid.uuid4())
        
        mock_fetch_pointset.return_value = create_random_pointset(num_points)
        
        result, status_code = benchmark(triangulator_instance.triangulation, point_set_id)
        
        assert status_code == 200
        assert isinstance(result, bytes)
        assert len(result) > 0
        mock_fetch_pointset.assert_called_once_with(point_set_id)
