from django.core.paginator import Paginator
from django.db.models import Q


class TableBuilder:

    class Meta:
        model = None
        columns = []
        actions = []
        search_fields = []
        filters = {}
        per_page = 10
        ordering = None

    def __init__(self, request):
        self.request = request

    def get_queryset(self):
        """
        Override jika ingin custom queryset.
        """
        model = self.Meta.model

        if model is None:
            raise ValueError(
                f"{self.__class__.__name__}.Meta.model harus diisi"
            )

        return model.objects.all()

    def apply_search(self, queryset):
        q = self.request.GET.get("q", "")

        if not q:
            return queryset

        search_fields = getattr(
            self.Meta,
            "search_fields",
            []
        )

        if not search_fields:
            return queryset

        query = Q()

        for field in search_fields:
            query |= Q(**{
                f"{field}__icontains": q
            })

        return queryset.filter(query)

    def apply_filters(self, queryset):

        filters = getattr(
            self.Meta,
            "filters",
            {}
        )

        for param_name, lookup in filters.items():

            value = self.request.GET.get(param_name)

            if value:
                queryset = queryset.filter(
                    **{lookup: value}
                )

        return queryset

    def apply_ordering(self, queryset):

        ordering = getattr(
            self.Meta,
            "ordering",
            None
        )

        if ordering:
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_page_obj(self, queryset):

        page_number = self.request.GET.get("page")

        paginator = Paginator(
            queryset,
            self.Meta.per_page
        )

        return paginator.get_page(page_number)

    def get_context(self):

        queryset = self.get_queryset()

        queryset = self.apply_search(queryset)
        queryset = self.apply_filters(queryset)
        queryset = self.apply_ordering(queryset)

        page_obj = self.get_page_obj(queryset)

        return {
            "page_obj": page_obj,
            "columns": self.Meta.columns,
            "actions": self.Meta.actions,
            "table_title": getattr(
                self.Meta,
                "table_title",
                ""
            ),
        }
        