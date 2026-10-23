from .models import Workspace, WorkspaceMemberShip, Project
from .serializers import WorkspaceSerializer, ProjectSerializer
from .permissions import WorkspaceRolePermission, ProjectPermission, AdminCanWrite, OwnerCanWrite, get_workspace
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db import transaction
from django.utils.text import slugify

def generate_unique_slug(model, name, **scope):
    base = slugify(name)[:150] or 'item'  # deja lugar al sufijo (max_length=160)
    slug, n = base, 2
    while model.objects.filter(slug=slug, **scope).exists():
        slug = f'{base}-{n}'
        n += 1
    return slug

class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkspaceSerializer
    lookup_field = 'slug'

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
        workspace = get_workspace(self.request, self)
        serializer.save(workspace=workspace)

        WorkspaceMemberShip.objects.create(workspace=workspace, user=user,
        role=WorkspaceMemberShip.Role.OWNER, slug=generate_unique_slug(Workspace, serializer.validated_data['name']))

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            perm = AdminCanWrite
        elif self.action == 'destroy':
            perm = OwnerCanWrite
        else:
            perm = WorkspaceRolePermission

        return[IsAuthenticated(), perm()]

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]
    lookup_field = 'slug'
    workspace_kwarg = 'workspace_slug'

    def get_queryset(self):
        workspace = get_workspace(self.request, self)
        return Project.objects.filter(workspace=workspace)

    @transaction.atomic
    def perform_create(self, serializer):
        workspace=get_workspace(self.request,self)
        serializer.save(
            workspace=workspace,
            slug=generate_unique_slug(Project, serializer.validated_data['name'], workspace=workspace),
        )



