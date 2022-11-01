from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator

from .models import CustomUser

from django_countries.widgets import CountrySelectWidget
from django_countries import countries


class UserLoginForm(forms.Form):
    """
    A form for logging in registered users.
    """

    username = forms.CharField(
        required = True,
        strip = True,
        error_messages = {
            'unique': 'Username or password is incorrect.',
        },
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name" : "username"
            }
        )
    )
    password = forms.CharField(
        required = True,
        strip = True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password"
            }
        )   
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def clean_username(self):
        return self.cleaned_data["username"].lower().strip()

    def clean_password(self):
        return self.cleaned_data["password"].strip()
        

class UserRegistrationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all required fields, 
    plus a confirmation password.
    """

    username = forms.CharField(
        required = True,
        max_length = 50,
        min_length = 5,
        label = 'Username',
        help_text = 'Required',
        error_messages = {
            'required': 'Username is required to create an account.',
            'unique': 'An account with this username already exists.'
        },
        validators = [
            MaxLengthValidator(50, 'Username must be 50 characters or less.')
        ],
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'username'
            }
        )
    )
    email = forms.EmailField(
        required = True, 
        max_length=100, 
        label='Email',
        help_text='Required',
        error_messages={
            'required': 'An email address is required to create an account.',
            'unique': 'An account with this email address already exists.'
        },
        validators = [
            EmailValidator("Please enter a valid email address.")
        ],
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'name': 'email'
            }
        )
    )
    password_1 = forms.CharField(
        max_length=150, 
        label='Password',
        required = True,
        error_messages={'required': 'A password is required to create an account.'},
        validators = [
            MaxLengthValidator(150, 'Password must be 150 characters or less.'),
            MinLengthValidator(9, 'Password must be at least 9 characters.')
        ],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password_1'
            }
        )
    )
    password_2 = forms.CharField(
        max_length=150,
        required = True,
        label='Password Confirmation',
        error_messages={'required': 'Please confirm password.'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password_2',
                'placeholder': 'Confirm password'
            }
        )
    )
    first_name = forms.CharField(
        max_length=150, 
        label='First Name',
        required = True,
        help_text = 'Required',
        error_messages={'required': 'A first name is required to create an account.'},
        validators = [
            MaxLengthValidator(150, 'First name must be 150 characters or less.')
        ],
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'first_name'
            }
        )
    )
    last_name = forms.CharField(
        max_length=150, 
        label='Last Name',
        required = True,
        help_text = 'Required',
        error_messages={'required': 'A last name is required to create an account.'},
        validators = [
            MaxLengthValidator(150, 'Last name must be 150 characters or less.')
        ],
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'last_name'
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 
            'password_1', 
            'password_2', 
            'email', 
            'first_name', 
            'last_name'
        )

    def clean_username(self):
        return self.cleaned_data["username"].lower().strip()

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    
    def clean_password_1(self):
        return self.cleaned_data["password_1"].strip()
        
    def clean_password_2(self):
        return self.cleaned_data["password_2"].strip()

    def clean_first_name(self):
        return self.cleaned_data["first_name"].lower().strip()

    def clean_last_name(self):
        return self.cleaned_data["last_name"].lower().strip()


class UserShippingForm(forms.ModelForm):
    """
    A form for registered users to save their shipping info.
    """

    first_name = forms.CharField(
        max_length=150, 
        label='First Name',
        required = True,
        help_text = 'Required',
        validators = [
            MaxLengthValidator(150, 'First name must be 150 characters or less.')
        ],
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'first_name'
            }
        )
    )
    last_name = forms.CharField(
        max_length=150, 
        label='Last Name',
        required = True,
        help_text = 'Required',
        validators = [
            MaxLengthValidator(150, 'Last name must be 150 characters or less.')
        ],
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'last_name'
            }
        )
    )
    phone_number = forms.CharField(
        required = False,
        validators = [
            RegexValidator(r'^\d{3}-\d{3}-\d{4}$', 'Enter a valid phone number.')
        ],
        error_messages={'invalid': "Please include '-' in the phone number."},
        help_text="Format 555-555-5555",
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'phone_number'
            }
        )
    )
    address_line_1 = forms.CharField(
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'address_line_1'
            }
        )
    )
    address_line_2 = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'address_line_2'
            }
        )
    )
    city = forms.CharField(
        required = True,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'city'
            }
        )
    )
    state = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'state'
            }
        )
    )
    postcode = forms.CharField(
        required = True,
        validators = [
            RegexValidator('^\d{5}$', 'Enter a valid postcode.')
        ],
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'postcode'
            }
        )
    )
    country = forms.ChoiceField(
        widget=CountrySelectWidget, choices=countries
    )

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 
            'last_name', 
            'phone_number',
            'address_line_1', 
            'address_line_2', 
            'city',
            'state',
            'postcode',
            'country'
        )
 

class UserDeletionForm(forms.ModelForm):
    """
    A form for users to deactivate their accounts. is_active is 
    set to False rather than deleting the account.
    """

    is_active = forms.BooleanField(
        widget = forms.TextInput(
            attrs={
            'class': 'form-control',
            }
        )
    )

    class Meta: 
        model = CustomUser
        fields = ('is_active',)
     