from django import forms
from .models import UserProfile, Comment


class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    phone_number = forms.IntegerField()
    zip = forms.CharField()
    city = forms.CharField()


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    # phone_number = forms.CharField(max_length=15)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # user.phone_number = self.cleaned_data['phone_number']
        user.save()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email",
                  "address", "city", "phone_number"]


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Enter Coupon Code'
    }))


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            "name": forms.Textarea(attrs={"cols": 80, "rows": 20}),
        }
