from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, ProfileForm


def post_list(request):
    posts = Post.objects.order_by("-id")
    return render(request, "blog/post_list.html", {"posts": posts})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if hasattr(post, "author") and post.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "GET":
        return render(request, "blog/post_confirm_delete.html", {"post": post})

    if request.method == "POST":
        post.delete()
        return redirect("post_list")


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comments = post.comments.select_related("author").all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect("post_detail", pk=post.pk)

        return render(
            request,
            "blog/post_detail.html",
            {"post": post, "comments": comments, "comment_form": comment_form},
        )

    comment_form = CommentForm()
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})

    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("post_list")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if hasattr(post, "author") and post.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, "blog/post_form.html", {"form": form, "post": post})

    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post_detail", pk=post.pk)

    return render(request, "blog/post_form.html", {"form": form, "post": post})


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "GET":
        form = CommentForm(instance=comment)
        return render(request, "blog/comment_form.html", {"form": form, "comment": comment})

    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("post_detail", pk=comment.post.pk)

    return render(request, "blog/comment_form.html", {"form": form, "comment": comment})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "GET":
        return render(request, "blog/comment_confirm_delete.html", {"comment": comment})

    if request.method == "POST":
        post_pk = comment.post.pk
        comment.delete()
        return redirect("post_detail", pk=post_pk)


User = get_user_model()


def profile_detail(request, username):
    target_user = get_object_or_404(User, username=username)

    # ✅ 없으면 자동 생성해서 "User has no profile" 방지
    profile, _ = Profile.objects.get_or_create(user=target_user)

    return render(request, "blog/profile_detail.html", {
        "target_user": target_user,
        "profile": profile,
    })


@login_required
def profile_edit(request):

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, "blog/profile_form.html", {"form": form})