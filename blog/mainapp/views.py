from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.translation import gettext as _
from .forms import PostForm
from .mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from .models import Post


# Create your views here.
# def posts_list(request):
#     # __lte = less than equal
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#     return render(request, 'mainapp/posts_list.html', {'posts': posts})


class PostsListView(ListView, BaseClassContextMixin):
    model = Post
    template_name = 'mainapp/posts_list.html'
    title = _('Posts list')

    def get_queryset(self):
        # __lte = less than equal
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return posts


class PostDetailView(DetailView, BaseClassContextMixin):
    model = Post
    title = _('Post view')


class PostCreateView(CreateView, BaseClassContextMixin, UserDispatchMixin):
    model = Post
    title = _('Post create')
    template_name = 'mainapp/post_edit.html'
    form_class = PostForm
    success_url = 'mainapp:post_detail'

    def form_valid(self, form):
        """
        if form is valid fill author post with current user
        @param form:
        @type form:
        @return:
        @rtype:
        """
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        """
        if success redirect to created post view
        @return:
        @rtype:
        """
        return reverse(self.success_url, args=(self.object.id,))


class PostUpdateView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = Post
    title = _('Post edit')
    template_name = 'mainapp/post_edit.html'
    form_class = PostForm
    success_url = 'mainapp:post_detail'

    def get_success_url(self):
        """
        if success redirect to created post view
        @return:
        @rtype:
        """
        return reverse(self.success_url, args=(self.object.id,))

    def post_publish(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        post.publish()
        # self.object = self.get_object()
        # self.object.publish()
        return redirect('mainapp:post_detail', pk=kwargs['pk'])
        # return HttpResponseRedirect(self.get_success_url())
        # return redirect(self.get_success_url())
        # return reverse(PostUpdateView.success_url, args=(self.object.id,))

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Post, pk=kwargs['pk'])
    #
    # def form_valid(self, form):
    #     form.instance.customer_id = self.kwargs['pk']
    #     return super(PostUpdateView, self).form_valid(form)


class PostsDraftsListView(ListView, BaseClassContextMixin, UserDispatchMixin):
    model = Post
    template_name = 'mainapp/posts_drafts_list.html'
    title = _('Posts drafts list')

    def get_queryset(self):
        posts_drafts = Post.objects.filter(published_date__isnull=True).order_by('created_at')
        return posts_drafts


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('mainapp:post_detail', pk=pk)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('mainapp:posts_list')
