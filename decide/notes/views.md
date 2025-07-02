# `views.py`

## `views.py` Contents

```python
# decide/views.py
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, IntegerField, Value, When
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import DecisionForm
from .models import Decision, DecisionResponse, Prompt
from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin


@registration_accepted_required
def create_decision(request):
    if request.method == "POST":
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.user = request.user
            decision.save()
            return redirect("decide:decision_flow", decision_id=decision.id)
    else:
        form = DecisionForm()
    return render(request, "decide/decision_create.html", {"form": form})


@registration_accepted_required
def decision_flow(request, decision_id):
    decision = get_object_or_404(Decision, id=decision_id, user=request.user)
    first_prompt = Prompt.objects.first()
    total = Prompt.objects.count()
    return render(
        request,
        "decide/decision_flow.html",
        {"decision": decision, "prompt": first_prompt, "total_prompts": total},
    )


@registration_accepted_required
@require_POST
def decision_flow_json(request, decision_id):
    """
    AJAX endpoint: Accepts JSON {prompt_id, answer} and returns next prompt or final quadrant. # noqa: E501
    """
    decision = get_object_or_404(Decision, id=decision_id, user=request.user)
    try:
        payload = json.loads(request.body)
        prompt_id = payload["prompt_id"]
        answer = payload["answer"]
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid JSON payload")

    prompt = get_object_or_404(Prompt, id=prompt_id)
    DecisionResponse.objects.create(decision=decision, prompt=prompt, answer=answer)

    # Fetch next prompt
    answered_ids = decision.responses.values_list("prompt_id", flat=True)
    remaining = Prompt.objects.exclude(id__in=answered_ids)
    if remaining.exists():
        nxt = remaining.first()
        return JsonResponse({"prompt_id": nxt.id, "text": nxt.text})

    # Compute quadrant
    resp = {r.prompt.slug: r.answer for r in decision.responses.all()}
    urgent = resp.get("is_urgent")
    important = resp.get("is_important")
    if urgent and important:
        decision.quadrant = "Q1"
    elif not urgent and important:
        decision.quadrant = "Q2"
    elif urgent and not important:
        decision.quadrant = "Q3"
    else:
        decision.quadrant = "Q4"
    decision.save()

    return JsonResponse({"quadrant": decision.get_quadrant_display()})


@registration_accepted_required
def decision_result(request, decision_id):
    decision = get_object_or_404(Decision, id=decision_id, user=request.user)
    return render(request, "decide/decision_result.html", {"decision": decision})


class DecisionListView(RegistrationAcceptedMixin, LoginRequiredMixin, ListView):
    model = Decision
    template_name = "decide/decision_list.html"
    context_object_name = "decisions"
    paginate_by = 20

    def get_sort(self):
        # ?sort=quadrant or ?sort=date
        return self.request.GET.get("sort", "quadrant")

    def get_queryset(self):
        qs = Decision.objects.filter(user=self.request.user)
        sort = self.get_sort()

        if sort == "quadrant":
            # Annotate a numeric order for Q1→Q4, default last
            qs = qs.annotate(
                quadrant_order=Case(
                    When(quadrant="Q1", then=Value(1)),
                    When(quadrant="Q2", then=Value(2)),
                    When(quadrant="Q3", then=Value(3)),
                    When(quadrant="Q4", then=Value(4)),
                    default=Value(5),
                    output_field=IntegerField(),
                )
            ).order_by("quadrant_order", "-created_at")
        else:
            # Date created, newest first
            qs = qs.order_by("-created_at")

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_sort"] = self.get_sort()
        return ctx


class ResponseListView(RegistrationAcceptedMixin, LoginRequiredMixin, ListView):
    model = DecisionResponse
    template_name = "decide/response_list.html"
    context_object_name = "responses"
    paginate_by = 20

    def get_queryset(self):
        return (
            DecisionResponse.objects.filter(decision__user=self.request.user)
            .select_related("decision", "prompt")
            .order_by("-answered_at")
        )
```

## `views.py` Explanation

Below is each view and mixin broken down line-by-line with inline comments explaining exactly what’s happening. I’ve grouped imports separately, then each function and class.

---

