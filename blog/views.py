from typing import Annotated, NewType
from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Comment

# similar post
from django.db.models import Count

# class based view import
from django.views.generic import ListView

# pagination import
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# email form
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# taggin
from taggit.models import Tag

# all published post view (function based view)
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    # taggin
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # paginator
    paginator = Paginator(object_list, 2)  # 2 posts on each page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range then deliver the first page
        posts = paginator.page(paginator.num_pages)

    context = {
        "post_list": posts,
        "page": page,
        "tag": tag,
    }
    return render(request, "blog/post/list.html", context)


# all published post view (class based view)
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = "post_list"  # context variable name
#     paginate_by = 2
#     template_name = "blog/post/list.html"


def indexView(request):
    return render(request, "blog/front_page.html", {})


# to display a single post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # list of active comments for this post
    comments = post.comment.filter(active=True)

    new_comment = None

    if request.method == "POST":
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create a comment obj but dont save it for now
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()
    # similar post
    # retrieve a Python list of IDs for the tags of the current post.
    # flat=True to it to get single values such as [1, 2, 3, ...]
    post_tags_ids = post.tags.values_list("id", flat=True)  #
    # get all the posts containg any of these tags
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "similar_posts": similar_posts,
    }
    return render(request, "blog/post/detail.html", context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # send email
            # print(post.get_absolute_url())
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f" {cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, "admin@rj.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        "post": post,
        "form": form,
        "sent": sent,
    }
    return render(request, "blog/post/share.html", context)
