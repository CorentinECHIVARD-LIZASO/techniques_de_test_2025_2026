import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.point import Point
from src.pointSet import PointSet


class TestPointSet:
    def test_pointset_nominal(self):
        pointsList = [Point(1, 2), Point(3, 4), Point(5, 6)]
        pointSet = PointSet(pointsList)
        binary_data = pointSet.to_binary()
        assert binary_data.code == 200
        expected_binary = b'000000110000000000000000000000000000000000000000100000000011111100000000000000000000000001000000000000000000010001000000000000000000000001000000000000000000101001000000000000000000000001000000000000000000110001000000'
        assert binary_data.data == expected_binary
        
        pointSet2 = PointSet.from_binary(binary_data.data)
        assert pointSet2.code == 200
        assert pointSet2.points == pointsList

    def test_pointset_donnees_vides(self):
        pointSet = PointSet()
        with pytest.raises(ValueError):
            pointSet.to_binary()

    def test_pointset_to_binary_invalid_content(self):
        pointsList = [Point(1, 2), "not-a-point", Point(5, 6)]
        pointSet = PointSet(pointsList)
        with pytest.raises(TypeError):
            pointSet.to_binary()

    def test_pointset_from_binary_contradictory_data(self):
        # Announce de 10 points, mais en donne que 1
        binary_data = b'00001010000000000000000000000000' + b'0' * 64
        with pytest.raises(ValueError):
            PointSet.from_binary(binary_data)

    def test_pointset_from_binary_invalid_length(self):
        # Annonce de 1 point, mais longeure de données incorrecte 
        binary_data = b'00000001000000000000000000000000' + b'0' * 60
        with pytest.raises(ValueError):
            PointSet.from_binary(binary_data)