from django import forms
from .models import Note, NoteShare
from django.contrib.auth.models import User

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'folder', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note here...'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Tags (comma-separated)'}),
        }

class ShareNoteForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username to share with", required=True)
    permission = forms.ChoiceField(choices=NoteShare.PERMISSION_CHOICES, label="Permission")

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            if self.current_user and user == self.current_user:
                raise forms.ValidationError("You cannot share with yourself.")
            return user
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
