from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, filters, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend

# ----- drf -----
from drf_spectacular.utils import extend_schema

# ----- serializers -----
from . import serializers

# ----- models -----
from pengaduan.models import (
    Pengaduan, StatusLaporan, RiwayatStatus
)

# ----- selectors -----
from pengaduan import selectors

# ----- usecase -----
from pengaduan.usecases.lihat_statistik_pengaduan import LihatStatistikPengaduan
from pengaduan.usecases import kelola_timeline

# ----- dto -----
from pengaduan.dtos import TimeLineDTO

# ----- daftar status pengaduan -----
@extend_schema(
    # request=serializers.TimeLineSerializer,
    responses=serializers.RiwayatStatusResponseSerializer,
    tags=["Pengaduan"]
)
class PengaduanDaftarStatusView(APIView):
    
    def get(self, request, pengaduan_id):
        pengaduan = Pengaduan.objects.get(id=pengaduan_id)
        daftar_status = selectors.get_riwayat_status(pengaduan)
        serializer = serializers.RiwayatStatusSerializer(daftar_status, many=True)
        return Response({
            "data": serializer.data,
            "is_success": True,
            "message": "success"
        }, status=status.HTTP_200_OK)

# ----- update status pengaduan -----
@extend_schema(
    request=serializers.TimeLineRequestSerializer,
    responses=serializers.TimeLineResponseSerializer,
    tags=["Pengaduan"]
)
class PengaduanUpdateStatusView(APIView):
    def post(self, request, pengaduan_id, *args, **kwargs):
        pengaduan = Pengaduan.objects.get(id=pengaduan_id)
        petugas = request.user.petugas
        
        data = {
            "pengaduan_id": pengaduan.id,
            "petugas_id": petugas.id,
            "status": request.data.get("status"),
            "keterangan": request.data.get("keterangan")
        }
        
        serializer = serializers.TimeLineSerializer(data=data)
        serializer_valid = serializer.is_valid()
        
        if serializer_valid:
            
            data_clened = serializer.validated_data
            
            # create riwayat status
            obj = kelola_timeline.create_timeline(TimeLineDTO(**data_clened))
            
            return Response({
                "message": "success",
                "is_success": True,
                "data": serializers.RiwayatStatusSerializer(instance=obj).data
            })
        else:
            
            return Response({
                "message": "failed",
                "data": serializer.errors,
                "is_success": False
            }, status=status.HTTP_400_BAD_REQUEST)
        

# ----- rangkuman -----
@extend_schema(
    responses=serializers.PengaduanSerializer,
    tags=["Pengaduan"]
)
class PengaduanRangkumanView(APIView):
    def get(self, request):
        uc = LihatStatistikPengaduan()
        obj = uc.execute(request.user)
        serializer = serializers.PengaduanRangkumanSerializer(obj)
        return Response({
            "message": "success",
            "data": serializer.data,
            "is_success": True
        }, status=status.HTTP_200_OK)

# ----- detail pengaduan -----
@extend_schema(
    responses=serializers.PengaduanSerializer,
    tags=["Pengaduan"]
)
class PengaduanDetailView(APIView):
    def get(self, request, pengaduan_id):
        try:
            pengaduan = Pengaduan.objects.get(id=pengaduan_id)
        except Pengaduan.DoesNotExist:
            return Response({
                "message": "pengaduan not found",
                "is_success": False,
                "data": {}
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = serializers.PengaduanSerializer(pengaduan, context={"request": request})
        return Response({
            "message": "success",
            "data": serializer.data,
            "is_success": True
        }, status=status.HTTP_200_OK)

# ----- create pengaduan -----
@extend_schema(
    responses=serializers.PengaduanSerializer,
    tags=["Pengaduan"]
)
class PengaduanCreateView(generics.CreateAPIView):
    serializer_class = serializers.PengaduanCreateSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        
        # tampilkan print data yang dikirim
        # print(self.request.data)

        if not user.groups.filter(name="masyarakat").exists():
            raise PermissionDenied(
                "Hanya masyarakat yang dapat membuat pengaduan."
            )

        serializer.save(
            masyarakat=user.masyarakat,
            status=StatusLaporan.MENUNGGU
        )
    

@extend_schema(
    responses=serializers.PengaduanSerializer,
    tags=["Pengaduan"]
)
class PengaduanListView(ListAPIView):
    # queryset = Pengaduan.objects.all()
    serializer_class = serializers.PengaduanSerializer
    
    def get_queryset(self):
        user = self.request.user
        qs = Pengaduan.objects.select_related(
            "masyarakat"
        )
        
        groups = set(user.groups.values_list("name", flat=True))

        if "masyarakat" in groups:
            return qs.filter(masyarakat=user.masyarakat)

        if "petugas" in groups:
            return qs

        return qs.none()
    
    # ----- ini manual, bisa di set default di settings.py -----
    # filter_backends = [
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter
    # ]
    
    filterset_fields = [
        'status',
        'tanggal_pengaduan',
        'kategori'
    ]
    
    search_fields = [
        'status',
        'tanggal_pengaduan',
        'judul'
    ]
    
    ordering_fields = [
        'status',
        'tanggal_pengaduan'
    ]
    ordering = ['-tanggal_pengaduan']

@extend_schema(
    responses=serializers.PengaduanSerializer,
    tags=["Pengaduan"]
)
class PengaduanView(APIView):
    # parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request) -> Response:
        qs = Pengaduan.objects.all()
        serializer = serializers.PengaduanSerializer(qs, many=True)
        return Response({
            "message": "success",
            "data": serializer.data,
            "is_success": True
            
        }, status=status.HTTP_200_OK)
        
    @extend_schema(
        summary="Tambah pengaduan",
        request=serializers.PengaduanSerializer,
        responses={
            201: serializers.PengaduanSerializer,
            400: serializers.PengaduanSerializer,
        },
    )
    def post(self, request):
        serializer = serializers.PengaduanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "success",
                "data": serializer.data,
                "is_success": True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "failed",
                "data": serializer.errors,
                "is_success": False
            }, status=status.HTTP_400_BAD_REQUEST)