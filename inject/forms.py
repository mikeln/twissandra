from django import forms

import cass

class InjectForm(forms.Form):
    numusers = forms.IntegerField(label='Number of New Users to Add', max_value=100000, min_value=-2)
    numtweets = forms.IntegerField(label='Number of New Tweets to Add', max_value=100000, min_value=-2)
    secdelay = forms.IntegerField(label='Delay between tweets (sec)', max_value=36400, min_value=0)
    distroflag = forms.BooleanField(label='Use Random Distribution', required=False)

    def clean(self):
        # no additional validation
        numusers = self.cleaned_data.get('numusers')
        numtweets = self.cleaned_data.get('numtweets')
        secdelay = self.cleaned_data.get('secdelay')
        distroflag = self.cleaned_data.get('distroflag')
        return self.cleaned_data

    def inject(self):
        numusers = self.cleaned_data.get('numusers')
        numtweets = self.cleaned_data.get('numtweets')
        secdelay = self.cleaned_data.get('secdelay')
        distroflag = self.cleaned_data.get('distroflag')
        #
        # call injection here?
        #
        return self.cleaned_data

