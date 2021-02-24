#! /bin/bash
while (true)
do
    export http_proxy=http://;
    python dataworks.py;
    sleep 5;
done
