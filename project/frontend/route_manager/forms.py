"""
Define a new form used by POST method.
"""
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    This class is used for create a new route.
    """
    class Meta:
        """
        Class Method define model and required fields.
        """
        model = Post
        fields = ('ip', 'next_hop', 'community',)