```python
# decide/views.py

import json
# — Standard library module for parsing JSON payloads.

from django.contrib.auth.mixins import LoginRequiredMixin
# — Mixin to require login on class-based views.

from django.db.models import Case, IntegerField, Value, When
# — Used to build conditional annotations in QuerySets.

from django.http import HttpResponseBadRequest, JsonResponse
# — HttpResponseBadRequest returns a 400 error; JsonResponse serializes Python dicts to JSON.

from django.shortcuts import get_object_or_404, redirect, render
# — get_object_or_404: fetch or 404; redirect: shortcut to HttpResponseRedirect; render: render a template.

from django.views.decorators.http import require_POST
# — Decorator to ensure a view only accepts POST requests.

from django.views.generic import ListView
# — Generic class-based view for displaying lists of objects.

from .forms import DecisionForm
# — Your form for creating a Decision.

from .models import Decision, DecisionResponse, Prompt
# — The three core models: Decision, Prompt, DecisionResponse.

from base.decorators import registration_accepted_required
# — Custom decorator ensuring the user has completed registration.

from base.mixins import RegistrationAcceptedMixin
# — Mixin counterpart to that decorator for class-based views.
```

---

### `create_decision`

```python
@registration_accepted_required
def create_decision(request):
    if request.method == "POST":
        form = DecisionForm(request.POST)
        # ← Instantiate the form with POST data.
        if form.is_valid():
            decision = form.save(commit=False)
            # ← Create a Decision instance but don’t write to DB yet.
            decision.user = request.user
            # ← Associate the new Decision with the logged-in user.
            decision.save()
            # ← Now save to the database.
            return redirect("decide:decision_flow", decision_id=decision.id)
            # ← Send the user into the flow view for this new Decision.
    else:
        form = DecisionForm()
        # ← GET request: show an empty form.
    return render(request, "decide/decision_create.html", {"form": form})
    # ← Render the “new decision” template with the form in context.
```

1. **@registration\_accepted\_required**:
   Ensures the user has finished any extra registration steps before using the view.
2. **if request.method == "POST"**:
   Distinguishes form submission (POST) from initial page load (GET).
3. **DecisionForm(request.POST)**:
   Binds the incoming data to your form.
4. **form.is\_valid()**:
   Runs validation (required fields, max lengths, etc.).
5. **form.save(commit=False)**:
   Creates but doesn’t persist, so you can attach the `user`.
6. **redirect(...)**:
   Issues an HTTP redirect to the AJAX-driven flow for answering prompts.
7. **render(...)**:
   On GET (or invalid POST), displays the HTML form template.

---

### `decision_flow`

```python
@registration_accepted_required
def decision_flow(request, decision_id):
    decision = get_object_or_404(Decision, id=decision_id, user=request.user)
    # ← Fetch the Decision or 404 if it doesn't exist or doesn’t belong to this user.

    first_prompt = Prompt.objects.first()
    # ← Grab the very first Prompt in order (e.g. “Is it urgent?”).

    total = Prompt.objects.count()
    # ← Count how many prompts exist (used for the progress bar).

    return render(
        request,
        "decide/decision_flow.html",
        {
            "decision": decision,
            "prompt": first_prompt,
            "total_prompts": total,
        },
    )
    # ← Render the AJAX/JS‐driven wizard template, passing initial prompt and metadata.
```

1. **get\_object\_or\_404(...)**:
   Guards against someone manually changing the URL to another user’s decision.
2. **Prompt.objects.first() / .count()**:
   Sets you up to display prompt #1 and know how many total steps there are.

---

### `decision_flow_json`

