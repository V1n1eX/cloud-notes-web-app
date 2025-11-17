# TODO List for Adding Sorting and Folder Recycle Bin Functionality

## 1. Update Folder Model
- [x] Add `is_deleted` and `deleted_at` fields to Folder model in `notes/models.py`.

## 2. Create and Run Migration
- [x] Run `python manage.py makemigrations` to create migration for Folder model changes.
- [x] Run `python manage.py migrate` to apply the migration.

## 3. Update Views (notes/views.py)
- [x] Add sorting logic to `notes_home` view using `request.GET.get('sort')` for loose notes (sort by 'time' or 'name').
- [x] Add sorting logic to `folder_detail` view using `request.GET.get('sort')` for notes in folder.
- [x] Change `delete_folder` view to perform soft delete instead of hard delete.
- [x] Add `restore_folder` view to restore a soft-deleted folder.
- [x] Add `permanent_delete_folder` view to permanently delete a folder from recycle bin.
- [x] Update `recycle_bin` view to include deleted folders in context.

## 4. Update URLs (notes/urls.py)
- [x] Add URL patterns for `restore_folder` and `permanent_delete_folder`.

## 5. Update Templates
- [x] Update `notes/templates/notes_home.html`: Add sorting dropdown for loose notes.
- [x] Update `notes/templates/notes/folder_detail.html`: Add sorting dropdown for notes in folder.
- [x] Update `notes/templates/notes/recycle_bin.html`: Add section for deleted folders with restore/permanent delete actions.

## 6. Testing and Verification
- [x] Server started successfully at http://127.0.0.1:8000/
- [ ] Test sorting functionality for notes (by time and name) in notes_home and folder_detail.
- [ ] Test folder soft delete, restore, and permanent delete from recycle bin.
