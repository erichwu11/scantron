from scan import read_csv
import pandas as pd
from math import ceil
import csv

file_path = './output.csv'
store_path = './changed.csv'

def diff_count(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    difference = (set1 - set2) | (set2 - set1)
    return len(difference)

ans, choices, points, _ = read_csv("exam1_ans.csv")

data = pd.read_csv(file_path, dtype=str)
new_data = []
wronged = 0

print(ans)
print(choices)
print(points)

headers = data.columns.values.tolist()

for index, row in data.iterrows():
    stud_count = 0
    ans_count = 0
    total = 0
    row = row.tolist()
    new_arr = [row[0]]
    file_name = row[2]
    stud_ans = row[3:]

    while ans_count < len(choices):
        if type(stud_ans[stud_count]) != str:
            stud_ans[stud_count] = ""

        if choices[ans_count] == 1:
            if len(stud_ans[stud_count]) == 1 and int(stud_ans[stud_count]) in ans[ans_count]:
                total += points[ans_count]
            stud_count += 1
            ans_count += 1
        elif choices[ans_count] > 0:
            cur_ans = [int(x) for x in stud_ans[stud_count]]
            if len(cur_ans) > 0 and max(cur_ans) < choices[ans_count]:
                diff = choices[ans_count]
                for sets in ans[ans_count]:
                    diff = min(diff, diff_count([int(x) for x in sets], cur_ans))
                total += max(0, ceil(points[ans_count] * (1 - diff * 2 / choices[ans_count])))
            stud_count += 1
            ans_count += 1
        else:
            if stud_ans[stud_count] in ans[ans_count]:
                total += points[ans_count]
            stud_count += 1
            ans_count -= choices[ans_count]

    if total != int(row[1]):
        print(row[0], f"new:{total} - old:{int(row[1])} = {total - int(row[1])}")
        wronged += 1
    new_arr.append(total)
    new_arr.append(file_name)
    new_data.append(new_arr + stud_ans)

print("Total changed:", wronged)
with open(store_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    writer.writerows(new_data)