#!/bin/sh

source /root/.bashrc
cd /root/server_release/stock_backtest/cron;

# 设置日志文件路径
LOG_FILE="./cron_job.log"

# 设置执行时间
EXECUTE_TIME=$(date +"%Y-%m-%d %H:%M:%S")

echo "[$EXECUTE_TIME] Starting daily job execution..." >> $LOG_FILE
# conda init
conda activate stock_backtest_310
python ../instock/job/execute_daily_job.py >> $LOG_FILE 2>&1
echo "[$EXECUTE_TIME] Daily job execution completed." >> $LOG_FILE
