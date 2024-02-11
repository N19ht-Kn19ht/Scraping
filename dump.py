import gzip
import subprocess
from pathlib import Path
import os


def backup_database(host, username, password, database, dump_folder, dt):

    print("PostgreSQL database dump started")

    # Ensure that the dump folder exists
    dump_folder = Path(dump_folder)
    dump_folder.mkdir(parents=True, exist_ok=True)

    f_name = 'backup ' + dt + '.gz'

    # Create the backup file
    backup_file = dump_folder / f_name

    # Create the command
    command = [
        'pg_dump',
        '-h', host,
        '-U', username,
        '-d', database,
    ]

    os.environ['PGPASSWORD'] = password

    with gzip.open(backup_file, 'wb') as f:
        subprocess.run(command, stdout=f, check=True)

    print("[INFO] PostgreSQL database dump complete")

    return
