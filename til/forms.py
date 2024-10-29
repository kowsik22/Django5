from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label=_("Email"))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            # Here you can use your custom logic to authenticate using email
            from django.contrib.auth import authenticate
            user = authenticate(request=self.request, username=email, password=password)
            if user is None:
                raise forms.ValidationError(_("Invalid login"))

        return self.cleaned_data
