#! /bin/bash
(python -W ignore rds_monitor.py) &
(python -W ignore rds_slow_sql.py) &