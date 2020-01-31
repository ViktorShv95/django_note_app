from django.contrib import admin
from .models import Note, Category

@admin.register(Note)
class NoteModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']



admin.site.register(Category)
