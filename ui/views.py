from django.shortcuts import render
from django.views.generic import TemplateView
from django import forms
from . import query

# create choice fields
HAPPY = (
    ('none', '----------'),
    ('happy', 'HAPPY'),
    ('neutral', 'NEUTRAL'),
    ('sad', 'SAD')
)

RELAX = (
    ('none', '----------'),
    ('relaxing', 'RELAXING'),
    ('neutral', 'NEUTRAL'),
    ('intensive', 'EXCITING')
)

NEW = (
    ('none', '----------'),
    ('yes', 'YES'),
    ('no', 'NO')
)


class SearchForm(forms.Form):
    """Create search form."""
    happy = forms.ChoiceField(label='How are you feeling today?', choices=HAPPY, required=False)
    relaxing = forms.ChoiceField(label='Do you prefer relaxing or exciting music?', choices=RELAX, required=False)
    yes = forms.ChoiceField(label='Would you prefer new songs?', choices=NEW, required=False)


class HomePageView(TemplateView):
    """Create homepage view."""
    def get(self, request, **kwargs):
        context = {}
        res = None
        if request.method == 'GET':
            # create a form instance and populate it with data from the request:
            form = SearchForm(request.GET)
            # check whether it's valid:
            if form.is_valid():
                # Convert form data to an args dictionary for recommendation
                args = {}
                if form.cleaned_data['happy'] != 'none':
                    args['happy'] = form.cleaned_data['happy']
                if form.cleaned_data['relaxing'] != 'none':
                    args['relaxing'] = form.cleaned_data['relaxing']
                if form.cleaned_data['yes'] != 'none':
                    args['yes'] = form.cleaned_data['yes']

                try:
                    res = query.execute(args)
                except Exception:
                    res = ''
        else:
            form = SearchForm()

        context['result'] = res
        context['form'] = form
        return render(request, 'index.html', context)
