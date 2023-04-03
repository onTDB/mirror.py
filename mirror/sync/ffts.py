import mirror

from time import sleep
import subprocess

def ffts(package: mirror.structure.Package):
    """Sync package to mirror"""
    if check(package.settings.fftsfile, package.settings.src, package.settings.path, package.settings.dst): # If FFTS file is out of date
        command = [
            "rsync",
            "-vrlptDSH",
            "--exclude=\"*.~tmp~\"",
            "--delete-delay",
            "--delay-updates",
            f'"{package.settings.src}/{package.settings.ffts_file}"',  
            f'"{package.settings.dst}/{package.settings.ffts_file}"',
        ]

        command = " ".join(command)
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            package.setstatus("ACTIVE")
        else:
            package.setstatus("ERROR")

def check(fftsfile: str, src: str, srcpath: str, dst: str) -> bool:
    """Check if the mirror is up to date"""
    command = [
        "rsync",
        "--no-motd",
        "--dry-run",
        "--out-format=\"%n\"",
        f'"{src}::{srcpath}/{fftsfile}"',
        f'"{dst}/{fftsfile}"',
    ]

    command = " ".join(command)
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.stdout == b'':
        return False # Don't need to sync
    else:
        return True
