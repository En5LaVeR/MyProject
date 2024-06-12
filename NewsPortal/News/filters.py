import django_filters
from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='post_time_in',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte'
    )

    class Meta:
        model = Post
        fields = {
            'author_id': ['exact'],
            'title': ['icontains'],

        }
