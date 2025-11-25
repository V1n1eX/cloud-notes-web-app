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
    username = forms.CharField(max_length=150, label="Username to share with", required=False)
    user_select = forms.ModelChoiceField(queryset=User.objects.all(), label="Select user", required=False, empty_label="Choose a user...")
    permission = forms.ChoiceField(choices=NoteShare.PERMISSION_CHOICES, label="Permission")

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if self.current_user:
            self.fields['user_select'].queryset = User.objects.exclude(id=self.current_user.id)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        user_select = cleaned_data.get('user_select')

        if not username and not user_select:
            raise forms.ValidationError("Please enter a username or select a user.")

        if username and user_select:
            raise forms.ValidationError("Please use either username field or user selection, not both.")

        if username:
            try:
                user = User.objects.get(username=username)
                if self.current_user and user == self.current_user:
                    raise forms.ValidationError("You cannot share with yourself.")
                cleaned_data['user'] = user
            except User.DoesNotExist:
                raise forms.ValidationError("User does not exist.")
        elif user_select:
            cleaned_data['user'] = user_select

        return cleaned_data
