# packing_list/views.py
import io

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from base.decorators import registration_accepted_required
from config.settings import THE_SITE_NAME

from .forms import ActivityForm, ItemForm
from .models import Activity, Item

# ---------- Activity Views ----------


@registration_accepted_required
def activity_list(request):
    activities = Activity.objects.filter(user=request.user)
    return render(
        request,
        "packing_list/activity_list.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Activities",
            "activities": activities,
        },
    )


@registration_accepted_required
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    items = activity.packing_items.all()  # uses related_name on Item.activity
    return render(
        request,
        "packing_list/activity_detail.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": activity.name,
            "activity": activity,
            "items": items,
        },
    )


@registration_accepted_required
def activity_create(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect("packing_list:activity_list")
    else:
        form = ActivityForm()
    return render(
        request,
        "packing_list/activity_form.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Create Activity",
            "form": form,
        },
    )


@registration_accepted_required
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("packing_list:activity_list")
    else:
        form = ActivityForm(instance=activity)
    return render(
        request,
        "packing_list/activity_form.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Update Activity",
            "form": form,
        },
    )


@registration_accepted_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == "POST":
        activity.delete()
        return redirect("packing_list:activity_list")
    return render(
        request,
        "packing_list/activity_confirm_delete.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": f"Delete {activity.name}",
            "activity": activity,
        },
    )


@registration_accepted_required
def activity_pdf(request, pk):
    # fetch only the user’s own activity
    activity = get_object_or_404(Activity, pk=pk, user=request.user)

    # build PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title: Activity name at 20pt
    p.setFont("Helvetica-Bold", 20)
    p.drawString(1 * inch, height - 1 * inch, activity.name)

    # Items: 20pt, with check-boxes
    p.setFont("Helvetica", 20)
    y = height - 1.5 * inch
    for item in activity.packing_items.all():
        # draw an empty square for checkbox
        p.rect(1 * inch, y - 0.2 * inch, 0.2 * inch, 0.2 * inch, stroke=1, fill=0)
        # item name
        p.drawString(1.3 * inch, y - 0.2 * inch, item.name)

        y -= 0.5 * inch
        # new page if we run out of room
        if y < 1 * inch:
            p.showPage()
            p.setFont("Helvetica", 20)
            y = height - 1 * inch

    p.save()
    buffer.seek(0)

    # return as attachment
    response = HttpResponse(buffer, content_type="application/pdf")
    activity_slug_name = slugify(activity.name)
    response["Content-Disposition"] = f'attachment; filename="{activity_slug_name}.pdf"'
    return response


# ---------- Item Views ----------


@registration_accepted_required
def item_list(request):
    items = Item.objects.filter(user=request.user).select_related("activity")
    return render(
        request,
        "packing_list/item_list.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Items",
            "items": items,
        },
    )


@registration_accepted_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    return render(
        request,
        "packing_list/item_detail.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": item.name,
            "item": item,
        },
    )


@registration_accepted_required
def item_create(request):
    activity_id = request.GET.get(
        "activity"
    )  # e.g. from clicking “Add Item” on an activity page

    if request.method == "POST":
        form = ItemForm(
            request.POST,
            user=request.user,
            activity=activity_id,
        )
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect("packing_list:item_list")
    else:
        form = ItemForm(
            user=request.user,
            activity=activity_id,
        )

    return render(
        request,
        "packing_list/item_form.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Create Item",
            "form": form,
        },
    )


@registration_accepted_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("packing_list:item_list")
    else:
        form = ItemForm(instance=item)
    return render(
        request,
        "packing_list/item_form.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": f"Update {item.name}",
            "form": form,
        },
    )


@registration_accepted_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("packing_list:item_list")
    return render(
        request,
        "packing_list/item_confirm_delete.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": f"Delete {item.name}",
            "item": item,
        },
    )
