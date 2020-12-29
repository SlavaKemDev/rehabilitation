from Geometry2D import *


class Exercise:
    PUFFING_UP = 1
    SMILE = 2
    TONGUE_STRETCHING = 3
    EYES = 4

    def __init__(self, start_model, exercise_name):
        self.start_model = start_model
        self.model = start_model  # TODO: создать нормальный конструктор модели
        self.exercise = exercise_name

    def compare_points(self, point_start, point_new, point_user):
        point_start = Point(point_start[0], point_start[1])  # точка из первой модели лица
        point_new = Point(point_new[0], point_new[1])  # точка из предполагаемой на данном упражнении модели лица
        point_user = Point(point_user[0], point_user[1])  # точка, которая] в итоге получилась у пользователя

        start_new_segment = Segment(point_start, point_new)
        start_user_segment = Segment(point_start, point_user)
        new_user_segment = Segment(point_new, point_user)

        result = (start_user_segment.length - new_user_segment.length) / start_new_segment.length
        return result

    def get_result(self, user_model):
        if len(user_model) != len(self.model):
            return 0
        point_results = []
        for i in range(len(user_model)):
            result = self.compare_points(self.start_model[i], self.model[i], user_model[i])
            point_results.append(result)

        average_value = sum(point_results) / len(point_results)

        return average_value >= 0.85
