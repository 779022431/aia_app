#! /bin/bash
(python -W ignore polardb_monitor.py) &
(python -W ignore polardb_slow_sql.py) &
(python -W ignore polardb_disk.py) &