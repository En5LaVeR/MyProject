from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['title', 'post_text', 'categories', 'author_id', ]

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get("post_text")
        title = cleaned_data.get("title")

        if title == post_text:
            raise ValidationError(
                "Текст поста не должен быть идентичен названию."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
