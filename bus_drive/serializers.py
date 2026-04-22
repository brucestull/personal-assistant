from rest_framework import serializers

from .models import Thought


class ThoughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thought
        fields = ["id", "text", "created", "updated"]
        read_only_fields = ["id", "created", "updated"]
