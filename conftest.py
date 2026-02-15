import pytest
from users.models import User
from pytest_factoryboy import register
from users.tests.factories import UserFactory

register(UserFactory)

@pytest.fixture()
def super_user(db):
    return User.objects.create_superuser(
        email="superuser@test.com",
        password="password1234",
        display_name='admin_user'
    )