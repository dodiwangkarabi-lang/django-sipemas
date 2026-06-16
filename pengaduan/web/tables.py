import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse

# models
from pengaduan.models import (
    Pengaduan
)

# def render_aksi(self, record):
#     url = reverse(
#         'pengaduan:pengaduan_web:lihat_status_laporan',
#         args=[record.pk]
#     )

#     return format_html(
#         '<a href="{}">Detail</a>',
#         url
#     )

class PengaduanTable(tables.Table):
    aksi = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name="Aksi"
    )

    ACTIONS = [
        {
            "title": "Detail",
            "url": "pengaduan:pengaduan_web:lihat_status_laporan",
            "icon": "eye-outline",
        },
        # {
        #     "title": "Verifikasi Laporan",
        #     "url": "pengaduan:pengaduan_web:verifikasi_laporan",
        #     # "permission": "pengaduan.change_pengaduan",
        #     "icon": "create-outline",
        # },
        # {
        #     "title": "Hapus",
        #     "url": "pengaduan:pengaduan_web:hapus",
        #     "permission": "pengaduan.delete_pengaduan",
        #     "icon": "trash-outline",
        # },
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
        model = Pengaduan
        fields = ["masyarakat", "kategori", "status", "judul"]
        template_name = "core/partials/tables/tailwind.html"
        per_page = 10




# from core.table_builder import TableBuilder

# # models
# from pengaduan.models import (
#     Pengaduan
# )

# class PengaduanTable(TableBuilder):
#     class Meta:
#         model = Pengaduan

#         table_title = "Data Pengaduan"

#         columns = [
#             {
#                 "key": "masyarakat.nama",
#                 "label": "Masyarkat",
#             },
#             {
#                 "key": "kategori",
#                 "label": "Kategori",
#             },
#             # {
#             #     "key": "status",
#             #     "label": "Status",
#             # },
#             # {
#             #     "key": "created_at",
#             #     "label": "Tanggal",
#             # },
#         ]

#         actions = [
#         #     {
#         #         "key": "detail",
#         #         "label": "Detail",
#         #         "url": "pengajuan:detail",
#         #         "param": "id",
#         #     },
#         #     {
#         #         "key": "edit",
#         #         "label": "Edit",
#         #         "url": "pengajuan:update",
#         #         "param": "id",
#         #     },
#         # ]

#         # search_fields = [
#         #     "nomor_pengajuan",
#         #     "pemohon__nama",
#         ]

#         # filters = {
#         #     "status": "status",
#         #     "tanggal_awal": "created_at__date__gte",
#         #     "tanggal_akhir": "created_at__date__lte",
#         # }

#         per_page = 20

#         # ordering = [
#         #     "-created_at"
#         # ]
        
#     # def get_queryset(self):
#     #     return (
#     #         Pengaduan.objects
#     #         .select_related("pemohon")
#     #     )
    
     