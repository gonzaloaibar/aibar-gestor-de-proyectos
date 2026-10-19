from rest_framework import serializers
from .models import Workspace

class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fielsd=('name', 'description', 'slug', 'created_at', 'updated_at')
        read_only_fields=('created_at', 'updated_at', 'slug')


