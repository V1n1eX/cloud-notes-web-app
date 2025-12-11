from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.TextField(null=True, blank=True)  # Comma-separated tags
    is_deleted = models.BooleanField(default=False)  # For recycle bin
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Not nullable
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True)  # Nullable
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)  # Comma-separated tags
    is_deleted = models.BooleanField(default=False)  # For recycle bin
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Untitled"

    def can_user_view(self, user):
        return self.owner == user or self.shares.filter(user=user).exists()

    def can_user_edit(self, user):
        return self.owner == user or self.shares.filter(user=user, permission='write').exists()

class NoteShare(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read Only'),
        ('write', 'Read and Write'),
    ]
    note = models.ForeignKey(Note, related_name='shares', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='read')
    shared_by = models.ForeignKey(User, related_name='shared_notes', on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('note', 'user')

    def __str__(self):
        return f"{self.note.title} shared with {self.user.username} ({self.permission})"
