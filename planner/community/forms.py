from django import forms
from .models import MembershipRequest

class MembershipRequestForm(forms.ModelForm):
    community_id = forms.IntegerField(label='Community ID')
    requester_id = forms.IntegerField(label='Requester ID')

    class Meta:
        model = MembershipRequest
        fields = ['community_id', 'requester_id']
