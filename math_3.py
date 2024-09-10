import random
from itertools import product

# 需要再装配的逻辑
# 生成决策向量
arrays = list(product([0, 1], repeat=16))
# 第0~7个决定零配件检测
# 第8~10决定半成品是否检测
# 第11决定成品是否检测
# 第12~14决定半成品是否拆解
# 第15决定成品是否拆解

# 模拟零配件个数
num = 500
money = 0
type1 = 8
type2 = 3

N = [0 for _ in range(type1)]  # 零配件个数
part1 = [-1 for _ in range(type1)]  # 8种零配件合格
part2 = [-1 for _ in range(type2)]  # 3种半成品-1，0,1分别表示无，次品，合格品
product = -1  # 成品 -1，0,1分别表示无，次品，合格品
# 情况一
p1 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
p2 = [0.1, 0.1, 0.1]
P = [0.1]
part_cost = [2, 8, 12, 2, 8, 12,8,12]  # 半成品i所需零件成本
test_part_cost = [1, 1, 2,1, 1, 2,1, 2]  # 检测零件i所需成本
test_half_product_cost = [4, 4, 6]  # 检测半成品i所需成本
test_product_cost = 3  # 检测成品成本
half_mounting_cost = [8, 8, 8]  # 半成品i装配成本
mounting_cost = 8  # 成品装配成本
sale_price = 200  # 市场售价
change_cost = 40  # 调换损失
fix_cost = [6, 6, 6]  # 半成品i拆解费用
fix = 10  # 成品拆解费用
NUM = 0
#生成零配件i
def generate_parts(i):
    global money,part1,N
    money -= part_cost[i]
    N[i] -= 1
    part1[i] = 1 if random.random() >= p1[i] else 0

# 检测零配件i
def inspect_part(i):
    global money,part1
    money -= test_part_cost[i]
    if part1[i] == 0:  # 如果他是次品就丢掉
        part1[i] = -1
        return False
    return True

# 装配半成品1
def assemble_product1():
    global money
    money -= half_mounting_cost[0]
    for i in range(3):
        if part1[i] != 1:
            return 0
    return 1 if random.random() >= p2[0] else 0
#装配半成品2
def assemble_product2():
    global money
    money -= half_mounting_cost[1]
    for i in [3,4,5]:
        if part1[i] != 1:
            return 0
    return 1 if random.random() >= p2[1] else 0
#装配半成品3
def assemble_product3():
    global money
    money -= half_mounting_cost[2]
    for i in [6,7]:
        if part1[i] != 1:
            return 0
    return 1 if random.random() >= p2[2] else 0

#检测半成品
def inspect_half_product(i):
    global money
    money -= test_half_product_cost[i]
    if part2[i] == 0:
        return False  # 不合格成品
    return True  # 合格品
#装配成品
def assemble_product():
    global money
    money -= mounting_cost
    for i in range(type2):
        if part2[i] != 1:
            return 0
    return 1 if random.random() >= P[0] else 0
#检测成品
def inspect_product():
    global money
    money -= test_product_cost
    if product == 0:
        return False  # 不合格成品
    return True  # 合格


# 售出商品
def sell_product():
    global money,NUM
    global product
    money += sale_price
    product = -1
    NUM += 1


# 模拟调换逻辑
def handle_customer_return():
    global money
    money -= change_cost

#拆解半成品1
def disassemble_product1():
    global money
    money -= fix_cost[0]
    for i in range(3):
        money += part_cost[0]
        N[i] += 1
#拆解半成品2
def disassemble_product2():
    global money
    money -= fix_cost[1]
    for i in [3,4,5]:
        money += part_cost[1]
        N[i] += 1
#拆解半成品3
def disassemble_product3():
    global money
    money -= fix_cost[2]
    for i in [6,7]:
        money += part_cost[2]
        N[i] += 1
#拆解成品
def disassemble_product():
    global money
    money -= fix



