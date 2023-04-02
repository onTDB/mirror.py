import mirror

from pathlib import Path
import json

DEFAULT_CONFIG = {
    "lastsettingmodified": 111111111,
    "mirrorname": "My Mirror",
    "settings": {
        "logfolder": "/mirror/logs",
        "webroot": "/var/www/mirror",
    },
    "packages": {
        "mirror": {
            "name": "onTDB Mirror",
            "id": "mirror",
            "status": "ACTIVE",
            "timestamp": 11111111,
            "log": "/mirror/logs/mirror.log",
            "href": "/mirror",
            "synctype": "FFTS",
            "syncrate": "PT1H",
            "link": [
                {
                    "rel": "HOME",
                    "href": "http://www.ontdb.com"
                },
                {
                    "rel": "HTTP",
                    "href": "http://mirror.ontdb.com/mirror"
                },
                {
                    "rel": "HTTPS",
                    "href": "https://mirror.ontdb.com/mirror"
                }
            ],
            "settings": {
                "hidden": False,
                "src": "test.org::mirror",
                "dst": "/disk/mirror",
                "fftsfile": "fullfiletimelist-mirror",
            }
        }
    }
}

def load_config(configPath: Path):
    """Load the configuration file"""
    config = json.loads(configPath.read_text())
    mirror.settings = mirror.config.Settings(config)
    

