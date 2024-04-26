#!/bin/sh

source /root/.bashrc
conda activate stock_backtest_310;

cd /root/server_release/stock_backtest/cron;
#/usr/local/bin/python3 /data/InStock/instock/job/basic_data_daily_job.py
python ../instock/job/basic_data_daily_job.py
#mkdir -p /data/logs
#DATE=`date +%Y-%m-%d:%H:%M:%S`
#echo $DATE >> /data/logs/hourly.log