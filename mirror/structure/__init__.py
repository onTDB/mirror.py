import mirror

from pathlib import Path
import json
import time
import re

class INP:
    keys: list[str]
    def __init__(self, inp: dict) -> None:
        self.keys = inp.keys()
        for key in inp:
            setattr(self, key, inp[key])

    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.keys}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

class Package:
    class InSettings(INP):
        hidden: bool
        src: str
        dst: str

    class Link(INP):
        rel: str
        href: str

    pkgid: str
    name: str
    status: str
    timestamp: int
    log: Path
    href: str
    synctype: str
    syncrate: str
    link: list[Link]
    settings: InSettings

    def __init__(self, config: dict) -> None:
        self.pkgid = config["id"]
        self.name = config["name"]
        self.status = config["status"]
        self.timestamp = config["timestamp"]
        self._path_check(Path(config["log"]))
        self.log = config["log"]
        self.href = config["href"]
        if config["sync"] in mirror.sync.types:
            self.synctype = config["sync"]
        else:
            raise ValueError(f"Sync type not in {mirror.sync.types}")
        self.syncrate = config["syncrate"]
        self.link = []
        for link in config["link"]:
            self.link.append(self.Link(link))
        self.settings = self.InSettings(config["settings"])
        #self.original = config
    
    def __str__(self) -> str:
        return self.id

    def set_status(self, status) -> None:
        statuslist = ["ACTIVE", "ERROR", "SYNC", "UNKNOWN"]
        if status in statuslist:
            self.status = status
            self.timestamp = time.time() * 1000
        else:
            raise ValueError(f"Status not in {statuslist}")
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.pkgid,
            "status": self.status,
            "timestamp": self.timestamp,
            "log": self.log,
            "href": self.href,
            "synctype": self.synctype,
            "syncrate": self.syncrate,
            "link": [link.to_dict() for link in self.link],
            "settings": self.settings.to_dict()
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())


    def _path_check(self, path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")
    
    def _iso8601_parser(duration_str): # ISO 8601 Parser
        match = re.match(
            r'P((?P<years>\d+)Y)?((?P<months>\d+)M)?((?P<weeks>\d+)W)?((?P<days>\d+)D)?(T((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?)?',
            duration_str
        ).groupdict()
        return int(match['years'] or 0)*365*24*3600 + \
            int(match['months'] or 0)*30*24*3600 + \
            int(match['weeks'] or 0)*7*24*3600 + \
            int(match['days'] or 0)*24*3600 + \
            int(match['hours'] or 0)*3600 + \
            int(match['minutes'] or 0)*60 + \
            int(match['seconds'] or 0)
    
    def _iso8601_maker(duration):
        if duration < 0:
            raise ValueError("Duration must be a positive integer.")
        dates = [365*24*3600, 30*24*3600, 7*24*3600, 24*3600, 3600, 60, 1]
        names = ["Y", "M", "W", "D", "H", "M", "S"]
        iso8601 = "P"
        for i in range(len(dates)):
            if names[i] == "D": iso8601 += "T"
            if duration >= dates[i]:
                iso8601 += f"{duration // dates[i]}{names[i]}"
                duration %= dates[i]
        return iso8601

class Config:
    class InPackage(INP):
        def to_dict(self) -> dict:
            return {key: getattr(self, key).to_dict() for key in self.keys}

    name: str
    lastsettingmodified: int
    packages: InPackage

    logfolder: Path
    webroot: Path

    def __init__(self, config: dict) -> None:
        self.name = config["mirrorname"]
        self.lastsettingmodified = config["lastsettingmodified"]
        self.packages = self.InPackage(config["packages"])

        self._path_check(Path(config["settings"]["logfolder"]))
        self._path_check(Path(config["settings"]["webroot"]))
        self.logfolder = Path(config["settings"]["logfolder"])
        self.webroot = Path(config["settings"]["webroot"])

    def _path_check(self, path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")
        if not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory")

    def to_dict(self) -> dict:
        return {
            "mirrorname": self.name,
            "lastsettingmodified": self.lastsettingmodified,
            "packages": self.packages.to_dict(),
            "settings": {
                "logfolder": self.logfolder,
                "webroot": self.webroot
            }
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    def save(self) -> None:
        mirror.configPath.write_text(self.to_json())