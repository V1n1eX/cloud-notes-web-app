from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_home, name='notes_home'),
    path('create/', views.create_note, name='create_note'),
    path('create/<int:folder_id>/', views.create_note_in_folder, name='create_note_in_folder'),
    path('view/<int:note_id>/', views.view_note, name='view_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('move/<int:note_id>/', views.move_note, name='move_note'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('edit-folder/<int:folder_id>/', views.edit_folder, name='edit_folder'),
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('recycle-bin/', views.recycle_bin, name='recycle_bin'),
    path('restore/<int:note_id>/', views.restore_note, name='restore_note'),
    path('permanent-delete/<int:note_id>/', views.permanent_delete, name='permanent_delete'),
    path('restore-folder/<int:folder_id>/', views.restore_folder, name='restore_folder'),
    path('permanent-delete-folder/<int:folder_id>/', views.permanent_delete_folder, name='permanent_delete_folder'),
]
