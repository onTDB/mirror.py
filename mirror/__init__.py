import mirror.logger
import mirror.command
import mirror.config
import mirror.structure
import mirror.sync
import mirror.socket

from pathlib import Path
import logging

conf: mirror.config.Config = None
confPath: Path = None