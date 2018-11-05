from django import forms


class CarePlanTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CarePlanTemplateForm, self).__init__(*args, **kwargs)

        self.fields['type'].required = True
