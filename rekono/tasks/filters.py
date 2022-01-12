from django_filters import rest_framework
from django_filters.rest_framework.filters import OrderingFilter
from tasks.models import Task


class TaskFilter(rest_framework.FilterSet):
    o = OrderingFilter(
        fields=(
            ('target__project', 'project'),
            'target', 'process', 'tool', 'intensity', 'executor', 'status', 'start', 'end'
        ),
    )

    class Meta:
        model = Task
        fields = {
            'target': ['exact'],
            'target__target': ['exact', 'icontains'],
            'target__project': ['exact'],
            'target__project__name': ['exact', 'icontains'],
            'process': ['exact'],
            'process__name': ['exact', 'icontains'],
            'tool': ['exact'],
            'tool__name': ['exact', 'icontains'],
            'intensity': ['exact'],
            'executor': ['exact'],
            'executor__username': ['exact', 'icontains'],
            'status': ['exact'],
            'start': ['gte', 'lte', 'exact'],
            'end': ['gte', 'lte', 'exact']
        }