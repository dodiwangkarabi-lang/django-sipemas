# ----- service -----
from pengaduan.services.timeline import TimeLineService

# ----- dto -----
from pengaduan.dtos import TimeLineDTO

def update_timeline(timeline: TimeLineDTO):
    return TimeLineService.update_or_create(timeline)

def create_timeline(timeline: TimeLineDTO):
    return TimeLineService.create(timeline)