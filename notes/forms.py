from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'folder']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note here...'}),
        }
