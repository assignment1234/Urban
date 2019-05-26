from rest_framework import serializers
from .models import *


class TaskInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'priority', 'created', 'created_by', 'last_state')


class TaskStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskState
        fields = ('task', 'state', 'created')
