from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import (CreateView)

from .forms import PostForm
from .models import Post


class CreatePost(PermissionRequiredMixin, CreateView):
    permission_required = 'app.add_post'
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    success_url = 'posts'

    def form_valid(self, form):
        form.instance.post_author = self.request.user.author
        return super().form_valid(form)


def index(request):
    return render(request, 'index.html')


def posts(request):
    post = Post.objects.order_by('-id')
    return render(request, 'posts.html', {'title': 'Новостной портал - Статьи', 'post': post})


def show_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post,
        'post_title': post.post_title,
        'post_text': post.post_text,
        'post_photo': post.post_photo,
        'post_author': post.post_author,
        'post_date': post.post_date,
        'post_date_update': post.post_date_update,
    }

    return render(request, 'app/post.html', context=context)
