#!/bin/sh
conda activate stock_backtest_310;
#/usr/local/bin/python3 /data/InStock/instock/job/basic_data_daily_job.py
python ../instock/job/basic_data_daily_job.py
#mkdir -p /data/logs
#DATE=`date +%Y-%m-%d:%H:%M:%S`
#echo $DATE >> /data/logs/hourly.log