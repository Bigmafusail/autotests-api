from clients.exercises.exercises_schema import ExerciseSchema, CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.errors_schema import InternalErrorResponseSchema
from tools.assertions.base import assert_equal
from tools.assertions.errors import assert_internal_error_response


def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    """
    Проверяет, что ответ на создание задания соответствует запросу.

    :param request: Исходный запрос на создание задания.
    :param response: Ответ API с данными задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.courseId, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные задания
    :param expected: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.courseId, expected.courseId, "courseId")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


def assert_get_exercise_response(response: GetExerciseResponseSchema, expected_exercise: ExerciseSchema):
    """
    Проверяет, что ответ получения данных задания соответствует ожидаемому заданию.

    :param response: Ответ API с данными задания.
    :param expected_exercise: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_exercise(response.exercise, expected_exercise)


def assert_update_exercise_response(request: UpdateExerciseRequestSchema, response: UpdateExerciseResponseSchema):
    """
    Проверяет, что ответ на обновление задания соответствует запросу.

    :param request: Исходный запрос на обновление задания.
    :param response: Ответ API с данными обновленного задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    if request.title is not None:
        assert_equal(response.exercise.title, request.title, "title")
    if request.max_score is not None:
        assert_equal(response.exercise.max_score, request.max_score, "max_score")
    if request.min_score is not None:
        assert_equal(response.exercise.min_score, request.min_score, "min_score")
    if request.order_index is not None:
        assert_equal(response.exercise.order_index, request.order_index, "order_index")
    if request.description is not None:
        assert_equal(response.exercise.description, request.description, "description")
    if request.estimated_time is not None:
        assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise_not_found_response(response: InternalErrorResponseSchema):
    """
    Проверяет, что ответ содержит ошибку "Exercise not found".

    :param response: Ответ API с ошибкой.
    :raises AssertionError: Если сообщение об ошибке не соответствует ожидаемому.
    """
    expected_error = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(response, expected_error)
