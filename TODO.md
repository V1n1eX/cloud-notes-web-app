# TODO List for Enhancing Note Sharing with Permissions, Owner, and Timestamp

## 1. Update shared_notes View (notes/views.py)
- [x] Modify `shared_notes` view to pass permission and can_edit flag for each shared note.

## 2. Update shared_notes.html Template
- [x] Display permission level (read/write) for each shared note.
- [x] Show Edit button if user has write permission (not just owner).
- [x] Change timestamp to note's updated_at instead of shared_at.

## 3. Update Share Note Form
- [x] Add dropdown for user selection alongside username input.
- [x] Allow sharing with no specific user (optional sharing).
- [x] Update form validation to handle both input methods.

## 4. Apply Dark Theme to Templates
- [x] Update shared_notes.html with dark theme matching dashboard.
- [x] Update share_note.html with dark theme matching dashboard.
- [x] Update login.html with dark theme and JavaScript error messages.
- [x] Update register.html with dark theme and JavaScript error messages.
- [x] Update view_note.html with dark theme.
- [x] Update folder_form.html with dark theme.
- [x] Update recycle_bin.html with dark theme.
- [x] Update note_form.html with dark theme.
- [x] Update move_note.html with dark theme.
- [x] Update view_shared_note.html with dark theme.
- [x] Update edit_shared_note.html with dark theme.
- [x] Update folder_detail.html with dark theme.

## 5. Testing and Verification
- [x] Server started successfully at http://127.0.0.1:8000/
- [x] Created test users (testuser1, testuser2) and a shared note with read permission.
- [ ] Test sharing notes with read and write permissions.
- [ ] Verify shared notes list shows owner, permission, and correct timestamp.
- [ ] Ensure Edit button appears for write permission users.
- [ ] Test user selection dropdown and username input in share form.
- [ ] Test login and register forms with dark theme and error messages.
