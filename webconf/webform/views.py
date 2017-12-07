from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.core.management import call_command

from webform.forms import SettingsForm
from webform.models import Label


class WebFormView(TemplateView):
    template_name = "webform.html"

    def get(self, request, *args, **kwargs):
        # TODO: replace with ModelForm
        form = SettingsForm()
        for f in form.visible_fields():
            form.fields[f.html_name].initial = Label.objects.get(key=f.label).value

        response = TemplateResponse(request, self.template_name, {'form': form})
        return response

    def post(self, request, *args, **kwargs):
        form = SettingsForm(request.POST)
        result = False
        if form.is_valid():
            for f in form.visible_fields():
                Label.objects.update_or_create(
                    key=f.label, defaults={"value": f.data})
            call_command('update_settings')
            result = True
        response = TemplateResponse(request, self.template_name, {'form': form, 'success': result})
        return response
