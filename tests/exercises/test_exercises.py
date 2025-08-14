from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.errors_schema import InternalErrorResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, assert_update_exercise_response, assert_exercise_not_found_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture
    ):

        # Формируем данные для создания упражнения, используя фикстуру курса
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        
        # Отправляем POST-запрос на создание упражнения
        response = exercises_client.create_exercise_api(request)
        
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)
        
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)
        
        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)
        
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        # Отправляем GET-запрос на получение задания по ID
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)
        
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)
        
        # Проверяем, что данные в ответе соответствуют ожидаемому заданию
        assert_get_exercise_response(response_data, function_exercise.response.exercise)
        
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        # Формируем данные для обновления задания
        request = UpdateExerciseRequestSchema()
        
        # Отправляем PATCH-запрос на обновление задания
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)
        
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)
        
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)
        
        # Проверяем, что данные в ответе соответствуют запросу на обновление
        assert_update_exercise_response(request, response_data)
        
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        # Отправляем DELETE-запрос на удаление задания
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        
        # Проверяем, что код ответа на удаление 200 OK
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        
        # Отправляем GET-запрос для проверки, что задание было удалено
        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        
        # Проверяем, что код ответа на получение 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        
        # Десериализуем JSON-ответ с ошибкой в Pydantic-модель
        error_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        
        # Проверяем, что тело ответа содержит ошибку "Exercise not found"
        assert_exercise_not_found_response(error_response_data)
        
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(get_response.json(), error_response_data.model_json_schema())
