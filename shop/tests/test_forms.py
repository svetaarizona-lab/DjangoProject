import pytest

from shop.forms import CustomUserCreationForm

from shop.models import User


@pytest.mark.django_db
def test_valid_user_creation_form():
    form = CustomUserCreationForm(
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_passwords_do_not_match():
    form = CustomUserCreationForm(
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPassword123",
            "password2": "WrongPassword123",
        }
    )

    assert not form.is_valid()
    assert "password2" in form.errors


@pytest.mark.django_db
def test_username_is_required():
    form = CustomUserCreationForm(
        data={
            "username": "",
            "email": "test@example.com",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_form_save_creates_user():
    form = CustomUserCreationForm(
        data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
    )

    assert form.is_valid()

    user = form.save()

    assert isinstance(user, User)
    assert user.username == "newuser"
    assert user.email == "new@example.com"


def test_form_labels():
    form = CustomUserCreationForm()

    assert form.fields["username"].label is not None
    assert form.fields["email"].label is not None
    assert form.fields["password1"].label is not None
    assert form.fields["password2"].label is not None
