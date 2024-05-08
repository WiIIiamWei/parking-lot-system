import re

# 定义每小时的费用
COST_PER_HOUR = 10

def calculate_fee(start_time, end_time, is_vip=False):
    duration = end_time - start_time
    if duration.total_seconds() < 3600:  # 停车时间少于一小时
        fee = 5
    else:
        fee = duration.total_seconds() / 3600 * 5  # 每小时收费 5 元
    if is_vip:
        fee *= 0.8  # VIP 打 8 折
    return round(fee)


def is_license_plate(str):
    pattern = r"^(([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z](([0-9]{5}[DF])|([DF]([A-HJ-NP-Z0-9])[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳使领]))$"
    return bool(re.match(pattern, str))



