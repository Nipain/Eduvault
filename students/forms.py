from django import forms
from .models import Student


class StudentAdmissionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            'admission_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input', # Your existing styles will still apply
                'placeholder': 'YYYY-MM-DD'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        relation = cleaned_data.get("guardian_relation")
        other = cleaned_data.get("guardian_relation_other")

        if relation == "other" and not other:
            raise forms.ValidationError(
                "Please specify relation if 'Other' is selected."
            )

        return cleaned_data