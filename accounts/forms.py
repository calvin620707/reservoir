from django import forms
from django.forms import modelformset_factory

from . import models
from accounts.util import refresh_project_memberships


class UpdateProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = kwargs['instance'].members

    class Meta:
        model = models.Project
        fields = ['name', 'description', 'start_date', 'end_date', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
        }

    def save(self, commit=True):
        super().save(commit=False)
        if 'members' in self.changed_data:
            refresh_project_memberships(self.instance, list(self.cleaned_data['members'].all()))
        self.instance.save()


class UpdateMembershipForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMembership
        fields = ['user', 'rate']
        widgets = {
            'user': forms.Select(attrs={'readonly': True})
        }

    def clean(self):
        super().clean()
        if 'user' in self.changed_data:
            raise forms.ValidationError("You shouldn't change user")


MembershipFormSet = modelformset_factory(
    models.ProjectMembership,
    form=UpdateMembershipForm,
    extra=0
)


class CreateNewProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        e_date = cleaned_data.get('end_date')
        s_date = cleaned_data.get('start_date')
        if (e_date and s_date) and (e_date < s_date):
            raise forms.ValidationError("End date should be greater than start date.")
