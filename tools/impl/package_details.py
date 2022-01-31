from dataclasses import dataclass

from impl.os_details import OsDetails


@dataclass
class PackageDetails:
    download_url: str
    os_details: OsDetails
