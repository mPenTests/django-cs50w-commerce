from django import forms
from .models import AuctionListing, Comment

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "price", "image"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'width: 400px;',
                'required': "True"
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'width: 800px;',
                'required': "True"
            }),
            'price': forms.NumberInput(attrs={
                'class': 'forms-control',
                'required': "True"
            }),
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["title", "comment"]
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 400px; margin-top: 15px;',
                'required': 'True'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 800px; margin-top: 15px;',
                'required': 'True'
            })
        }