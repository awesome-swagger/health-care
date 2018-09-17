import pytz

from datetime import datetime, time
from rest_framework import filters
from rest_framework.compat import coreapi, coreschema

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


class DurationFilter(filters.BaseFilterBackend):
    """
    Custom filtering that enables views to filter using the model's
    `appear_datetime` or `due_datetime` fields.
    """
    appear_datetime_param = 'appear_datetime'
    appear_datetime_title = _('Appear Datetime')
    appear_datetime_description = _(
        'Appear Datetime format: YYYY-MM-DD`'
    )
    due_datetime_param = 'due_datetime'
    due_datetime_title = _('Due Datetime')
    due_datetime_description = _(
        'Due Datetime format: YYYY-MM-DD`'
    )

    def get_appear_datetime(self, request):
        appear_datetime = request.query_params.get('appear_datetime', None)
        if appear_datetime:
            appear_datetime = datetime.strptime(appear_datetime, '%Y-%m-%d')
            appear_datetime = datetime.combine(
                appear_datetime,
                time.min,
                tzinfo=pytz.utc
            )
        return appear_datetime

    def get_due_datetime(self, request):
        due_datetime = request.query_params.get('due_datetime', None)
        if due_datetime:
            due_datetime = datetime.strptime(due_datetime, '%Y-%m-%d')
        return due_datetime

    def filter_queryset(self, request, queryset, view):
        appear_datetime = self.get_appear_datetime(request)
        due_datetime = self.get_due_datetime(request)

        context = {}
        if appear_datetime:
            start_date = datetime.combine(
                appear_datetime.date(),
                time.min,
                tzinfo=pytz.utc
            )
            end_date = datetime.combine(
                appear_datetime.date(),
                time.max,
                tzinfo=pytz.utc
            )
            context.update({
                'appear_datetime__range': (start_date, end_date)
            })

        if due_datetime:
            start_date = datetime.combine(
                due_datetime.date(),
                time.min,
                tzinfo=pytz.utc
            )
            end_date = datetime.combine(
                due_datetime.date(),
                time.max,
                tzinfo=pytz.utc
            )
            context.update({
                'due_datetime__range': (start_date, end_date)
            })
        return queryset.filter(**context)

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.appear_datetime_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(self.appear_datetime_title),
                    description=force_text(self.appear_datetime_description)
                )
            ),
            coreapi.Field(
                name=self.due_datetime_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(self.due_datetime_title),
                    description=force_text(self.due_datetime_description)
                )
            ),
        ]
