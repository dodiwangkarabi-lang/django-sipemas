from collections import Counter

# models
from academics.models import (
    Siswa
)

class StatistikService:
    def __init__(self):
        pass
    
    def statistik_siswa(self):
        # semua siswa
        daftar_siswa = Siswa.objects.all()

        map_hasil_prediksi = {}
        for siswa in daftar_siswa:
            if siswa.has_prediksi_prestasi:
                map_hasil_prediksi[siswa.id] = siswa.prediksi_prestasi.hasil_prediksi
            else:
                map_hasil_prediksi[siswa.id] = "BELUM_DIKETAHUI"
                
        values = list(map_hasil_prediksi.values())

        valid = [v for v in values if v is not None]
        missing = values.count(None)
        counter = Counter(valid)

        total = sum(counter.values())

        hasil = {
            k: {
                "jumlah": v,
                "persentase": round((v / total) * 100, 2)
            }
            for k, v in counter.items()
        }
        
        
        
        data = {
            "total_siswa": Siswa.objects.count(),
            "statistik_prediksi": hasil
        }
        return data
    
    