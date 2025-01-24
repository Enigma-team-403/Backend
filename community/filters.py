from django_filters import FilterSet, CharFilter
from .models import Community

class CommunityFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Community Name')
    category = CharFilter(field_name='category__name', lookup_expr='icontains', label='Category Name')

    class Meta:
        model = Community
        fields = ['name', 'category']