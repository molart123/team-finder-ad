import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .forms import ProjectForm
from .models import Project

User = get_user_model()


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            name="Owner",
            surname="Test",
            password="testpass123",
        )

    def test_create_project(self):
        project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            owner=self.user,
            github_url="https://github.com/test/repo",
            status="open",
        )
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.owner, self.user)
        self.assertEqual(project.status, "open")
        self.assertIsNotNone(project.created_at)

    def test_project_str_method(self):
        project = Project.objects.create(
            name="Str Project",
            owner=self.user,
        )
        self.assertEqual(str(project), "Str Project")

    def test_project_participants(self):
        project = Project.objects.create(
            name="Team Project",
            owner=self.user,
        )
        user2 = User.objects.create_user(
            email="participant@example.com",
            name="Participant",
            surname="Test",
            password="testpass123",
        )
        project.participants.add(user2)
        self.assertIn(user2, project.participants.all())
        self.assertIn(project, user2.participated_projects.all())


class ProjectFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="form@example.com",
            name="Form",
            surname="Test",
            password="testpass123",
        )

    def test_valid_project_form(self):
        form_data = {
            "name": "Test Project",
            "description": "Test Description",
            "github_url": "https://github.com/test/repo",
            "status": "open",
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_github_url(self):
        form_data = {
            "name": "Test Project",
            "github_url": "https://gitlab.com/test/repo",
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("github_url", form.errors)


class ProjectViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="view@example.com",
            name="View",
            surname="Test",
            password="testpass123",
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            owner=self.user,
            status="open",
        )

    def test_project_list_view(self):
        response = self.client.get(reverse("projects:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_list.html")
        self.assertIn("projects", response.context)

    def test_project_detail_view(self):
        response = self.client.get(
            reverse("projects:detail", kwargs={"id": self.project.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project-details.html")
        self.assertEqual(response.context["project"], self.project)

    def test_create_project_view_get(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.get(reverse("projects:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/create-project.html")
        self.assertFalse(response.context["is_edit"])

    def test_create_project_view_post_valid(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.post(
            reverse("projects:create"),
            {
                "name": "New Project",
                "description": "New Description",
                "github_url": "https://github.com/new/repo",
                "status": "open",
            },
        )
        new_project = Project.objects.get(name="New Project")
        self.assertRedirects(
            response, reverse("projects:detail", kwargs={"id": new_project.id})
        )
        self.assertEqual(new_project.owner, self.user)
        self.assertIn(self.user, new_project.participants.all())

    def test_edit_project_view_get(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.get(
            reverse("projects:edit", kwargs={"id": self.project.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/create-project.html")
        self.assertTrue(response.context["is_edit"])
        self.assertEqual(response.context["form"].instance, self.project)

    def test_edit_project_view_post_valid(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.post(
            reverse("projects:edit", kwargs={"id": self.project.id}),
            {
                "name": "Updated Project",
                "description": "Updated Description",
                "github_url": "https://github.com/updated/repo",
                "status": "closed",
            },
        )
        self.assertRedirects(
            response, reverse("projects:detail", kwargs={"id": self.project.id})
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")
        self.assertEqual(self.project.status, "closed")

    def test_complete_project_view(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.post(
            reverse("projects:complete", kwargs={"id": self.project.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": "ok", "project_status": "closed"},
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "closed")

    def test_toggle_participate_view(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.post(
            reverse("projects:toggle_participate", kwargs={"id": self.project.id})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["status"], "ok")
        self.assertTrue(data["is_participating"])
        self.assertIn(self.user, self.project.participants.all())

        # Выход
        response = self.client.post(
            reverse("projects:toggle_participate", kwargs={"id": self.project.id})
        )
        data = json.loads(response.content)
        self.assertEqual(data["status"], "ok")
        self.assertFalse(data["is_participating"])
        self.assertNotIn(self.user, self.project.participants.all())

    def test_toggle_favorite_view(self):
        self.client.login(email="view@example.com", password="testpass123")
        response = self.client.post(
            reverse("projects:toggle_favorite", kwargs={"id": self.project.id})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["status"], "ok")
        self.assertTrue(data["favorited"])
        self.assertIn(self.project, self.user.favorites_projects.all())

        # Удаляем из избранного
        response = self.client.post(
            reverse("projects:toggle_favorite", kwargs={"id": self.project.id})
        )
        data = json.loads(response.content)
        self.assertEqual(data["status"], "ok")
        self.assertFalse(data["favorited"])
        self.assertNotIn(self.project, self.user.favorites_projects.all())
