# do_it/serializers.py

from rest_framework import serializers
from .models import Tag, Cycle, Task

# from .models import TaskCompleted


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "description", "user"]
        read_only_fields = ["id", "user"]


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = ["id", "name", "periodicity", "user"]
        read_only_fields = ["id", "user"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "description", "tag", "cycle", "is_recurrent", "user"]
        read_only_fields = ["id", "user"]


# class TaskCompletedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskCompleted
#         fields = ["id", "task_repr", "date_scheduled", "date_completed", "user"]
#         read_only_fields = ["id", "user"]
