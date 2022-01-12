from math import sin, cos, atan2, sqrt, pi


class Node:
    def __init__(self, _id, lat=None, lon=None):
        self.id = _id
        self.lat = lat
        self.lon = lon

    def set_coords(self, lat, lon):
        self.lat = lat
        self.lon = lon


def convert_to_radian(x: float) -> float:
    return x * pi / 180


def get_distance(n1: Node, n2: Node) -> float:
    R = 6378137  # Earth’s mean radius in meter
    dLat = convert_to_radian(n2.lat - n1.lat)
    dLong = convert_to_radian(n2.lon - n1.lon)
    a = sin(dLat / 2) * sin(dLat / 2) + cos(convert_to_radian(n1.lat)) * cos(convert_to_radian(n2.lat)) \
        * sin(dLong / 2) * sin(dLong / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    return round(d, 1)


def calculate_polygon_area(coordinates: list[Node]) -> float:
    R = 6378137  # Earth’s mean radius in meter
    area = 0
    if len(coordinates) > 2:
        for i in range(len(coordinates) - 1):
            p1 = coordinates[i]
            p2 = coordinates[i + 1]
            area += convert_to_radian(p2.lon - p1.lon) * (
                        2 + sin(convert_to_radian(p1.lat)) + sin(convert_to_radian(p2.lat)))
        area = area * pow(R, 2) / 2
    return round(abs(area), 1)


if __name__ == '__main__':
    node1, node2 = Node(1), Node(2)
    node1.set_coords(-25.9791692, 32.5772479)
    node2.set_coords(-25.9789443, 32.5773481)
    print(get_distance(node1, node2))
