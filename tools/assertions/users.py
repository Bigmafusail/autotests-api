from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema
from tools.assertions.base import assert_equal


def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")


def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Проверяет корректность данных пользователя, сравнивая фактические и ожидаемые значения.

    :param actual: Фактические данные пользователя.
    :param expected: Ожидаемые данные пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")


def assert_get_user_response(get_user_response: UserSchema, create_user_response: CreateUserResponseSchema):
    """
    Проверяет, что данные пользователя при запросе совпадают с данными при создании.

    :param get_user_response: Ответ API при запросе пользователя (UserSchema).
    :param create_user_response: Ответ API при создании пользователя (CreateUserResponseSchema).
    :raises AssertionError: Если данные не совпадают.
    """
    # Сравниваем данные пользователя из ответа на запрос с данными из ответа на создание
    assert_user(get_user_response, create_user_response.user)
