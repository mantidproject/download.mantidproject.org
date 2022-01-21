import datetime
from dataclasses import dataclass
from typing import List, Optional

from impl.package_details import PackageDetails


@dataclass
class ReleaseInfo:
    date: datetime.date
    version: str
    package_details: List[PackageDetails]
    formatted_version: Optional[str] = None
    release_notes_url: Optional[str] = None
