from .api import WorkspaceViewSet, ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'workspaces', WorkspaceViewSet, basename='workspaces')
router.register(r'projects', ProjectViewSet, basename='projects')
urlpatterns = router.urls
