from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Folder, NoteShare
from .forms import NoteForm, ShareNoteForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def notes_home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/accounts/login/')

    folders = Folder.objects.filter(owner=user, is_deleted=False)
    notes = Note.objects.filter(owner=user, folder__isnull=True, is_deleted=False)

    sort_by = request.GET.get('sort', 'time')
    if sort_by == 'name':
        notes = notes.order_by('title')
    else:  # default to 'time'
        notes = notes.order_by('-updated_at')

    context = {
        'folders': folders,
        'notes': notes,
        'current_sort': sort_by
    }
    return render(request, 'notes/notes_home.html', context)




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

# View Note
def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    return render(request, 'notes/view_note.html', {'note': note})

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

# Create Folder
def create_folder(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Folder.objects.create(name=name, owner=request.user)
            return redirect('notes_home')
    return render(request, 'notes/folder_form.html')

# Edit Folder
def edit_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            folder.name = name
            folder.save()
            return redirect('notes_home')
    return render(request, 'notes/folder_form.html', {'folder': folder})

# Delete Folder
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    folder.is_deleted = True
    folder.deleted_at = timezone.now()
    folder.save()
    return redirect('notes_home')

# Folder Detail
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user, is_deleted=False)
    notes = Note.objects.filter(owner=request.user, folder=folder, is_deleted=False)

    sort_by = request.GET.get('sort', 'time')
    if sort_by == 'name':
        notes = notes.order_by('title')
    else:  # default to 'time'
        notes = notes.order_by('-updated_at')

    context = {
        'folder': folder,
        'notes': notes,
        'current_sort': sort_by
    }
    return render(request, 'notes/folder_detail.html', context)

# Create Note in Folder
def create_note_in_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.folder = folder
            note.save()
            return redirect('folder_detail', folder_id=folder_id)
    else:
        form = NoteForm(initial={'folder': folder})
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Create', 'folder': folder})

# Move Note
def move_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user, is_deleted=False)
    if request.method == 'POST':
        folder_id = request.POST.get('folder')
        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
            note.folder = folder
        else:
            note.folder = None
        note.save()
        return redirect('notes_home')
    folders = Folder.objects.filter(owner=request.user)
    return render(request, 'notes/move_note.html', {'note': note, 'folders': folders})

# Recycle Bin
def recycle_bin(request):
    notes = Note.objects.filter(owner=request.user, is_deleted=True)
    folders = Folder.objects.filter(owner=request.user, is_deleted=True)
    return render(request, 'notes/recycle_bin.html', {'notes': notes, 'folders': folders})

# Restore Note
def restore_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user, is_deleted=True)
    note.is_deleted = False
    note.deleted_at = None
    note.save()
    return redirect('recycle_bin')

# Permanent Delete
def permanent_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user, is_deleted=True)
    note.delete()
    return redirect('recycle_bin')

# Restore Folder
def restore_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user, is_deleted=True)
    folder.is_deleted = False
    folder.deleted_at = None
    folder.save()
    return redirect('recycle_bin')

# Permanent Delete Folder
def permanent_delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user, is_deleted=True)
    folder.delete()
    return redirect('recycle_bin')

@login_required
def share_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    if request.method == 'POST':
        form = ShareNoteForm(request.POST, current_user=request.user)
        if form.is_valid():
            user = form.cleaned_data['user']
            permission = form.cleaned_data['permission']
            NoteShare.objects.get_or_create(
                note=note,
                user=user,
                defaults={'permission': permission, 'shared_by': request.user}
            )
            messages.success(request, f"Note shared with {user.username}.")
            return redirect('view_note', note_id=note.id)
    else:
        form = ShareNoteForm(current_user=request.user)
    return render(request, 'notes/share_note.html', {'form': form, 'note': note})

@login_required
def shared_notes(request):
    shared_notes = Note.objects.filter(shares__user=request.user).distinct()
    shared_notes_with_info = []
    for note in shared_notes:
        share = note.shares.filter(user=request.user).first()
        can_edit = note.can_user_edit(request.user)
        shared_notes_with_info.append({
            'note': note,
            'permission': share.permission if share else 'read',
            'can_edit': can_edit,
            'timestamp': note.updated_at
        })
    return render(request, 'notes/shared_notes.html', {'notes': shared_notes_with_info})

@login_required
def view_shared_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if not note.can_user_view(request.user):
        messages.error(request, "You do not have permission to view this note.")
        return redirect('notes_home')
    can_edit = note.can_user_edit(request.user)
    return render(request, 'notes/view_shared_note.html', {'note': note, 'can_edit': can_edit})

@login_required
def edit_shared_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if not note.can_user_edit(request.user):
        messages.error(request, "You do not have permission to edit this note.")
        return redirect('view_shared_note', note_id=note.id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return redirect('view_shared_note', note_id=note.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_shared_note.html', {'form': form, 'note': note})

@login_required
def remove_share(request, note_id, user_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    share = get_object_or_404(NoteShare, note=note, user_id=user_id)
    share.delete()
    messages.success(request, "Share removed.")
    return redirect('view_note', note_id=note.id)

