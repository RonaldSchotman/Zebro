import math
import string
from typing import Dict
from typing import List


def are_fuzzy_equal(value_1, value_2, fuzziness):
    # type: (float, float, float) -> bool
    return value_2 - fuzziness < value_1 < value_2 + fuzziness


class Point(object):
    def __init__(self, x, y):
        # type: (float, float) -> None
        self.__x = x
        self.__y = y
        self.__line_segments_from_this_point = []
        self.__line_segments_that_connect_line_segments_from_this_point = []

    @property
    def x(self):
        # type: () -> float
        return self.__x

    @property
    def y(self):
        # type: () -> float
        return self.__y

    @property
    def line_segments_from_this_point(self):
        # type: () -> List[LineSegment]
        return self.__line_segments_from_this_point

    @property
    def line_segments_that_connect_line_segments_from_this_point(self):
        # type: () -> List[LineSegment]
        return self.__line_segments_that_connect_line_segments_from_this_point

    def __repr__(self):
        return '<Point(x={}, y={})>'.format(self.__x, self.__y)

    def distance_to(self, other_point):
        # type: (Point) -> float
        delta_x = abs(self.x - other_point.x)
        delta_y = abs(self.y - other_point.y)
        distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)  # pythagoras
        return distance

    def add_line_segment_from_this_point(self, link):
        # type: (LineSegment) -> None
        self.__line_segments_from_this_point.append(link)

    def add_line_segment_that_connect_line_segments_from_this_point(self, line_segment):
        # type: (LineSegment) -> None
        self.__line_segments_that_connect_line_segments_from_this_point.append(line_segment)

    def sort_line_segments_by_length(self):
        self.__line_segments_from_this_point = sorted(self.line_segments_from_this_point, key=lambda link: link.length)

    def find_line_segments_that_connect_line_segments_from_this_point(self):
        connected_points = []
        for line_segment in self.line_segments_from_this_point:
            connected_points.append(line_segment.get_other_point(self))

        for connected_point in connected_points:
            for line_segment in connected_point.line_segments_from_this_point:
                if (
                    line_segment.get_other_point(connected_point) in connected_points
                    and line_segment not in self.__line_segments_that_connect_line_segments_from_this_point
                ):
                    self.add_line_segment_that_connect_line_segments_from_this_point(line_segment)


class LineSegment(object):
    def __init__(self, point_1, point_2):
        # type: (Point, Point) -> None
        self.__length = point_1.distance_to(point_2)

        self.__point_1 = point_1
        self.__point_2 = point_2
        self.__relative_length = 0

        point_1.add_line_segment_from_this_point(self)
        point_2.add_line_segment_from_this_point(self)

    def starts_or_ends_in(self, point):
        # type: (Point) -> bool
        return self.__point_1 is point or self.__point_2 is point

    @property
    def point_1(self):
        # type: () -> Point
        return self.__point_1

    @property
    def point_2(self):
        # type: () -> Point
        return self.__point_2

    @property
    def length(self):
        # type: () -> float
        return self.__length

    @property
    def relative_length(self):
        # type: () -> float
        return self.__relative_length

    def __repr__(self):
        return '<LineSegment({}, {})>'.format(self.__point_1, self.__point_2)

    def calculate_relative_length(self, scale):
        self.__relative_length = self.length / scale

    def get_other_point(self, point):
        # type: (Point) -> Point or None
        if self.__point_1 is point:
            return self.__point_2
        elif self.point_2 is point:
            return self.__point_1
        else:
            return None

    # returns the first common point found
    def get_common_point(self, other_line_segment):
        # type: (LineSegment) -> Point or None

        if other_line_segment.starts_or_ends_in(self.__point_1):
            return self.__point_1
        elif other_line_segment.starts_or_ends_in(self.__point_2):
            return self.__point_2
        else:
            return None


