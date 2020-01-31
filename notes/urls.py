from django.contrib import admin
from django.urls import path
from note import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.NoteAppLoginView.as_view(), name='login_page'),
    path('register', views.RegisterUserView.as_view(), name='register_page'),
    path('logout', views.NoteAppLogout.as_view(), name='logout_page'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/create', views.create_note, name='note_create'),
    path('notes/<int:id>/update', views.update_note, name='note_update'),
    path('notes/<int:id>/delete', views.delete_note, name='note_delete'),
    path('notes/<uuid:link_id>', views.share_page, name='note_share'),
]
