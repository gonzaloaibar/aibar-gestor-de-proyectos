
from .models import Workspace, WorkspaceMemberShip, Project
from django.shortcuts import get_object_or_404
from .serializers import WorkspaceSerializer, WorkspaceMemberShipSerializer, ProjectSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import responses

class WorkspaceViewSet(ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

class WorkspaceMemberShipViewSet(ModelViewSet):
    queryset = WorkspaceMemberShip.objects.all()
    serializer_class = WorkspaceMemberShipSerializer

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


