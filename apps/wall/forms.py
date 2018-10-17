"""
Here we define forms that are specific to WallItems.
"""

from django import forms
from wall.models import Wall, WallItem
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop

class WallItemForm(forms.Form):
    """
    This form collects a new post.
    """
    posting = forms.CharField(label=_(u"Item"),
        widget=forms.Textarea(attrs={'rows': '10', 'cols':'100'}))
    img = forms.ImageField(label=_(u"Add an Image (optional)"),required=False)

    def __init__(self, *args, **kwargs):
        help_text = kwargs.pop('help_text', "")
        super(WallItemForm, self).__init__(*args, **kwargs)
        self.fields['posting'].help_text = help_text

    def save(self, user=None):
        posting = self.cleaned_data['posting']
        
        return posting
    
class WallItemCommentForm(forms.Form):
    """
    This form collects a comment.
    """
    comment = forms.CharField(label=_(u"Comment:"),max_length = 500,
        widget=forms.Textarea(attrs={'rows': '3'}))

    def __init__(self, *args, **kwargs):
        help_text = kwargs.pop('help_text', "")
        super(WallItemCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].help_text = help_text

    def save(self, user=None):
        comment = self.cleaned_data['comment']
        
        return comment

