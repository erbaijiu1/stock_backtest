import numpy as np
import talib as tl
from datetime import datetime, timedelta


# 一根大阳线，包含了前面的9根大阴线。
# 成交量放大。
# 最好是有长期箱体震荡，比如3个月以上的箱体震荡。


# 检查某天的成交量是否比之前的平均成交量大
def check_volume(data, date, threshold=60):
    end_date = date
    start_date = end_date - timedelta(days=threshold)
    data_range = data[
        (data['date'] >= start_date.strftime("%Y-%m-%d")) & (data['date'] <= end_date.strftime("%Y-%m-%d"))]
    if len(data_range) < threshold:
        return False
    avg_volume = data_range['volume'].mean()
    current_volume = data.loc[data['date'] == end_date.strftime("%Y-%m-%d"), 'volume'].values[0]
    return current_volume > avg_volume


def check_box_range(data, period=90):
    # 检查是否在长期箱体震荡
    if len(data) < period:
        return False
    recent_data = data.tail(period)
    max_price = recent_data['close'].max()
    min_price = recent_data['close'].min()
    box_range = max_price - min_price
    if box_range / min_price < 0.1:  # 比如箱体震荡幅度小于10%
        return True
    return False


def one_bull_nine_bears(code_name, data, date=None, threshold=60):
    if date is None:
        end_date = data['date'].iloc[-1]
    else:
        end_date = date.strftime("%Y-%m-%d")

    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask].copy()

    if len(data.index) < threshold:
        return False

    data['ma60'] = tl.MA(data['close'].values, timeperiod=60)
    data['ma60'].values[np.isnan(data['ma60'].values)] = 0.0

    # 检查1阳吃9阴
    if len(data) < 10:
        return False

    for i in range(9, len(data)):
        recent_10_days = data.iloc[i - 9:i + 1]
        if (recent_10_days['close'].values[-1] > recent_10_days['open'].values[-1] * 1.02 and  # 大阳线
                recent_10_days['close'].values[-1] > recent_10_days['high'].values[:-1].max() and  # 包含前9根阴线
                (recent_10_days['close'].values[:-1] < recent_10_days['open'].values[:-1]).all()):  # 前9根都是阴线
            if check_volume(data, datetime.strptime(recent_10_days['date'].values[-1], '%Y-%m-%d'),
                            threshold=threshold):
                if check_box_range(data, period=30):
                    return True

    return False
