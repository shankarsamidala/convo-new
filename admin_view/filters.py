import django_filters

from login import models
from django import forms

class GDFileter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter(lookup_expr='gte', label='Date')
    class Meta:
        model = models.Attendance
        fields = ['college_id','date','presence']


class DayFileter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter(lookup_expr='gte', label='Date')
    class Meta:
        model = models.Attendance
        fields = ['college_id','date']
