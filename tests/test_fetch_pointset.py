import pytest
import requests
from unittest.mock import patch, MagicMock
import struct
import uuid
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.point import Point
from src.pointSet import PointSet
from src.triangulator import Triangulator


def create_binary_pointset_data(points):
    num_points_str = ''.join(f'{b:08b}' for b in struct.pack('<L', len(points)))
    binary_data_str = num_points_str
    for p in points:
        binary_data_str += ''.join(f'{b:08b}' for b in struct.pack('<ff', float(p.x), float(p.y)))
    return bytes(binary_data_str, 'utf-8')


class TestFetchPointSet:

    @patch('requests.get')
    def test_fetch_pointset_success(self, mock_get):
        triangulator_instance = Triangulator()
        
        point_set_id = str(uuid.uuid4())
        points_data = [Point(0, 0), Point(10, 0), Point(5, 10)]
        binary_data = create_binary_pointset_data(points_data)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = binary_data
        
        mock_response.url = f"/pointset/{point_set_id}"
        mock_get.return_value = mock_response
        
        point_set = triangulator_instance.fetch_pointset(point_set_id)

        mock_get.assert_called_once()
        assert isinstance(point_set, PointSet)
        assert len(point_set.points) == len(points_data)
        assert point_set.points[1].x == 10.0

    @patch('requests.get')
    def test_fetch_pointset_not_found(self, mock_get):
        triangulator_instance = Triangulator()
        point_set_id = str(uuid.uuid4())

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'code': 'NOT_FOUND', 'message': 'PointSet not found.'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            triangulator_instance.fetch_pointset(point_set_id)

        assert excinfo.value.response.status_code == 404

    @patch('requests.get')
    def test_fetch_pointset_bad_id_format_from_client(self, mock_get):
        triangulator_instance = Triangulator()

        with pytest.raises(ValueError):
            triangulator_instance.fetch_pointset("this-is-not-a-uuid")

        mock_get.assert_not_called()