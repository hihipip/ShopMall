from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=20,initial='')
    username = forms.CharField(max_length=20, initial='')
    password = forms.CharField(max_length=20, initial='')

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("Your password should be at least 6 Characters")
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6:
            raise forms.ValidationError("Your username should be at least 6 Characters")
        return username


