from src.point import Point


class PointSet:
    def __init__(self, points: list[Point] = []):
        self.points = points

    def to_binary(self) -> bytes:
        """
        Return the binary form of the PointSet object

        Returns:
            200 -> Conversion successful
                -> Return the binary form of the PointSet object
            500 -> Internal server error, e.g., conversion failed 
                -> Return the error message following this format :
                    -> "CONVERTION_FAILED - Conversion could not be computed : {reason}"
        """
        pass

    def from_binary(data: bytes) -> 'PointSet':
        """
        Return the PointSet object from the binary form

        Args:
            data (bytes): The binary form of the PointSet object
        Returns:
            200 -> Conversion successful
                -> Return the PointSet object
            550 -> Internal server error, e.g., conversion failed
                -> Return the error message following this format :
                    -> "CONVERTION_FAILED - Conversion could not be computed : Internal server error"
            400 -> Bad request, e.g., invalid data format
                -> Return the errir message following this format :
                    -> "CONVERSION_FAILED - Conversion could not be computed : Invalid data format"
        """
        pass
