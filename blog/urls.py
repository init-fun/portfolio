from django.urls import path
from .views import post_detail, post_share, indexView
from django.conf import settings
from django.conf.urls.static import static
from .views import post_list
from .views import WorkExpView

# from .views import PostListView

# from .views import post_list # function based url

app_name = "blog"
# we define the app_name as "blog" so that later we can refer to the blog URL
# just by blog:post_list or blog:post_detail
urlpatterns = [
    path("", indexView, name="index"),
    path("post/", post_list, name="post_list"),  # function based view url
    path("carrer/", WorkExpView, name="carrer_page"),
    path("post/tag/<slug:tag_slug>/", post_list, name="post_list_by_tag"),
    path(
        "post/<int:year>/<int:month>/<int:day>/<slug:post>/",
        post_detail,
        name="post_detail",
    ),
    path("post/<int:post_id>/share/", post_share, name="post_share"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
