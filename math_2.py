import random
from itertools import product

# 生成决策向量
arrays = list(product([0, 1], repeat=4))

# 模拟零配件个数
num = 1000000
money = 0
type = 2
product = -1
N = [0 for _ in range(type)]
part = [-1 for _ in range(type)]  # -1，0,1分别表示无，次品，合格品
A = 0
# 情况一
# p=[0.1,0.1]
# P =[0.1]
# part_cost = (4, 18)  # 零配件购买单价
# test_part_cost = (2, 3)  # 零配件检测成本
# test_product_cost = 3  # 成品检测成本
# mounting_cost = 6  # 装配成本
# sale_price = 56  # 市场售价
# change_cost = 6  # 调换损失
# fix_cost = 5  # 拆解费用
# 情况二
p = [0.2, 0.2]
P = [0.2]
part_cost = (4, 18)  # 零配件购买单价
test_part_cost = (2, 3)  # 零配件检测成本
test_product_cost = 3  # 成品检测成本
mounting_cost = 6  # 装配成本
sale_price = 56  # 市场售价
change_cost = 6  # 调换损失
fix_cost = 5  # 拆解费用
# 情况三
# p = [0.1, 0.1]
# P = [0.1]
# part_cost = (4, 18)  # 零配件购买单价
# test_part_cost = (2, 3)  # 零配件检测成本
# test_product_cost = 3  # 成品检测成本
# mounting_cost = 6  # 装配成本
# sale_price = 56  # 市场售价
# change_cost = 30  # 调换损失
# fix_cost = 5  # 拆解费用
#情况四
# p = [0.2, 0.2]
# P = [0.2]
# part_cost = (4, 18)  # 零配件购买单价
# test_part_cost = (1, 1)  # 零配件检测成本
# test_product_cost = 2  # 成品检测成本
# mounting_cost = 6  # 装配成本
# sale_price = 56  # 市场售价
# change_cost = 30  # 调换损失
# fix_cost = 5  # 拆解费用

#情况五
# p = [0.1, 0.2]
# P = [0.1]
# part_cost = (4, 18)  # 零配件购买单价
# test_part_cost = (8, 1)  # 零配件检测成本
# test_product_cost = 2  # 成品检测成本
# mounting_cost = 6  # 装配成本
# sale_price = 56  # 市场售价
# change_cost = 10  # 调换损失
# fix_cost = 5  # 拆解费用

#情况六
# p = [0.05, 0.05]
# P = [0.05]
# part_cost = (4, 18)  # 零配件购买单价
# test_part_cost = (2, 3)  # 零配件检测成本
# test_product_cost = 3  # 成品检测成本
# mounting_cost = 6  # 装配成本
# sale_price = 56  # 市场售价
# change_cost = 10  # 调换损失
# fix_cost = 40  # 拆解费用

# 模拟零配件的生成
def generate_parts(i):
    global money
    money -= part_cost[i]
    N[i] -= 1
    part[i] = 1 if random.random() >= p[i] else 0


# 检测零配件

def inspect_part(i):
    global money
    money -= test_part_cost[i]
    if part[i] == 0:  # 如果他是次品就丢掉
        part[i] = -1


# 装配
def assemble_product():
    global money
    money -= mounting_cost
    for i in range(type):
        if part[i] != 1:
            return 0
    return 1 if random.random() >= P[0] else 0


# 检测成品
def inspect_product():
    global money, product
    money -= test_product_cost
    if product == 0:
        return False  # 不合格成品
    return True  # 合格


# 售出商品
def sell_product():
    global money
    global product
    global A
    A += 1
    money += sale_price
    product = -1


# 拆解
def disassemble_product():
    global money
    money -= fix_cost
    for i in range(type):
        money += part_cost[i]
        N[i] += 1


# 模拟调换逻辑
def handle_customer_return():
    global money
    money -= change_cost


# 主函数，模拟整个流程并计算损益
def process_cycle():
    # 成本和收入
    global num, N, money, product,A

    max_value = float('-inf')  # 初始化最大值为负无穷
    best_array = None  # 初始化最佳决策向量

    for array in arrays:  # 对每一种决策
        N = [num for _ in range(type)]
        money = 0
        flag = 0
        A = 0
        while True:
            # 保证还有零件
            if any(n == 0 for n in N):
                current_value = ((money - flag * sale_price)/(A))
                print(current_value,array)
                break
            # 开始生产
            # 产生零配件
            for j in range(type):
                while True:
                    generate_parts(j)
                    # 是否检验
                    if array[j] == 1:  # 检验
                        inspect_part(j)  # 要么无，要么是合格品
                        if part[j] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                            break
                    else:
                        break  # 不检验
            # 装配
            product = assemble_product()
            # 装配检测
            if array[type] == 1:  # 检测了
                if not inspect_product():  # 为次品
                    if array[type + 1] == 1:  # 要拆解的话
                        disassemble_product()
                    product = -1
                else:  # 检测为合格品
                    sell_product()
            else:  # 没检测
                if product == 1:
                    sell_product()
                else:
                    sell_product()
                    handle_customer_return()
                    flag += 1
                    if array[type + 1] == 1:  # 要拆解的话
                        disassemble_product()
                    product = -1

if __name__ == "__main__":
    process_cycle()
