import mirror

import json

class Package:
    pkgid: str
    name: str
    status: str
    timestamp: int
    log: str
    href: str
    synctype: str
    link: list[dict]

    def __init__(self, config: dict) -> None:
        self.pkgid = config["id"]
        self.name = config["name"]
        self.status = config["status"]
        self.timestamp = config["timestamp"]
        self.log = config["log"]
        self.href = config["href"]
        if config["sync"] in mirror.sync.types:
            self.synctype = config["sync"]
        else:
            raise ValueError(f"Sync type not in {mirror.sync.types}")
        self.link = []
        self.originconfig = config
    
    def __str__(self) -> str:
        return self.id

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.pkgid,
            "status": self.status,
            "timestamp": self.timestamp,
            "log": self.log,
            "href": self.href,
            "synctype": self.synctype,
            "link": self.link
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def setstatus(self, status) -> None:
        statuslist = ["ACTIVE", "ERROR", "SYNC", "UNKNOWN"]
        if status in statuslist:
            self.status = status
        else:
            raise ValueError(f"Status not in {statuslist}")

class FFTS:
    def __init__(self, config: dict) -> None:
        self.file = config["fftsfile"]
        self.src = config["src"]
        self.dst = config["dst"]