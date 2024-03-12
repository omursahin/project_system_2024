from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'items_per_page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'payload': {
                'pagination': {
                    'links': [
                        {
                            'url': self.get_previous_link(),
                            'label': "Previous",
                            'active': False,
                            'page': self.page.number - 1
                            if self.page.number > 1 else None
                        },
                        {
                            'url': self.get_next_link(),
                            'label': "Next",
                            'active': False,
                            'page': self.page.number + 1
                            if self.page.number < self.page.paginator.num_pages
                            else None
                        }
                    ],
                    'next_page_url': self.get_next_link(),
                    'previous_page_url': self.get_previous_link(),
                    'current_page': self.page.number,
                    'per_page': self.page.paginator.per_page,
                    'total': self.page.paginator.count,
                    'total_pages': self.page.paginator.num_pages
                }
            }
        })
