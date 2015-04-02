from django import forms

import cass

class InjectForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean(self):
        numusers = self.cleaned_data['numusers']
        numtweets = self.cleaned_data['numtweets']
        distroflag = self.cleaned_data['distroflag']
        numtweets = self.cleaned_data['numtweets']
        #try:
        #    user = cass.get_user_by_username(username)
        #except cass.DatabaseError:
        #    raise forms.ValidationError(u'Invalid username and/or password')
        #if user.password != password:
        #    raise forms.ValidationError(u'Invalid username and/or password')
        return self.cleaned_data

    def get_username(self):
        return self.cleaned_data['username']

