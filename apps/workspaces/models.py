from django.db import models
from django.conf import settings

# Create your models here.
class Workspace(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(
        max_length=160,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workspace'
        indexes = [
            models.Index(fields=['slug'], name='idx_workspace_slug'),
        ]
        ordering = ('name', 'created_at')
        verbose_name_plural = 'Workspaces'

    def __str__(self):
        return f"{self.name}, {self.slug}, {self.created_at}"



class WorkspaceMemberShip(models.Model):

    class Role(models.IntegerChoices):
        VIEWER = 0, 'Viewer'
        MEMBER = 1, 'Member'
        ADMIN = 2, 'Admin'
        OWNER = 3, 'Owner'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'


    role = models.PositiveSmallIntegerField(choices=Role.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #relaciones
    workspace = models.ForeignKey('Workspace', on_delete=models.CASCADE,
                                  related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='workspace_memberships')

    class Meta:
        db_table = 'workspace_membership'
        verbose_name_plural = 'WorkspacesMemberships'
        ordering = ('workspace', 'joined_at')
        constraints = [
            models.UniqueConstraint(
                fields=['workspace', 'user'], name='uq_workspace_membership_user'
            ),
        ]

    def __str__(self):
        return f"{self.workspace.name}, {self.role}, {self.status}, {self.joined_at}"


class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=160,
        unique=True,
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wokspace = models.ForeignKey('Workspace', on_delete=models.CASCADE,
                                 related_name='projects')

    class Meta:
        db_table = 'project'
        ordering = ('name', 'created_at')
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['wokspace'], name='idx_projects_wokspace'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['wokspace', 'slug'],
                                    name='uq_project_slug_workspace'),]

    def __str__(self):
        return f"{self.name}, {self.slug}, {self.created_at}, {self.wokspace}"