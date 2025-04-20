'''from django import forms
from .models import Answer

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        for question in Question.objects.all():
            self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                queryset=Answer.objects.filter(question=question),
                widget=forms.RadioSelect,
                empty_label=None,
                label=question.text'''