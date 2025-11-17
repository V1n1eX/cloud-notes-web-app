from django import forms
from .models import Note, NoteShare
from django.contrib.auth.models import User

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'folder']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note here...'}),
        }

class ShareNoteForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username to share with")
    permission = forms.ChoiceField(choices=NoteShare.PERMISSION_CHOICES, label="Permission")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
        return user
