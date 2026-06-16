from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone

from django.core.paginator import Paginator

class TableBuilder:

    headers = []
    table_title = ""

    def __init__(
        self,
        # headers=None,
        rows=None,
        actions=True,
        striped=True,
        hover=True
    ):
        # self.headers = headers or self.__class__.headers
        self.rows = rows or []
        self.actions = actions
        self.striped = striped
        self.hover = hover

    def add_row(self, cells, actions=None):

        self.rows.append({
            "cells": cells,
            "actions": actions or []
        })

    def to_dict(self):
        return {
            "table_title": self.table_title,
            "headers": self.headers,
            "rows": self.rows,
        }

def build_table_context(
    *
    request,
    queryset,
    columns,
    actions,
    search_fields=None,
    filters=None,
    per_page=10,
):
    """

    Args:
        request (_type_): _description_
        queryset (QuerySet): _description_
        columns (_type_): _description_
        actions (_type_): _description_
        search_fields (_type_, optional): _description_. Defaults to None.
        filters (_type_, optional): _description_. Defaults to None.
        per_page (int, optional): _description_. Defaults to 10.

    Returns:
        _type_: _description_
        
    Example:
        >>> build_table_context(request, queryset, columns, actions, search_fields, filters)
        
        contoh filter:
        
        filters = {
            "tanggal": "created_at__date",
            "status": "status",
            "pegawai": "pegawai_id",
        }
        
        filters = {
            "tanggal_awal": "created_at__date__gte",
            "tanggal_akhir": "created_at__date__lte",
            "status": "status",
        }
        
        columns = [
            {"key": "created_at", "label": "Tanggal", "tipe": "date"},
            {"key": "status", "label": "Status"},
        ]
        
        actions = [
            {
                "key": "detail",
                "label": "Detail",
                "url": "disposisi_detail",
                "param": "id",
            },
        ]

    """
    q = request.GET.get("q", "")
    page_number = request.GET.get("page")

    # search
    if q and search_fields:
        query = Q()

        for field in search_fields:
            query |= Q(**{f"{field}__icontains": q})

        queryset = queryset.filter(query)

    # dynamic filters
    if filters:
        for param_name, lookup in filters.items():
            value = request.GET.get(param_name)

            if value:
                queryset = queryset.filter(**{lookup: value})

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
    }
        