def process_cycle():
    # 成本和收入
    global num, N, money, product,NUM
    max_value = float('-inf')  # 初始化最大值为负无穷
    best_array = None  # 初始化最佳决策向量
    for array in arrays:  # 对每一种决策
        N = [num for _ in range(type1)]
        money = 0
        flag = 0
        NUM = 0
        while True:
            #保证还有零件
            if any(n <= 0 for n in N):
                current_value = (money - flag * sale_price) / NUM
                if current_value > max_value:
                    max_value = current_value
                    best_array = array
                print(current_value,array)
                break
            #开始生产
            while True:
                # 得到半成品1
                while True:
                    #生产可用的零件1
                    while True:
                        generate_parts(0)
                        if array[0] == 1:  # 检验
                            inspect_part(0)  # 要么无，要么是合格品
                            if part1[0] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    #生产可用的零件2
                    while True:
                        generate_parts(1)
                        if array[1] == 1:  # 检验
                            inspect_part(1)  # 要么无，要么是合格品
                            if part1[1] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    #生产可用的零件3
                    while True:
                        generate_parts(2)
                        if array[2] == 1:  # 检验
                            inspect_part(2)  # 要么无，要么是合格品
                            if part1[2] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    part2[0] = assemble_product1()
                    if array[8] == 1:  # 检验
                        if not inspect_half_product(0):  # 要么无，要么是合格品
                            if array[12] == 1:
                                disassemble_product1()
                            else: #不拆解
                                break
                        else:
                            break
                    else:
                        break

                # 得到半成品2
                while True:
                    #生产可用的零件4
                    while True:
                        generate_parts(3)
                        if array[3] == 1:  # 检验
                            inspect_part(3)  # 要么无，要么是合格品
                            if part1[3] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    #生产可用的零件5
                    while True:
                        generate_parts(4)
                        if array[4] == 1:  # 检验
                            inspect_part(4)  # 要么无，要么是合格品
                            if part1[4] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    #生产可用的零件6
                    while True:
                        generate_parts(5)
                        if array[5] == 1:  # 检验
                            inspect_part(5)  # 要么无，要么是合格品
                            if part1[5] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    part2[1] =assemble_product2()
                    if array[9] == 1:  # 检验
                        if not inspect_half_product(1):  # 要么无，要么是合格品
                            if array[13] == 1: #拆解
                                disassemble_product1()
                            else: #不拆解
                                break
                        else:
                            break
                    else:
                        break
                # 得到半成品3
                while True:
                    #生产可用的零件7
                    while True:
                        generate_parts(6)
                        if array[6] == 1:  # 检验
                            inspect_part(6)  # 要么无，要么是合格品
                            if part1[6] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    #生产可用的零件8
                    while True:
                        generate_parts(7)
                        if array[7] == 1:  # 检验
                            inspect_part(7)  # 要么无，要么是合格品
                            if part1[7] == 1:  # 如果是合格品就可以跳出，否则重新生产零配件
                                break
                            else:
                                continue
                        else:
                            break  # 不检验
                    part2[2] = assemble_product3()
                    if array[10] == 1:  # 检验
                        if not inspect_half_product(2):  # 要么无，要么是合格品
                            if array[14] == 1:
                                disassemble_product1()
                            else: #不拆解
                                break
                        else:
                            break
                    else:
                        break
                #装配成品
                product = assemble_product()
                if array[11] == 1:  # 检测成品
                    if not inspect_product():  # 为次品
                        if array[15] == 1:  # 要拆解的话
                            disassemble_product()
                            disassemble_product1()
                            disassemble_product2()
                            disassemble_product3()
                        product = -1
                        break
                    else:  # 检测为合格品
                        sell_product()
                        break
                else:  # 没检测
                    if product == 1:
                        sell_product()
                        break
                    else:
                        handle_customer_return()
                        flag += 1
                        if array[15] == 1:  # 要拆解的话
                            disassemble_product()
                            disassemble_product1()
                            disassemble_product2()
                            disassemble_product3()
                        product = -1
                        break
    print(f"最佳决策向量: {best_array}")
    print(f"最大收益值: {max_value}")


process_cycle()

