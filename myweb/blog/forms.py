from .models import Post, Comment, Profile, Tag
from django import forms

class PostForm(forms.ModelForm):

    tags_input = forms.CharField(
        required=False,
        label="태그",
        help_text="예, 태그1, 태그2",
    )
    class Meta:
        model = Post
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            current = self.instance.tags.values_list("name",flat=True)
            self.fields["tags_input"].initial =", ".join(current)


    def save(self, commit=True):
        post = super().save(commit=commit)
        raw = self.cleaned_data.get("tags_input", "")
        names = [t.strip() for t in raw.split(",") if t.strip()]

        if post.pk:
            tags_objs = []

            for name in names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags_objs.append(tag)

        post.tags.set(tags_objs)

        return post



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "bio"]
