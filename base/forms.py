from django import forms
# from allauth.account.forms import LoginForm


class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    phone_number = forms.IntegerField()
    zip_code = forms.CharField()
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


# class MyCustomLoginForm(LoginForm):

#     def __init__(self, *args, **kwargs):
#         super(MyCustomLoginForm, self).__init__(*args, **kwargs)
#         for fieldname, field in self.fields.items():
#             field.widget.attrs.update({
#                 'class': 'red-border'
#             })

#     def login(self, *args, **kwargs):
#         return super(MyCustomLoginForm, self).login(*args, **kwargs)
