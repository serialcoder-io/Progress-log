import pytest
from django.db import IntegrityError
from users.models import User

@pytest.mark.django_db
def test_create_user(user_factory):
    user = user_factory(email='user@test.com', password='password1234', display_name='test_user')
    assert user.display_name == 'test_user'
    assert user.email == 'user@test.com'
    assert user.check_password("password1234")
    assert not user.is_staff
    assert not user.is_superuser
    assert User.objects.count() == 1


def test_create_superuser(super_user):
    assert super_user.is_staff
    assert super_user.is_superuser


@pytest.mark.django_db
def test_default_display_name(user_factory):
    user = user_factory()
    assert user.display_name == user.email.split('@')[0]


@pytest.mark.django_db
def test_custom_display_name(user_factory):
    user = user_factory(display_name='custom_name')
    assert user.display_name == "custom_name"


@pytest.mark.django_db
def test_email_unique():
    User.objects.create_user(
        email="user@test.com",
        password="password1234"
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="user@test.com",
            password="test_user2"
        )