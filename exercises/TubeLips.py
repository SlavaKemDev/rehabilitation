from Geometry2D import *


class TubeLips:
    def load(self, points):
        '''point61 = Point(points[61][0], points[61][1])
        point62 = Point(points[62][0], points[62][1])
        point63 = Point(points[63][0], points[63][1])

        point65 = Point(points[65][0], points[65][1])
        point66 = Point(points[66][0], points[66][1])
        point67 = Point(points[67][0], points[67][1])

        segment1 = Segment(point61, point67)
        segment2 = Segment(point62, point66)
        segment3 = Segment(point63, point65)

        len1 = segment1.length if point61.y < point67.y else -segment1.length
        len2 = segment2.length if point62.y < point66.y else -segment2.length
        len3 = segment3.length if point63.y < point65.y else -segment3.length

        avg = (len1 + len2 + len3) / 3

        return avg > 15'''
        point51 = Point(points[51][0], points[51][1])
        point57 = Point(points[57][0], points[57][1])
        vertical_segment = Segment(point51, point57)

        point48 = Point(points[48][0], points[48][1])
        point54 = Point(points[54][0], points[54][1])
        horizontal_segment = Segment(point48, point54)

        return horizontal_segment.length / vertical_segment.length < 2.5
