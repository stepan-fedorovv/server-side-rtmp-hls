import factory
from factory import fuzzy

from apps.user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fuzzy.FuzzyText()
