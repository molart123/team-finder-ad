from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .forms import RegisterForm, UpdateForm
from .models import User

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            name="Test",
            surname="User",
            password="testpass123",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            name="Admin",
            surname="User",
            password="adminpass123",
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_generate_avatar(self):
        user = User.objects.create_user(
            email="avatar@example.com",
            name="Avatar",
            surname="Test",
            password="testpass123",
        )
        self.assertIsNotNone(user.avatar)
        self.assertTrue(user.avatar.name.startswith(f"avatars/avatar_{user.id}"))

    def test_user_str_method(self):
        user = User.objects.create_user(
            email="str@example.com",
            name="String",
            surname="Test",
            password="testpass123",
        )
        self.assertEqual(str(user), "String Test")


class UserFormsTest(TestCase):
    def test_valid_register_form(self):
        form_data = {
            "email": "new@example.com",
            "password": "testpass123",
            "name": "New",
            "surname": "User",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_register_form(self):
        form_data = {
            "password": "testpass123",
            "name": "New",
            "surname": "User",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_update_form(self):
        user = User.objects.create_user(
            email="update@example.com",
            name="Update",
            surname="Test",
            password="testpass123",
        )
        form_data = {
            "name": "Updated",
            "surname": "Name",
            "phone": "+79991234567",
            "about": "About me",
            "github_url": "https://github.com/username",
        }
        form = UpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_format(self):
        user = User.objects.create_user(
            email="phone@example.com",
            name="Phone",
            surname="Test",
            password="testpass123",
        )
        form_data = {
            "name": "Phone",
            "surname": "Test",
            "phone": "1234567890",  # Неверный формат
        }
        form = UpdateForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_invalid_github_url(self):
        user = User.objects.create_user(
            email="github@example.com",
            name="GitHub",
            surname="Test",
            password="testpass123",
        )
        form_data = {
            "name": "GitHub",
            "surname": "Test",
            "github_url": "https://gitlab.com/username",  # Не GitHub
        }
        form = UpdateForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn("github_url", form.errors)


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="view@example.com",
            name="View",
            surname="Test",
            password="testpass123",
        )

    def test_users_list_view(self):
        response = self.client.get(reverse("users:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/participants.html")
        self.assertIn("participants", response.context)

    def test_user_detail_view(self):
        response = self.client.get(
            reverse("users:profile", kwargs={"id": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user-details.html")
        self.assertEqual(response.context["user"], self.user)

    def test_register_view_get(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertIsInstance(response.context["form"], RegisterForm)

    def test_register_view_post_valid(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "email": "newuser@example.com",
                "password": "newpass123",
                "name": "New",
                "surname": "User",
            },
        )
        self.assertRedirects(response, reverse("projects:list"))
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_login_view_get(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post_valid(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "email": "view@example.com",
                "password": "testpass123",
            },
        )
        self.assertRedirects(response, reverse("projects:list"))

    def test_login_view_post_invalid(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "email": "view@example.com",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertTrue(response.context["form"].errors)

    def test_logout_view(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.get(reverse("users:logout"))
        self.assertRedirects(response, reverse("projects:list"))

    def test_profile_edit_view_get(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.get(reverse("users:edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/edit_profile.html")
        self.assertIsInstance(response.context["form"], UpdateForm)

    def test_profile_edit_view_post_valid(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.post(
            reverse("users:edit"),
            {
                "name": "UpdatedName",
                "surname": "UpdatedSurname",
                "phone": "+79991234567",
                "about": "Updated about",
            },
        )
        self.assertRedirects(
            response, reverse("users:profile", kwargs={"id": self.user.id})
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "UpdatedName")
        self.assertEqual(self.user.surname, "UpdatedSurname")

    def test_change_password_view_get(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.get(reverse("users:change_password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/change_password.html")

    def test_favorites_view(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.get(reverse("users:favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/favorite_projects.html")
        self.assertIn("projects", response.context)
