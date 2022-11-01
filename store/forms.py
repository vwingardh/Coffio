from django import forms

from .models import EmailList, Reviews


class ReviewForm(forms.ModelForm):
    """
    A form for users to create a review for a specific product.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "username"
            }
        )
    )
    review = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "review"
            }
        )
    )
    stars = forms.IntegerField(
        required=True,
        error_messages={
            'required': 'Please choose a rating.',
            'invalid': 'Please choose a rating.'
        },
        widget=forms.Select(
            attrs={
                "class": "form-check",
                "name": "stars"
            }
        )
    )
    created = forms.DateTimeField(
        required=False
    )
    verified = forms.BooleanField(
        required=False
    )

    class Meta:
        model = Reviews
        fields = [
            'username',
            'review',
            'stars',
        ]


class EmailListForm(forms.ModelForm):
    """
    A form to capture users that sign up for the email list.
    """
    
    email = forms.EmailField() 

    class Meta:
        model = EmailList
        fields = ['email']
        