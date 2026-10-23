from .api import WorkspaceViewSet, ProjectViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspaces')

#Defino bien las operaciones en las vistas
project_list = ProjectViewSet.as_view({'get': 'list', 'post': 'create'})
project_detail = ProjectViewSet.as_view({
    'get': 'retrieve', 'put': 'update',
    'patch': 'partial_update', 'delete': 'destroy',
})
# member_list = MembershipViewSet.as_view({'get': 'list', 'post': 'create'})
# member_detail = MembershipViewSet.as_view({'patch': 'partial_update'})

urlpatterns = [
    path('', include(router.urls)),
    path('workspaces/<slug:workspace_slug>/projects/',project_list, name='project_list'),
    path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/',project_detail, name='project_detail'),
    # path('workspaces/<slug:workspace_slug>/members/', member_list, name='member-list'),
    # path('workspaces/<slug:workspace_slug>/members/<int:pk>/', member_detail, name='member-detail'),
]