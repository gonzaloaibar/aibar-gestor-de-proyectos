from rest_framework import serializers
from .models import Workspace, WorkspaceMemberShip, Project

class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields=('id','name', 'description', 'slug', 'created_at', 'updated_at')
        read_only_fields=('id','created_at', 'slug')



class WorkspaceMemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMemberShip
        fields = [
            'id',
            'workspace',
            'user',
            'role',
            'status',
        ]
        read_only_fields = ['id', 'status']

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields=('id','name', 'slug', 'description', 'created_at', 'updated_at', 'workspace')
        read_only_fields=('id','created_at', 'slug', 'workspace')

