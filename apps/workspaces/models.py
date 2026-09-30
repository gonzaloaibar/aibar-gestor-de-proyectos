from django.db import models

# Create your models here.

class WorkspaceMemberShips(models.Model):

    ROLES = [
        (0, 'Viewer'),
        (1, 'Member'),
        (2,'Admin'),
        (3,'Owner'),
    ]
    STATUS_CHOICES = [
        ('active','active'),
        ('inactive','inactive'),
        ('suspended','suspended'),
    ]
    rol = models.IntegerField(choices=ROLES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    joined_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    workspace = models.ForeignKey('Workspace', on_delete=models.CASCADE)

    class Meta:
        db_table = 'workspace_membership'
        verbose_name_plural = 'WorkspacesMemberships'
        ordering = ('workspace', 'joined_at')
        constraints = [
            models.UniqueConstraint(fields=['workspace', 'role'], name='uq_workspace_membership_role'),
        ]

    def __str__(self):
        return f"{self.workspace.name}, {self.role}, {self.status}, {self.joined_at}"

class Workspace(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(
        max_length=160,
        unique=True,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workspace'
        indexes = [
            models.Index(fields=['slug'], name='idx_workspace_slug'),
        ]
        ordering = ('name', 'create_at')
        verbose_name_plural = 'Workspaces'

    def __str__(self):
        return f"{self.name}, {self.slug}, {self.create_at}"


class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=160,
        unique=True,
    )
    descripcion = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wokspace = models.ForeignKey('Workspace', on_delete=models.CASCADE)

    class Meta:
        db_table = 'project'
        ordering = ('name', 'create_at')
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['wokspace'], name='idx_projects_wokspace'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['wokspace', 'slug'],
                                    name='uq_project_slug_workspace'),]

    def __str__(self):
        return f"{self.name}, {self.slug}, {self.create_at}, {self.wokspace}"