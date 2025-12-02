import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.point import Point
from src.pointSet import PointSet
from src.triangle import Triangle
from src.triangles import Triangles


class TestTriangles:

    def test_triangle_nominal(self):
        pointList = [Point(1, 2), Point(3, 4), Point(5, 6)]
        pointSet = PointSet(pointList)

        trianglesList = [Triangle(pointSet), Triangle(pointSet), Triangle(pointSet)]
        Triangles = Triangles(trianglesList)
        binary_data = Triangles.to_binary()
        assert binary_data.code == 200

        triangle_binary = b'000000110000000000000000000000000000000000000000100000000011111100000000000000000000000001000000000000000000010001000000000000000000000001000000000000000000101001000000000000000000000001000000000000000000110001000000'
        expected_binary = b'00000011000000000000000000000000' + triangle_binary * 3
        assert binary_data.data == expected_binary
        
        Triangles2 = Triangles.from_binary(binary_data.data)
        assert Triangles2.code == 200
        assert Triangles2.triangles == trianglesList
        

    def test_triangle_donnees_contradictoires(self):
        BinaryTriangles = b'00000001000000000000000000000000'

        with pytest.raises(ValueError):
            Triangles.from_binary(BinaryTriangles)

    def test_triangles_to_and_from_binary_integration(self):
        points1 = [Point(1, 1), Point(2, 2), Point(1, 2)]
        points2 = [Point(3, 3), Point(4, 4), Point(3, 4)]
        trianglesList = [Triangle(PointSet(points1)), Triangle(PointSet(points2))]
        original_triangles = Triangles(trianglesList)

        binary_data = original_triangles.to_binary()
        reconstructed_triangles = Triangles.from_binary(binary_data.data)

        assert reconstructed_triangles.triangles == original_triangles.triangles