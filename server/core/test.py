import datetime

import factory

from . import models as core_models


class UserF(factory.Factory):
    class Meta:
        model = core_models.User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(f"{first_name}.{last_name}@example.com".lower())
    date_joined = factory.LazyFunction(datetime.now)
    admin = True
