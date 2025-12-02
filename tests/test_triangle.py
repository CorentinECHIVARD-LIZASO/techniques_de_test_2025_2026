import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.point import Point
from src.pointSet import PointSet
from src.triangle import Triangle


class TestTriangle :
    
    def test_triangle_nominal(self):
        pointList = [Point(1, 2), Point(3, 4), Point(5, 6)]
        pointSet = PointSet(pointList)

        triangle = Triangle(pointSet)
        binary_data = triangle.to_binary()

        assert binary_data.code == 200
        expected_binary = b'000000110000000000000000000000000000000000000000100000000011111100000000000000000000000001000000000000000000010001000000000000000000000001000000000000000000101001000000000000000000000001000000000000000000110001000000'
        assert binary_data.data == expected_binary

        triangle2 = Triangle.from_binary(binary_data.data)
        assert triangle2.points == pointSet

    def test_triangle_donnees_vides(self):
        with pytest.raises(ValueError):
            triangle = Triangle()