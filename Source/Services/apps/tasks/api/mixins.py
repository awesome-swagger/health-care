from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class ValidateTaskTemplateAndCustomFields(object):

    def _validate_custom_fields(self, data, regular_edit=False):

        for custom_field in self.Meta.write_only_fields:
            value = data.get(custom_field)

            if regular_edit:
                value = getattr(self.instance, custom_field) \
                    if custom_field not in data.keys() \
                    else data.get(custom_field)

            if value is None:
                raise serializers.ValidationError({
                    custom_field: _('This field is required.')
                })

    def validate(self, data):

        if self.Meta.task_template_field not in data.keys() and \
           self.instance is None:
            self._validate_custom_fields(data)
        elif self.Meta.task_template_field in data.keys() and \
            not data.get(self.Meta.task_template_field) and \
                self.instance is not None:
            self._validate_custom_fields(data)
        elif self.Meta.task_template_field not in data.keys() and \
            self.instance is not None and \
                getattr(self.instance, self.Meta.task_template_field) is None:
            self._validate_custom_fields(data, regular_edit=True)

        return data
