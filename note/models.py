import uuid
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Категория")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок заметки')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор заметки', null=True)
    content = models.TextField(verbose_name='Текст заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата/время создания заметки', db_index=True)
    category = models.ForeignKey(Category, verbose_name='Категория', db_index=True, on_delete=models.CASCADE)
    chosen = models.BooleanField(db_index=True, verbose_name='Избранная')
    ready_to_pub = models.BooleanField(db_index=True, verbose_name='Доступна для публикации', default=True)
    link_id = models.UUIDField(default=uuid.uuid4, verbose_name='id для доступа по ссылке')


    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.title




