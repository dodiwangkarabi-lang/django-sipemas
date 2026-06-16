import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse

# models
from accounts.models import (
    Masyarakat, Petugas
)
from django.contrib.auth.models import User

class AccountTable(tables.Table):
    aksi = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name="Aksi"
    )

    ACTIONS = [
        {
            "title": "Detail",
            "url": "accounts:accounts_web:detail",
            "icon": "eye-outline",
        },
    ]
    
    def render_aksi(self, record):

        user = self.request.user

        html = []

        for action in self.ACTIONS:

            permission = action.get("permission")

            if permission and not user.has_perm(permission):
                continue

            url = reverse(
                action["url"],
                args=[record.pk]
            )

            html.append(
                f'''
                <a
                    href="{url}"
                    class="text-blue-600 hover:text-blue-800"
                >
                    {action["title"]}
                </a>
                '''
            )

        return format_html(" | ".join(html))
    
    class Meta:
        model = Masyarakat
        fields = ["id", "nik", "nama", "email", "alamat"]
        template_name = "core/partials/tables/tailwind.html"
        per_page = 10

