from django import forms

from accounts.models import Project


class UpdateProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = kwargs['instance'].members

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
        }


class CreateNewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        e_date = cleaned_data.get('end_date')
        s_date = cleaned_data.get('start_date')
        if (e_date and s_date) and (e_date < s_date):
            raise forms.ValidationError("End date should be greater than start date.")