
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Post
from .forms import PostForm
def post_list(request):
    posts = Post.objects.order_by('-id')
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        return render(request, "blog/post_confirm_delete.html", {"post": post})

    if request.method == "POST":
        post.delete()
        return redirect("post_list")

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post" : post})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

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



# templates