from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class PaginationWithCountHeader(LimitOffsetPagination):
    """ Inform the user of total count by header. """
    def get_paginated_response(self, data):
        count = self.count
        limit = self.limit
        headers = {'X-Total-Count': count, 'X-Limit': limit}
        return Response(data, headers=headers)
