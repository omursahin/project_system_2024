from rest_framework.filters import OrderingFilter

from project_system_2024 import settings


class MyOrderingFilter(OrderingFilter):
    # The URL query parameter used for the ordering.
    ordering_param = settings.ORDERING_PARAM

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            order = request.query_params.get('order')
            if order == 'desc':
                ordering = ['-' + item for item in ordering]
            return queryset.order_by(*ordering)

        return queryset
