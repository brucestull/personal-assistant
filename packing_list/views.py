# packing_list/views.py
import io

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
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
    # 1. Read & clamp font size between 11 and 20
    try:
        font_size = int(request.GET.get("font_size", 12))
    except (TypeError, ValueError):
        font_size = 12
    font_size = max(11, min(20, font_size))

    # 2. Compute leading in POINTS (not inches)
    leading = font_size * 1.2  # this is in points

    # fetch only the user’s own activity
    activity = get_object_or_404(Activity, pk=pk, user=request.user)

    # build PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", font_size)
    p.drawString(1 * inch, height - 1 * inch, activity.name)

    # Switch back to regular font
    p.setFont("Helvetica", font_size)

    # get real font metrics
    face = pdfmetrics.getFont("Helvetica").face
    ascent = face.ascent * font_size / 1000.0
    descent = face.descent * font_size / 1000.0

    leading = font_size * 1.2
    box_size = 0.2 * inch
    bottom_margin = 1 * inch

    # start y as the *baseline* of the first line,
    # we want that baseline to sit 1.5" below the top edge, so we add half the box height # noqa E501
    y = height - 1.5 * inch + box_size / 2

    for item in activity.packing_items.all():
        # new page?
        if y - leading < bottom_margin:
            p.showPage()
            p.setFont("Helvetica", font_size)
            y = height - 1.5 * inch + box_size / 2

        # draw the text at the baseline y
        text = f"({item.quantity}) {item.name}"
        p.drawString(1.3 * inch, y, text)

        # compute the true text height and center the box around it
        text_height = ascent - descent
        box_y = y + descent + (text_height - box_size) / 2
        p.rect(1 * inch, box_y, box_size, box_size, stroke=1, fill=0)

        y -= leading

        # description, same idea (but no box)
        if item.description:
            p.drawString(1.6 * inch, y, item.description)
            y -= leading

    p.save()
    buffer.seek(0)

    # return as attachment with slugified name
    filename = f"{slugify(activity.name)}.pdf"
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
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
    # grab the activity ID (or 404 early if you prefer)
    activity_id = request.GET.get("activity")
    activity = get_object_or_404(Activity, pk=activity_id, user=request.user)

    # build the form: on GET, request.POST is empty so data=None
    form = ItemForm(
        request.POST or None,  # always supply data or None
        user=request.user,  # custom kw
        activity=activity,  # pass the instance (not just the ID)
    )

    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return redirect("packing_list:item_list")

    return render(
        request,
        "packing_list/item_form.html",
        {
            "the_site_name": settings.THE_SITE_NAME,
            "page_title": "Create Item",
            "form": form,
        },
    )


@registration_accepted_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)

    if request.method == "POST":
        form = ItemForm(
            request.POST,
            instance=item,
            user=request.user,  # scope queryset to this user
        )
        if form.is_valid():
            form.save()
            return redirect("packing_list:item_list")
    else:
        form = ItemForm(
            instance=item,
            user=request.user,  # scope queryset + pick up .instance.activity
        )

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
