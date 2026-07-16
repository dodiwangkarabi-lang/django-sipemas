
from pengaduan.models import StatusLaporan
from enum import Enum, StrEnum
# dto dataclasses
from dataclasses import dataclass

@dataclass
class TimeLineDTO:
    status: str
    pengaduan_id: int
    petugas_id: int
    status: StatusLaporan
    keterangan: str | None