from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 5

    # to change variable page from default to user define variable use below
    # watch/ordering_watch/?ordering=-avg_rating&page=2" -> watch/ordering_watch/?ordering=-avg_rating&p=2"
    # page_query_param = 'p'
    # page_size_query_param = 'size' # client side page size requirement
    max_page_size =6


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10


class WatchListCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'created'