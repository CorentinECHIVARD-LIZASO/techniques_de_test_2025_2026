import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.point import Point

class testPoint:
    def test_point_creation(self):
        p = Point(3, 4)
        assert p.x == 3
        assert p.y == 4

    
    def test_point_to_binary(self):
        p = Point(1, 2)
        binary_data = p.to_binary()
        expected_data = b'0000000000000000100000000011111100000000000000000000000001000000'
        assert binary_data == expected_data
