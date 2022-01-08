from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.utils.translation import gettext as _
from commentsapp.forms import CommentForm
from commentsapp.models import Comment
from mainapp.mixin import BaseClassContextMixin
from mainapp.models import Post


# Create your views here.
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('mainapp:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'commentsapp/add_comment_to_post.html', {'form': form})


class CommentCreateView(CreateView, BaseClassContextMixin):
    model = Comment
    title = _('Add comment')
    template_name = 'commentsapp/add_comment_to_post.html'
    form_class = CommentForm
    success_url = 'mainapp:post_detail'

    def form_valid(self, form, *args, **kwargs):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs['pk']
        comment.save()
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        """
        if success redirect to created post view
        @return:
        @rtype:
        """
        return reverse(self.success_url, args=(self.kwargs['pk'],))


class CommentUpdateView(UpdateView, BaseClassContextMixin):
    model = Comment
    template_name = 'mainapp:post_detail'

    def comment_approve(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        comment.approve()
        return redirect('mainapp:post_detail', pk=comment.post.pk)

    def comment_remove(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        comment.delete()
        return redirect('mainapp:post_detail', pk=comment.post.pk)
