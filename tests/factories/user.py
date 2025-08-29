from factory.declarations import LazyAttribute
from factory.helpers import post_generation

from db.models import User
from tests.factories.base import AsyncSQLAlchemyModelFactory, fake


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = User

    first_name = LazyAttribute(lambda obj: fake.first_name())
    last_name = LazyAttribute(lambda obj: fake.last_name())
    email = LazyAttribute(lambda obj: fake.email())
    hashed_password = LazyAttribute(lambda obj: fake.password())
    is_active = True

    @post_generation
    def set_hashed_password(self, create, extracted, **kwargs):
        if extracted:
            self.hashed_password = f"hashed_{extracted}"
