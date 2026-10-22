from .models import Workspace, WorkspaceMemberShip, Project
from django.shortcuts import get_object_or_404
from .serializers import WorkspaceSerializer, ProjectSerializer
from .permissions import WorkspaceRolePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import responses
from rest_framework.decorators import action
from django.db import transaction

class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated, WorkspaceRolePermission]

    #le indico con que conjunto de objetos trabaja la vista
    def get_queryset(self):

        return Workspace.objects.filter(
            #uso memberships para aplicar la relacion inversa, accedo con memberships a los campos de WorkspaceMenberShip para filtrar
            memberships__user=self.request.user,
            memberships__status=WorkspaceMemberShip.Status.ACTIVE

        )

    @transaction.atomic
    def perform_create(self, serializer):
        user=self.request.user
        workspace = serializer.save()

        WorkspaceMemberShip.objects.create(workspace=workspace, user=user,
        rol=WorkspaceMemberShip.Role.OWNER)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


