from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

from decide import admin as decide_admin
from decide.forms import DecisionForm, DecisionResponseForm
from decide.models import Decision, DecisionResponse, Prompt

User = get_user_model()


class DecideModelFormAdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="decide-user", password="pw", registration_accepted=True
        )

    def test_models_and_forms(self):
        decision = Decision.objects.create(user=self.user, title="Title")
        prompt = Prompt.objects.create(slug="is_urgent", order=1, text="Urgent?")
        response = DecisionResponse.objects.create(
            decision=decision, prompt=prompt, answer=True
        )

        self.assertEqual(str(decision), "Title")
        self.assertEqual(str(prompt), "1. Urgent?")
        self.assertEqual(str(response), "Title \u2192 is_urgent = True")

        form = DecisionForm(data={"title": "T", "description": "D"})
        self.assertTrue(form.is_valid())
        response_form = DecisionResponseForm(data={"answer": "True"})
        self.assertTrue(response_form.is_valid())
        self.assertIs(response_form.cleaned_data["answer"], True)

    def test_admin_registration_and_configuration(self):
        self.assertIn(Decision, site._registry)
        self.assertIn(Prompt, site._registry)
        self.assertIn(DecisionResponse, site._registry)

        decision_admin = site._registry[Decision]
        prompt_admin = site._registry[Prompt]
        response_admin = site._registry[DecisionResponse]

        self.assertEqual(
            decision_admin.list_display, ("title", "user", "quadrant", "created_at")
        )
        self.assertEqual(prompt_admin.list_display, ("order", "slug", "text"))
        self.assertEqual(
            response_admin.list_display, ("decision", "prompt", "answer", "answered_at")
        )
        self.assertIn(decide_admin.DecisionResponseInline, decision_admin.inlines)


class DecideViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.accepted_user = User.objects.create_user(
            username="accepted", password="pw", registration_accepted=True
        )
        self.unaccepted_user = User.objects.create_user(
            username="unaccepted", password="pw", registration_accepted=False
        )

        self.p1 = Prompt.objects.create(slug="is_urgent", order=1, text="Urgent?")
        self.p2 = Prompt.objects.create(slug="is_important", order=2, text="Important?")
        self.client.login(username="accepted", password="pw")

    def test_create_decision_requires_accepted_registration(self):
        self.client.logout()
        response = self.client.get(reverse("decide:create_decision"))
        self.assertEqual(response.status_code, 403)

        self.client.login(username="unaccepted", password="pw")
        response = self.client.get(reverse("decide:create_decision"))
        self.assertEqual(response.status_code, 403)

    def test_create_and_flow_and_result_happy_path(self):
        create_url = reverse("decide:create_decision")
        response = self.client.post(
            create_url,
            {"title": "New Decision", "description": "Details"},
        )
        decision = Decision.objects.get(title="New Decision")
        self.assertEqual(decision.user, self.accepted_user)
        self.assertRedirects(
            response,
            reverse("decide:decision_flow", kwargs={"decision_id": decision.id}),
        )

        flow_url = reverse("decide:decision_flow", kwargs={"decision_id": decision.id})
        flow_response = self.client.get(flow_url)
        self.assertEqual(flow_response.status_code, 200)
        self.assertEqual(flow_response.context["prompt"], self.p1)
        self.assertEqual(flow_response.context["total_prompts"], 2)

        json_url = reverse(
            "decide:decision_flow_json", kwargs={"decision_id": decision.id}
        )
        invalid = self.client.post(
            json_url,
            data="{}",
            content_type="application/json",
        )
        self.assertEqual(invalid.status_code, 400)

        next_prompt = self.client.post(
            json_url,
            data=f'{{"prompt_id": {self.p1.id}, "answer": true}}',
            content_type="application/json",
        )
        self.assertEqual(next_prompt.status_code, 200)
        self.assertEqual(next_prompt.json()["prompt_id"], self.p2.id)

        final = self.client.post(
            json_url,
            data=f'{{"prompt_id": {self.p2.id}, "answer": false}}',
            content_type="application/json",
        )
        self.assertEqual(final.status_code, 200)
        payload = final.json()
        self.assertEqual(payload["quadrant"], "Urgent & Not Important")
        decision.refresh_from_db()
        self.assertEqual(decision.quadrant, "Q3")

        result_url = reverse(
            "decide:decision_result", kwargs={"decision_id": decision.id}
        )
        result = self.client.get(result_url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.context["decision"], decision)

    def test_result_404_for_other_user(self):
        other_user = User.objects.create_user(
            username="other", password="pw", registration_accepted=True
        )
        decision = Decision.objects.create(user=other_user, title="Other")
        response = self.client.get(
            reverse("decide:decision_result", kwargs={"decision_id": decision.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_decision_and_response_list_views(self):
        my_q4 = Decision.objects.create(
            user=self.accepted_user, title="Mine", quadrant="Q4"
        )
        my_q1 = Decision.objects.create(
            user=self.accepted_user, title="Mine 2", quadrant="Q1"
        )
        other_user = User.objects.create_user(
            username="other2", password="pw", registration_accepted=True
        )
        Decision.objects.create(user=other_user, title="Other", quadrant="Q2")

        response = self.client.get(reverse("decide:decision_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["current_sort"], "quadrant")
        self.assertEqual(
            [d.id for d in response.context["decisions"][:2]],
            [my_q1.id, my_q4.id],
        )

        by_date = self.client.get(reverse("decide:decision_list") + "?sort=date")
        self.assertEqual(by_date.status_code, 200)
        self.assertEqual(by_date.context["current_sort"], "date")

        DecisionResponse.objects.create(decision=my_q1, prompt=self.p1, answer=True)
        DecisionResponse.objects.create(decision=my_q4, prompt=self.p2, answer=False)
        response_list = self.client.get(reverse("decide:response_list"))
        self.assertEqual(response_list.status_code, 200)
        for resp in response_list.context["responses"]:
            self.assertEqual(resp.decision.user, self.accepted_user)

    def test_registration_accepted_mixin_unauthenticated_redirects(self):
        self.client.logout()
        response = self.client.get(reverse("decide:decision_list"))
        self.assertEqual(response.status_code, 302)


class DirectMixinDispatchCoverageTest(TestCase):
    def test_registration_mixin_denies_unaccepted_user(self):
        from decide.views import DecisionListView

        user = User.objects.create_user(
            username="mix", password="pw", registration_accepted=False
        )
        request = RequestFactory().get("/decisions/")
        request.user = user

        with self.assertRaises(PermissionDenied):
            DecisionListView.as_view()(request)

    def test_registration_mixin_allows_accepted_user(self):
        from decide.views import DecisionListView

        user = User.objects.create_user(
            username="mix-yes", password="pw", registration_accepted=True
        )
        request = RequestFactory().get("/decisions/")
        request.user = user

        response = DecisionListView.as_view()(request)
        self.assertIsInstance(response, HttpResponse)
