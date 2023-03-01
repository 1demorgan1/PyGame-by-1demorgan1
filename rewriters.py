all_nums = []
for i in range(int(input())):
    all_nums.append(input().split())
for i in all_nums:
    if abs(int(i[0])) != abs(int(i[1])) --and abs(int(i[0])) > abs(int(i[1])):
        print(f'({i[0]}, {i[1]})')

min_1, max_2, min_3, max_4 = [min(all_nums, key=lambda x: int(x[0])), max(all_nums, key=lambda x: int(x[0])),
                              min(all_nums, key=lambda x: int(x[1])), max(all_nums, key=lambda x: int(x[1]))]
print(f'left: ({min_1[0]}, {min_1[-1]})')
print(f'right: ({max_2[0]}, {max_2[-1]})')
print(f'top: ({max_4[0]}, {max_4[-1]})')
print(f'bottom: ({min_3[0]}, {min_3[-1]})')