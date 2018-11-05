from rest_framework.pagination import PageNumberPagination


class OrganizationEmployeePagination(PageNumberPagination):
    page_size = 20