```python
@registration_accepted_required
@require_POST
def decision_flow_json(request, decision_id):
    """
    AJAX endpoint: Accepts JSON {prompt_id, answer} and returns next prompt or final quadrant.
    """
    decision = get_object_or_404(Decision, id=decision_id, user=request.user)
    # ← Ensure user owns this Decision.

    try:
        payload = json.loads(request.body)
        # ← Parse raw JSON from the POST body.
        prompt_id = payload["prompt_id"]
        answer = payload["answer"]
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid JSON payload")
        # ← If JSON is malformed or missing keys, return HTTP 400.

    prompt = get_object_or_404(Prompt, id=prompt_id)
    # ← Validate the prompt ID.

    DecisionResponse.objects.create(decision=decision, prompt=prompt, answer=answer)
    # ← Persist the user's yes/no answer.

    # Fetch next prompt
    answered_ids = decision.responses.values_list("prompt_id", flat=True)
    # ← Gather prompt IDs the user has already answered.
    remaining = Prompt.objects.exclude(id__in=answered_ids)
    # ← Any prompts not answered yet.
    if remaining.exists():
        nxt = remaining.first()
        return JsonResponse({"prompt_id": nxt.id, "text": nxt.text})
        # ← Still more steps: return JSON for the next prompt.

    # No prompts left → calculate quadrant:
    resp = {r.prompt.slug: r.answer for r in decision.responses.all()}
    # ← Build a dict: {"is_urgent": True/False, "is_important": True/False}

    urgent = resp.get("is_urgent")
    important = resp.get("is_important")

    if urgent and important:
        decision.quadrant = "Q1"
    elif not urgent and important:
        decision.quadrant = "Q2"
    elif urgent and not important:
        decision.quadrant = "Q3"
    else:
        decision.quadrant = "Q4"
    decision.save()
    # ← Persist the computed quadrant back on the Decision.

    return JsonResponse({"quadrant": decision.get_quadrant_display()})
    # ← Return the human-readable quadrant label for the front end to render.
```

* **@require\_POST**: enforces that only POST requests reach this view.
* **json.loads(request.body)**: you’re bypassing Django’s form system in favor of raw JSON.
* **Case/When imports**: not used here, but available for advanced QuerySet annotations if you wanted to compute quadrant ordering in the database.

---

### `decision_result`

```python
@registration_accepted_required
def decision_result(request, decision_id):
    decision = get_object_or_404(Decision, id=decision_id, user=request.user)
    # ← Ensure the user owns it.

    return render(request, "decide/decision_result.html", {"decision": decision})
    # ← Show the “You got Q2”--style summary page.
```

Simple detail page for a completed decision.

---

### `DecisionListView`

```python
class DecisionListView(RegistrationAcceptedMixin, LoginRequiredMixin, ListView):
    model = Decision
    template_name = "decide/decision_list.html"
    context_object_name = "decisions"
    paginate_by = 20
```

* **RegistrationAcceptedMixin** + **LoginRequiredMixin**:
  Require both registration acceptance and login.
* **model** / **template\_name** / **context\_object\_name** / **paginate\_by**:
  Standard ListView config.

```python
    def get_sort(self):
        # ?sort=quadrant or ?sort=date
        return self.request.GET.get("sort", "quadrant")
```

* Reads a `sort` query parameter, defaulting to `"quadrant"`.

```python
    def get_queryset(self):
        qs = Decision.objects.filter(user=self.request.user)
        sort = self.get_sort()
```

* Starts with all Decisions by this user.

```python
        if sort == "quadrant":
            qs = qs.annotate(
                quadrant_order=Case(
                    When(quadrant="Q1", then=Value(1)),
                    When(quadrant="Q2", then=Value(2)),
                    When(quadrant="Q3", then=Value(3)),
                    When(quadrant="Q4", then=Value(4)),
                    default=Value(5),
                    output_field=IntegerField(),
                )
            ).order_by("quadrant_order", "-created_at")
```

* **annotate(...)**: adds a numeric `quadrant_order` so Q1=1, Q2=2, etc., defaulting to 5 if unset.
* **order\_by(...)**: sorts first by that computed order, then newest first.

```python
        else:
            qs = qs.order_by("-created_at")
```

* If `?sort=date`, just order by creation timestamp descending.

```python
        return qs
```

* Return the final QuerySet back to ListView internals.

```python
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_sort"] = self.get_sort()
        return ctx
```

* Injects `current_sort` into template context so you can highlight the active sort link.

---

### `ResponseListView`

```python
class ResponseListView(RegistrationAcceptedMixin, LoginRequiredMixin, ListView):
    model = DecisionResponse
    template_name = "decide/response_list.html"
    context_object_name = "responses"
    paginate_by = 20

    def get_queryset(self):
        return (
            DecisionResponse.objects
            .filter(decision__user=self.request.user)
            .select_related("decision", "prompt")
            .order_by("-answered_at")
        )
```

* Shows every prompt response of the logged-in user, most recent first.
* **select\_related("decision", "prompt")** pre-fetches related Decision and Prompt in the same SQL query.

---

With this annotation in hand, you can see exactly where you might hook in a redirect after creating each `DecisionResponse` (for example, in `decision_flow_json` you could alter the final `JsonResponse` to include a URL for redirecting on the client). Let me know if you’d like pointers on that next!
