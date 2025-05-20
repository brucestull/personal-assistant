# do_it/admin.py

from django.contrib import admin

from .models import Cycle, Tag, Task

# from .models import TaskCompleted


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name",)


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ("name", "periodicity", "user")
    list_filter = ("periodicity",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_recurrent", "cycle")
    list_filter = ("is_recurrent", "cycle")


# @admin.register(TaskCompleted)
# class TaskCompletedAdmin(admin.ModelAdmin):
#     list_display = ("task_repr", "user", "date_scheduled", "date_completed")
#     list_filter = ("user",)