class RightTriangle(object):
    def __init__(self, leg_a, leg_b, hypotenuse_c):
        self.__leg_a = leg_a
        self.__leg_b = leg_b
        self.__hypotenuse_c = hypotenuse_c

        self.__right_angle = self.__leg_a.get_common_point(self.__leg_b)
        self.__acute_angle_a = self.__leg_a.get_common_point(self.__hypotenuse_c)
        self.__acute_angle_b = self.__leg_b.get_common_point(self.__hypotenuse_c)

    def get_angles(self):
        return [self.__right_angle, self.__acute_angle_a, self.__acute_angle_b]

    def __repr__(self):
        return '<RightTriangle({}, {}, {})>'.format(self.__right_angle, self.__acute_angle_a, self.__acute_angle_b)

    def get_rotation_angle(self):
        # type: () -> float
        front_point = self.__right_angle
        back_point = self.__acute_angle_b

        x = front_point.x - back_point.x
        y = front_point.y - back_point.y

        rotation_angle_in_radians = 0

        quarter = math.pi / 2

        if x == 0:
            if y > 0:
                rotation_angle_in_radians = 0 * quarter        # 0 degrees
            else:
                rotation_angle_in_radians = 2 * quarter        # 180 degrees
        elif y == 0:
            if x > 0:
                rotation_angle_in_radians = quarter            # 90 degrees
            else:
                rotation_angle_in_radians = 3 * quarter        # 270 degrees
        else:
            a = math.atan(abs(y) / abs(x))

            if x > 0:
                if y > 0:
                    rotation_angle_in_radians = quarter - a
                elif y < 0:
                    rotation_angle_in_radians = quarter + a
            elif x < 0:
                if y > 0:
                    rotation_angle_in_radians = quarter * 3 + a
                elif y < 0:
                    rotation_angle_in_radians = quarter * 3 - a

        return rotation_angle_in_radians * 180 / math.pi

class RightTriangleFromPointFinder(object):
    def __init__(self, point, relative_length_leg_a, relative_length_leg_b, fuzziness):
        # type: (Point, float, float, float) -> None

        self.__point = point
        self.__relative_side_lengths = {
            'leg_a': relative_length_leg_a,
            'leg_b': relative_length_leg_b,
            'hypotenuse_c': math.sqrt(
                relative_length_leg_a * relative_length_leg_a
                + relative_length_leg_b * relative_length_leg_b
            )
        }
        self.__fuzziness = fuzziness

        self.__side_candidates = {}  # type: Dict[string, List[LineSegment]]
        self.__sides = {}            # type: Dict[string, LineSegment]

    def line_segment_matches_relative_side_length(self, line_segment, side_name):
        # type: (LineSegment, string) -> bool
        if are_fuzzy_equal(
            value_1=line_segment.relative_length,
            value_2=self.__relative_side_lengths[side_name],
            fuzziness=self.__fuzziness
        ):
            print('Line segment matches relative side length: {} == {}'.format(
                line_segment.relative_length,
                self.__relative_side_lengths[side_name]
            ))
            return True
        return False

    def add_side_candidate(self, side_name, line_segment):
        # type: (string, LineSegment) -> None

        for side_candidate_list in self.__side_candidates.values():
            if line_segment in side_candidate_list:
                return

        if side_name not in self.__side_candidates:
            self.__side_candidates[side_name] = []
        self.__side_candidates[side_name].append(line_segment)

    def calculate_relative_line_segment_lengths(self, scale):
        # type: (float) -> None

        for line_segment in (
                    self.__point.line_segments_from_this_point
                    + self.__point.line_segments_that_connect_line_segments_from_this_point
        ):
            line_segment.calculate_relative_length(scale)

    def find_line_segments_that_match_a_relative_side_length(self):
        for line_segment in self.__point.line_segments_from_this_point:
            for side_name in self.__relative_side_lengths.keys():
                if self.line_segment_matches_relative_side_length(line_segment, side_name):
                    self.add_side_candidate(side_name, line_segment)

        if len(self.__side_candidates.values()) >= 2:
            return True    # Found at least two side candidates
        else:
            # print("Failed match_ratio_pattern matches: {}".format(self.__matches))
            return False

    def try_to_find_last_side(self):
        # type: () -> bool

        for side_x_name, side_x_candidates in self.__side_candidates.items():
            for side_y_name, side_y_candidates in self.__side_candidates.items():
                if side_x_name is not side_y_name:
                    if self.try_to_find_side_z(side_x_name, side_x_candidates, side_y_name, side_y_candidates):
                        return True

        # print("Failed try_to_add_indirect_link")
        return False

    def try_to_find_side_z(self, side_x_name, side_x_candidates, side_y_name, side_y_candidates):
        # type: (string, List[LineSegment], string, List[LineSegment]) -> bool

        for side_x_candidate in side_x_candidates:
            for side_y_candidate in side_y_candidates:
                if self.try_to_find_side_z_for_side_x_and_y_candidate_pair(
                    side_x_name=side_x_name,
                    side_x_candidate=side_x_candidate,
                    side_y_name=side_y_name,
                    side_y_candidate=side_y_candidate
                ):
                    return True   # side_z found

        return False   # no side_z found

    def get_side_name_that_is_not(self, side_x_name, side_y_name):
        # type: (string, string) -> string

        return next(
            side_name
            for side_name in self.__relative_side_lengths.keys()
            if side_name != side_x_name and side_name != side_y_name
        )

    def try_to_find_side_z_for_side_x_and_y_candidate_pair(
            self,
            side_x_name,
            side_x_candidate,
            side_y_name,
            side_y_candidate
    ):
        # type: (string, LineSegment, string, LineSegment) -> bool

        end_point_side_x_candidate = side_x_candidate.get_other_point(self.__point)
        end_point_side_y_candidate = side_y_candidate.get_other_point(self.__point)

        for side_z_candidate in self.__point.line_segments_that_connect_line_segments_from_this_point:
            if (
                side_z_candidate.starts_or_ends_in(end_point_side_x_candidate)
                and side_z_candidate.starts_or_ends_in(end_point_side_y_candidate)
            ):
                side_z_name = self.get_side_name_that_is_not(side_x_name, side_y_name)

                if self.line_segment_matches_relative_side_length(
                        line_segment=side_z_candidate, side_name=side_z_name
                ):
                    self.__sides[side_z_name] = side_z_candidate
                    self.__sides[side_x_name] = side_x_candidate
                    self.__sides[side_y_name] = side_y_candidate
                    return True

        return False   # no side_z found

    def try_to_find_triangle_sides(self):
        for line_segment in (
                    self.__point.line_segments_from_this_point
                    + self.__point.line_segments_that_connect_line_segments_from_this_point
        ):
            self.__side_candidates = {}
            self.__sides = {}
            self.calculate_relative_line_segment_lengths(line_segment.length)

            if self.find_line_segments_that_match_a_relative_side_length():
                if self.try_to_find_last_side():
                    return True

        # print("Failed find_led_links_matching_ratio_pattern")
        return False

    def find_right_triangle(self):
        if self.try_to_find_triangle_sides():
            return RightTriangle(self.__sides['leg_a'], self.__sides['leg_b'], self.__sides['hypotenuse_c'])
        else:
            return None


