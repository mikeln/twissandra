from django import forms

import cass

class InjectForm(forms.Form):
    numusers = forms.IntegerField(label='New Users', max_value=100000, min_value=1)
    numtweets = forms.IntegerField(label='New Tweets', max_value=100000, min_value=1)
    secdelay = forms.IntegerField(label='Delay (sec)', max_value=36400, min_value=0)
    #distroflag = forms.BooleanField(label='Random Dist', required=False)

    def clean(self):
        # no additional validation
        numusers = self.cleaned_data.get('numusers')
        numtweets = self.cleaned_data.get('numtweets')
        secdelay = self.cleaned_data.get('secdelay')
        #distroflag = self.cleaned_data.get('distroflag')
        return self.cleaned_data

