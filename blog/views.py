from django.shortcuts import render
from django.utils import timezone
from blog.models import Post
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from blog.forms import CommentForm
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie 

import logging
# Create your views here.

logger = logging.getLogger(__name__)

# @cache_page(300) # cache the response for 300 seconds 
# @vary_on_cookie #This function’s parameters are names of the headers that will cause the response to vary in our case it’s just the Cookie header
def index(request):
    # from django.http import HttpResponse # cache concpet
    # return HttpResponse(str(request.user).encode("ascii"))# cache concpet
    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug("Got %d posts", len(posts)) #this line is more efficient than one below.
    # logger.debug("Got %d posts" % (len(posts)))
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info(
                  "Created comment on Post %d for user %s", post.pk, request.user
                  )
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )