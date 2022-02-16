from django.forms import ModelForm
from .models import Case

class CreateCaseForm(ModelForm):
    class Meta:
        model=Case
        exclude=['owner']

        fields=['category','title','description','skill',
        'contact','amount','period','respondent','mode',
        'state']