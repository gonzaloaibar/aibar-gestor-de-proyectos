from django.conf import settings
from django.db import models

# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=160,unique=True,)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    project = models.ForeignKey('workspaces.Project', on_delete=models.CASCADE,
                                related_name='boards')

    class Meta:
        db_table = 'board'
        ordering = ('name',)
        verbose_name_plural = 'Boards'

        constraints = [
            models.UniqueConstraint(
                fields=['project', 'slug'], name='uq_board_slug_project'
            ),
        ]

    def __str__(self):
        return f"{self.name}, {self.slug}"


class BoardList(models.Model):
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    board = models.ForeignKey('Board', on_delete=models.CASCADE,
                              related_name='lists')
    class Meta:
        db_table = 'board_list'
        ordering = ('position',)
        verbose_name_plural = 'Boards Lists'

    def __str__(self):
        return f'{self.name}, {self.position}'


class Task(models.Model):

    class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        URGENT = 4, 'Urgent'

    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    position = models.IntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    board_list = models.ForeignKey(
        'BoardList',
        on_delete=models.CASCADE,
        related_name='tasks',
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
    )

    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tasks',
        blank=True,
    )

    class Meta:
        db_table = 'task'
        ordering = ('position',)
        verbose_name_plural = 'Tasks'
        indexes = [

            models.Index(fields=['due_date'], name='idx_task_due_date'),
        ]


    def __str__(self):
        return f'{self.title}, {self.priority}, {self.due_date}'


