from django.contrib import admin
from .models import Post, Comment
from .models import WorkExp
from .models import ProjectModel

# Register your models here.
# admin.site.register(Post)

# my model is registered in the the site using a custom clas PostAdmim which inherits from ModelAdmin class
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "created", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "body")
    ordering = ("created",)


@admin.register(WorkExp)
class WorkExpAdmin(admin.ModelAdmin):
    search_fields = ("organization", "position_held")
    ordering = ("from_year",)
    list_display = (
        "from_year",
        "to_year",
        "position_held",
        "organization",
        "summary",
    )


admin.site.register(ProjectModel)