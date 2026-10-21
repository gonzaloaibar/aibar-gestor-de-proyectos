from django.urls import path
from .api import WorkspaceViewSet, WorkspaceMemberShipViewSet, ProjectViewSet

urlpatterns = [
    path('workspaces/', WorkspaceViewSet.as_view(), name='workspaces'),
    path('projects/', ProjectViewSet.as_view(), name='projects'),
]