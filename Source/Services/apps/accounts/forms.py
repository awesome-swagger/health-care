from django.contrib.auth.forms import SetPasswordForm


class CustomSetPasswordForm(SetPasswordForm):
    """
    A form that lets a user change set their password without entering the old
    password. This will also allow the user to set their `preferred_name`
    """

    def save(self, commit=True):
        preferred_name = self.data.get('preferred_name', '')
        password = self.cleaned_data["new_password1"]
        self.user.preferred_name = preferred_name
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
