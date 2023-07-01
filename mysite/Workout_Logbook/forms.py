from django import forms
from .models import CustomUserExercise


class CustomUserExerciseForm(forms.ModelForm):
    class Meta:
        model = CustomUserExercise
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        reference = cleaned_data.get('reference')
        name = cleaned_data.get('name')
        if not reference:
            if not name:
                self.add_error('name', 'This field is mandatory.')
            return cleaned_data
        for field_name, field in cleaned_data.items():
            if field_name in ['user', 'reference', 'tips', 'description', 'aliases']:
                continue
            if field_name == 'name':
                cleaned_data['name'] = name or reference.name
                continue
            cleaned_data[field_name] = getattr(reference, field_name) or cleaned_data[field_name]
        cleaned_data['reference'] = None
        return cleaned_data
