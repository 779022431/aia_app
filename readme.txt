把此文件复制到systemd目录下: 
cp /home/test.service /etc/systemd/system/
启动: systemctl start test.service
 systemctl stop test.service
 systemctl status test.service


[rds]
domain = https://rds.aliyuncs.com
regions = cn-shanghai,cn-shenzhen,cn-hangzhou
version = 2014-08-15
pageSize = 50
rdsListFile = rds_list.txt
rdsSlowSqlFile = rds_slow_sql.txt
rdsCpuFile = rds_cpu.txt
rdsMemoryFile = rds_memory.txt
rdsDiskFile = rds_disk.txt
slowSqlTime = 1

[polardb]
domain = polardb.aliyuncs.com
version = 2017-08-01
pageSize = 50
polardbListFile = polardb_list.txt
polardbSlowSqlFile = polardb_slow_sql.txt
polardbCpuFile = polardb_cpu.txt
polardbMemoryFile = polardb_memory.txt
polardbDiskFile = polardb_disk.txt
slowSqlTime = 1