from django.contrib import admin

from .models import Category, Location, Post, Comment


class PostAdminInLine(admin.StackedInline):
    model = Post
    extra = 1


class CategoryAdmin(admin.ModelAdmin):

    inlines = (
        PostAdminInLine,
    )
    list_display = (
        'title',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    list_display_links = ('title',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
        'category',
    )
    list_filter = (
        'category',
    )
    search_fields = ('title',)
    empty_value_display = 'Не задано'


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostAdminInLine,
    )
    list_display = (
        'name',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'author',
    )
    list_filter = (
        'author',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
