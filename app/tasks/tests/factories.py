import factory

from django.utils import timezone

from ..models import Task
from user.tests.factories import UserFactory


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    user = factory.SubFactory(UserFactory)  
    title = factory.Faker('word')
    description = factory.Faker('text')
    is_completed = True

    
    
