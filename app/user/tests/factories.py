import factory
from django.contrib.auth.models import User
from faker import Faker

from user.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: 'person{}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'passer@@@111')
    firstname = fake.name()
    lastname = fake.name()


class SuperAdminUserFactory(UserFactory):
    """"Factory for a super admin user"""
    is_superuser = 'True'
