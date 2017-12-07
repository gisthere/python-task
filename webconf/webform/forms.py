from django import forms


class SettingsForm(forms.Form):
    server_name = forms.CharField(label='ServerName', max_length=128)
    host = forms.CharField(label='Host', max_length=128)
    port = forms.CharField(label='Port', max_length=128)
    document_root = forms.CharField(label='DocumentRoot', max_length=128)
