from django.urls import path
from .views import post_detail, PostListView, post_share


# from .views import post_list # function based url

app_name = "blog"
# we define the app_name as "blog" so that later we can refer to the blog URL
# just by blog:post_list or blog:post_detail
urlpatterns = [
    # path("", post_list, name="post_list"), # function based view url
    path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail, name="post_detail"
    ),
    path("<int:post_id>/share/", post_share, name="post_share"),
]
