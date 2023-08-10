from rest_framework.pagination import PageNumberPagination


class PagePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 30


def api_paging_by_list(records, next_page, page_size=10):
    try:
        next_page = int(next_page)
    except ValueError:
        next_page = 1
    if next_page == 0:
        next_page = 1
    start_record = 0
    total_record = len(records)
    remainder = total_record % page_size
    quotient = total_record / page_size
    if remainder > 0:
        quotient = quotient + 1
    total_page = quotient
    if next_page >= total_page:
        next_page = total_page
    if next_page > 1:
        start_record = (next_page - 1) * page_size
    end_record = start_record + page_size
    result_list = records[start_record:end_record]
    result = {
        'total_page': total_page,
        'next_page': next_page,
        'total_number': total_record,
        'data': result_list
    }
    return result
