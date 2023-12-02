import pytest

# to avoid error: "RuntimeError: Database access not allowed, use the "django_db" mark, or the "db" or "transactional_db" fixtures to...
pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestNewUserModel():
    def test_string_method(self, new_user_factory):
        #Arrange
        #Act
        newuser = new_user_factory()
        #Assert
        assert newuser.__str__() == newuser.email
