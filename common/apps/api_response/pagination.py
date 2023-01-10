# from rest_framework.pagination import PageNumberPagination

# class CustomPagination(PageNumberPagination):
#     page_query_param = 'p'
#     page_size_query_param = 'page_size'

#     def __init__(self, page_size=None, max_page_size=None):
#         self.page_size = page_size
#         self.max_page_size = max_page_size

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_query_param = 'p'
    page_size_query_param = 'page_size'

    def __init__(self, page_size=6, max_page_size=100):
        self.page_size = page_size
        self.max_page_size = max_page_size
        self.count = None

    def paginate_data(self, data, request):
        self.page = request.query_params.get(self.page_query_param, 1)
        self.page_size = self._get_page_size(request)
        self.count = len(data)  # set count attribute
        paginated_data = self.paginate_queryset(data, request)
        return paginated_data

    def _get_page_size(self, request):
        """
        Return the page size to use for this request.
        """
        page_size = self.page_size
        if self.page_size_query_param:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
            except (KeyError, ValueError):
                pass

        if page_size > self.max_page_size:
            return self.max_page_size
        return page_size