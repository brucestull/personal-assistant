# packing_list/views.py
import io

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
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
            return redirect("packing_list:activity_detail", pk=activity.pk)

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
    # 1. clamp font size between 11 and 20
    try:
        font_size = int(request.GET.get("font_size", 12))
    except (TypeError, ValueError):
        font_size = 12
    font_size = max(11, min(20, font_size))

    # measurements
    box_size = 0.2 * inch
    extra_padding = 0.05 * inch
    leading = font_size * 1.2 + extra_padding
    left_box_x = 1 * inch
    name_x = left_box_x + box_size + 0.1 * inch
    desc_x = 1.6 * inch
    bottom_margin = 1 * inch
    right_margin = 1 * inch

    # fetch activity
    activity = get_object_or_404(Activity, pk=pk, user=request.user)

    # start PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", font_size)
    p.drawString(left_box_x, height - 1 * inch, activity.name)

    # switch back to body font
    p.setFont("Helvetica", font_size)
    # first baseline
    y = height - 1.5 * inch + (box_size + extra_padding) / 2

    for item in activity.packing_items.all():
        # page‐break if needed
        if y - leading < bottom_margin:
            p.showPage()
            p.setFont("Helvetica", font_size)
            y = height - 1.5 * inch + (box_size + extra_padding) / 2

        # draw checkbox
        face = pdfmetrics.getFont("Helvetica").face
        ascent = face.ascent * font_size / 1000.0
        descent = face.descent * font_size / 1000.0
        text_h = ascent - descent

        # same centering but now within a taller line
        box_y = y + descent + (text_h - box_size) / 2
        p.rect(left_box_x, box_y, box_size, box_size, stroke=1, fill=0)

        # draw item name
        p.drawString(name_x, y, f"({item.quantity}) {item.name}")
        y -= leading

        # descriptions, etc...
        if item.description:
            lines = simpleSplit(
                item.description, "Helvetica", font_size, width - desc_x - right_margin
            )
            for line in lines:
                if y - leading < bottom_margin:
                    p.showPage()
                    p.setFont("Helvetica", font_size)
                    y = height - 1.5 * inch + (box_size + extra_padding) / 2
                p.drawString(desc_x, y, line)
                y -= leading

    # finish up
    p.save()
    buffer.seek(0)

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
    # 1. Try to grab an activity ID from the URL; if none, activity stays None
    activity = None
    activity_id = request.GET.get("activity")
    if activity_id:
        activity = get_object_or_404(Activity, pk=activity_id, user=request.user)

    # 2. Build the form, passing activity instance or None
    form = ItemForm(
        request.POST or None,  # data or None
        user=request.user,  # your custom kwarg
        activity=activity,  # instance or None
    )

    # 3. On valid POST, save and redirect
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return redirect(item.activity)

    # 4. Render form on GET or invalid POST
    return render(
        request,
        "packing_list/item_form.html",
        {
            "the_site_name": settings.THE_SITE_NAME,
            "page_title": "Create Item",
            "form": form,
            "activity": activity,  # you can use this in the template if you want
        },
    )


@registration_accepted_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    activity = item.activity

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
            "activity": activity,
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
