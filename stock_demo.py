from matplotlib import pyplot as plt
from scipy import stats
import random
import numpy as np
import math
import pandas as pd

# quota 定额
# quantify 定量

def f_quota(quota, total_money, price_list):
    '''定额买入: 返回买入的股数和天数
    quota: 定额， 例如，每次定量10000元
    total_money: 花费的总金额，不能超过这个数值
    price_list: 价格列表
    '''
    quota_bought = []
    remain_money = total_money
    for p in price_list:
        if remain_money > 0:
            # 计算定额的钱，在当前价格下，能买的股票的数量和花费的钱
            amount = quota // p
            money = p * amount

            if remain_money > money:
                remain_money -= money
            else:
                amount = remain_money // p
                money = p * amount
                remain_money = 0

            quota_bought.append((p, amount, money))
    # 买入的总的股数
    total_amount = sum([i for _, i, _ in quota_bought])
    end_price = quota_bought[-1][0]
    # 买入的天数
    total_day_cnt = len(quota_bought)
    # 花费的总金额
    total_cost_money = sum([i for _, _, i in quota_bought])
    
    return total_amount, total_day_cnt, total_cost_money 


def f_quantify(quantify, total_money, price_list):
    '''定量买入: 返回买入的股数和天数
    quantify: 定量， 例如，每次定量1000股
    total_money: 花费的总金额，不能超过这个数值
    price_list: 价格列表
    '''
    quantify_bought = []
    remain_money = total_money
    for p in price_list:
        if remain_money > 0:
            # 计算每次购买定量，计算购买的总金额
            amount = quantify
            money = p * amount

            if remain_money > money:
                remain_money -= money
            else:
                amount = remain_money // p
                money = p * amount
                remain_money = 0
            quantify_bought.append((p, amount, money))
    # 买入的总的股数
    total_amount = sum([i for _, i, _ in quantify_bought])
    end_price = quantify_bought[-1][0]
    
    # 买入的天数
    total_day_cnt = len(quantify_bought)
    # 花费的总金额
    total_cost_money = sum([i for _, _, i in quantify_bought])
    
    return total_amount, total_day_cnt, total_cost_money

#总金额 100万
total_money = 100 * 10000  
quota = 10000        ## 定额 10000元
quantify = 10 * 100  ## 定量 每次10手

sample_cnt = 10000  

# 模拟股价
rand_data = np.random.random(sample_cnt)
rand_data_ppf = stats.norm.ppf(rand_data, 0, 0.01)
l2 = l1.cumsum()
# 模拟出来的价格列表，作为买入价，要足够用
price_list = 10 * np.exp(l2)

quantify_total_amount, quantify_total_day_cnt, quantify_total_cost_money = f_quantify(quantify, total_money, price_list)
quota_total_amount, quota_total_day_cnt, quota_total_cost_money = f_quota(quota, total_money, price_list)

# 最终卖出的价格 是在这天的价格 max([quantify_total_cnt, quota_total_cnt])
end_price = price_list[max([quantify_total_day_cnt, quota_total_day_cnt])]

quantify_end_money = end_price * quantify_total_amount
quota_end_money = end_price * quota_total_amount

# 收益率 = 最终收入 / 成本 - 1
quantify_rate = quantify_end_money / quantify_total_cost_money - 1
quota_rate = quota_end_money / quota_total_cost_money - 1

#收益率对比
result = quantify_rate - quota_rate
print('定量收益率： %s' %quantify_rate)
print('定额收益率： %s' %quota_rate)

final_relsut_list = []
if result > 0:
    print("Winner: quantify 定量")
elif result < 0:
    print("Winner: quota 定额" )
else:
    print("quantify == quota", quantify_end_money, quota_end_money)

print('-- # 价格波动曲线 # --')
plt.plot(price_list[: max([quantify_total_day_cnt, quota_total_day_cnt])])
plt.ylabel('Price')
plt.xlabel('Day')
plt.show()
