from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , PasswordChangeForm
from .models import Profile , Location , Ad , Category , sub_category , Review , Contact


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20, help_text='First Name' , widget=forms.TextInput(attrs={'placeholder':'User Name'}))
    first_name = forms.CharField(max_length=20, help_text='First Name' , widget=forms.TextInput(attrs={'placeholder':'First Name*'}))
    last_name = forms.CharField(max_length=20 , help_text='Last Name', widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(max_length=30 , help_text= 'Email' , widget=forms.TextInput(attrs={'placeholder':'Email*'}))
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Password*'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email','first_name', 'last_name',
                 'password1', 'password2')


class EditProfile(UserChangeForm):

    class Meta:
        model = User
        fields = ('username' , 'email' , 'first_name' , 'last_name' )


class ChangePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('Old Password' , 'New Password' , 'Confirm Password')


class UserPicture(forms.ModelForm):
    ad_profile_pic = forms.ImageField(help_text='Max Image Size: 3MB',required=False , widget= forms.FileInput(attrs={'accept':"image/*" }))
    Phone = forms.CharField(widget= forms.TextInput(attrs={'placeholder':"987*******" , 'class': 'form-control-file mt-4 pt-1'}))

    class Meta:
        model= Profile
        fields = ('ad_profile_pic','Phone')


class LocationForm(forms.ModelForm):
    location = forms.CharField(widget= forms.TextInput(attrs={'placeholder':"Address"}))
    city = forms.CharField(widget= forms.TextInput(attrs={'placeholder':"City"}))
    state = forms.CharField(widget= forms.TextInput(attrs={'placeholder':"State"}))
    pin_code = forms.CharField(widget= forms.TextInput(attrs={'placeholder':"Pin Code"}))

    class Meta:
        model = Location
        fields =('location' , 'city' , 'state' , 'pin_code')

STATUS= [
    ('True', 'Active'),
    ('False', 'Inactive')
    ]

class AdForm(forms.ModelForm):
    ad_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Title of your Ad"}))
    ad_brand = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Brand"}))
    ad_model = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Model"}))
    condition = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Condition"}))
    ad_price = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Price"}))
    ad_description= forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write about Product Description" }) )
    ad_image1 = forms.ImageField(help_text='Max Image Size: 3MB', widget=forms.FileInput(attrs={'accept': "image/*"}))
    ad_image2 = forms.ImageField(help_text='Max Image Size: 3MB', widget=forms.FileInput(attrs={'accept': "image/*"}) , required= False)
    ad_image3 = forms.ImageField(help_text='Max Image Size: 3MB', widget=forms.FileInput(attrs={'accept': "image/*"}) , required= False)
    ad_status = forms.CharField(label='Ad Status', widget=forms.RadioSelect( attrs={'class': 'py-2'} , choices=STATUS))
    ad_location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Address"}))
    ad_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "City"}))
    ad_state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "State"}))
    ad_pin_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Pin Code"}))
    class Meta:
        model = Ad
        fields = {'ad_title', 'ad_subcat' ,'ad_brand', 'condition', 'ad_description','ad_cat',  'ad_price' , 'ad_model' , 'ad_status' ,'ad_image1',
                 'ad_image2', 'ad_image3','ad_location' , 'ad_city' , 'ad_state' , 'ad_pin_code'}


class ReviewForm(forms.ModelForm):
    subject = forms.CharField(widget= forms.TextInput(attrs={'placeholder' :"Subject"}))
    ad_message = forms.CharField(widget= forms.Textarea(attrs={'placeholder' :"Message"}))

    class Meta:
        model = Review
        fields = {'subject','ad_message',}

class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Name"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Subject"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Type Your Message"}))

    class Meta:
        model = Contact
        fields = {'name','subject', 'message' }

