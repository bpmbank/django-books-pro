# coding:utf8
from django.contrib import admin
from books_app.models import *
from django_markdown.admin import MarkdownModelAdmin


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'isbn', 'title', 'author', 'translator', 'publisher', 'type',)
    list_filter = ('type', 'publisher',)
    search_fields = ('id', 'title', 'isbn',)
    list_per_page = 20


#admin.site.register(Book)
admin.site.register(Book, MarkdownModelAdmin)


class CrawlURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'weight', 'is_save', 'date',)
    ordering = ('-id',)
    list_filter = ('is_save', 'weight', 'date',)
    fields = ('url', 'weight', 'is_save',)


admin.site.register(CrawlURL, CrawlURLAdmin)
