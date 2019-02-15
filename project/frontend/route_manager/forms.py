<<<<<<< HEAD
from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
=======
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
>>>>>>> development
        model = Post
        fields = ('ip', 'next_hop', 'community',)
