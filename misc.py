import re

# 定义每小时的费用
COST_PER_HOUR = 10

def calculate_fee(start_time, end_time):
    # 计算总时间（以小时为单位）
    total_hours = (end_time - start_time).seconds / 3600

    # 计算总费用
    total_fee = total_hours * COST_PER_HOUR
    if total_fee <= 1:
        total_fee = 1

    return total_fee

def is_license_plate(str):
    pattern = r"^(([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z](([0-9]{5}[DF])|([DF]([A-HJ-NP-Z0-9])[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳使领]))$"
    return bool(re.match(pattern, str))