from http import HTTPStatus

import pytest

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "example.com"])
def test_create_user(domain: str, public_users_client: PublicUsersClient):
    # Генерируем email с указанным доменом
    request = CreateUserRequestSchema(email=fake.email(domain=domain))
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(private_users_client: PrivateUsersClient, function_user: UserFixture):
    # Выполняем запрос на получение данных текущего пользователя
    response = private_users_client.get_user_me_api()
    response_data = GetUserResponseSchema.model_validate_json(response.text)

    # Проверяем статус код ответа
    assert_status_code(response.status_code, HTTPStatus.OK)

    # Сравниваем данные полученного пользователя с данными созданного пользователя
    assert_get_user_response(response_data.user, function_user.response)

    # Валидируем JSON-схему ответа
    validate_json_schema(response.json(), response_data.model_json_schema())