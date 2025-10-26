from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Folder
from .forms import NoteForm
from django.utils import timezone

# Create Note

def notes_home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/accounts/login/')
    
    folders = Folder.objects.filter(owner=user)
    notes = Note.objects.filter(owner=user, folder__isnull=True, is_deleted=False)

    context = {
        'folders': folders,
        'notes': notes
    }
    return render(request, 'notes/dashboard.html', context)




def create_note(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect('notes_home')
    else:
        form = NoteForm()

    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Create'})

# Edit Note
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_home')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Edit'})

# Soft Delete Note (Recycle Bin)
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    note.is_deleted = True
    note.deleted_at = timezone.now()
    note.save()
    return redirect('notes_home')