class RightTriangleFinder(object):
    def __init__(self, points, relative_length_leg_a, relative_length_leg_b, fuzziness):
        # type: (List[Point], float, float, float) -> None

        self.__points = points
        self.__relative_length_leg_a = relative_length_leg_a
        self.__relative_length_leg_b = relative_length_leg_b
        self.__fuzziness = fuzziness

        self.__points_that_are_already_in_a_triangle = []

    def find_all_right_triangles(self):
        # type: () -> List[RightTriangle]

        right_triangles = []

        for point in self.__points:
            if point not in self.__points_that_are_already_in_a_triangle:
                right_triangle = RightTriangleFromPointFinder(
                    point,
                    self.__relative_length_leg_a,
                    self.__relative_length_leg_b,
                    self.__fuzziness).find_right_triangle()

                if right_triangle is not None:
                    for point_in_triangle in right_triangle.get_angles():
                        self.__points_that_are_already_in_a_triangle.append(point_in_triangle)

                    right_triangles.append(right_triangle)

        return right_triangles


class LineSegmentGenerator(object):
    @staticmethod
    def create_line_segments_between_points(points, max_delta_x, max_delta_y):
        # type: (List[Point], float, float) -> List[LineSegment]

        line_segments = []
        finished_points = []
        for point_1 in points:
            for point_2 in points:
                if (
                    point_1 is not point_2
                    and point_2 not in finished_points
                    and abs(point_1.x - point_2.x) < max_delta_x
                    and abs(point_1.y - point_2.y) < max_delta_y
                ):
                    line_segments.append(LineSegment(point_1, point_2))

            finished_points.append(point_1)
            point_1.sort_line_segments_by_length()

        return line_segments


