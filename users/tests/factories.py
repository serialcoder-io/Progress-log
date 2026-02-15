import factory
from faker import Faker
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker('en_GB')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = fake.unique.email()
    password = factory.PostGenerationMethodCall('set_password', "Password123")
    display_name = factory.LazyAttribute(lambda a: a.email.split("@")[0])
    is_staff = False
    is_superuser = False
    is_active = True
