from django import forms
from allauth.account.forms import SignupForm
#from tinymce.widgets import TinyMCE
from tinymce.widgets import TinyMCE
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        #self.helper.form_class = 'form-control'
        self.helper.form_action = '/create/'
        self.helper.add_input(Submit('submit', 'Submit'))

    post_content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))

    # post_content = forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    # )
    class Meta:
        model = Post
        # widgets = {
        #     'post_content': TinyMCE(attrs={'required': False, 'cols': 30, 'rows': 10}),
        # }
        fields = ('title', 'overview', 'post_content', 'thumbnail', 'categories', 'featured', 'previous_post', 'next_post','tags')

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'pk': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )


