from rest_framework import serializers

# ----- models -----
from pengaduan.models import (
    Pengaduan, RiwayatStatus
)


# ----- rangkuman -----
class PengaduanRangkumanSerializer(serializers.Serializer):
   total_pengaduan = serializers.IntegerField()
   total_menunggu = serializers.IntegerField()
   total_diproses = serializers.IntegerField()
   total_selesai = serializers.IntegerField()
    

# ----- create pengaduan serializer -----
class PengaduanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengaduan
        exclude = ['masyarakat', 'status', 'hasil_klasifikasi']

class PengaduanSerializer(serializers.ModelSerializer):
    foto_bukti = serializers.SerializerMethodField()
    
    class Meta:
        model = Pengaduan
        fields = '__all__'
        
    def get_foto_bukti(self, obj):
        if not obj.foto_bukti:
            return None

        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.foto_bukti.url)

        return obj.foto_bukti.url
    
class RiwayatStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatStatus
        fields = '__all__'
        
class RiwayatStatusResponseSerializer(serializers.Serializer):
    data = RiwayatStatusSerializer(many=True)
    is_success = serializers.BooleanField()
    message = serializers.CharField()
    
    
# ----- riwayat status -----
class TimeLineSerializer(serializers.Serializer):
    status = serializers.CharField()
    keterangan = serializers.CharField()
    pengaduan_id = serializers.IntegerField()
    petugas_id = serializers.IntegerField()
    
class TimeLineRequestSerializer(serializers.Serializer):
    status = serializers.CharField()
    keterangan = serializers.CharField(required=False)
    
class TimeLineResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    is_success = serializers.BooleanField()
    data = RiwayatStatusSerializer()