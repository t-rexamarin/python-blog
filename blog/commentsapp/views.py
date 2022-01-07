from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from commentsapp.forms import CommentForm
from commentsapp.models import Comment
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


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('mainapp:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('mainapp:post_detail', pk=comment.post.pk)
