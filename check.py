from scan import read
from math import ceil

def diff_count(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    difference = (set1 - set2) | (set2 - set1)
    return len(difference)

def checky(ans, points, choices, img_path):
    assert isinstance(ans, list)
    assert isinstance(points, list) and all(isinstance(i, int) for i in points)
    assert isinstance(choices, list) and all(isinstance(i, int) for i in choices)
    assert isinstance(img_path, str)

    stud_id, stud_ans = read(img_path, len(ans))

    total = 0
    i = 0
    while i < len(ans):
        print(i, total)
        if choices[i] == 1: # single answer
            if len(stud_ans[i]) == 1 and int(ans[i]) == stud_ans[i][0]:
                total += points[i]
            i += 1
        elif choices[i] > 1: # multi answers
            diff = diff_count([int(x) for x in ans[i]], stud_ans[i])
            total += max(0, ceil(points[i] * (1 - diff * 2 / choices[i])))
            i += 1
        else: # linked answer
            real = ''.join(str(x) for x in ans[i:i+(-choices[i])])
            stud = ''.join(str(num) for sublist in stud_ans[i:i+(-choices[i])] for num in sublist)

            # print(real, stud)
            if real == stud:
                total += points[i]
            i += (-choices[i])

    return stud_id, total

def test_works_with_arrays_of_different_lengths():
    assert diff_count([1, 3, 5], [2, 4]) == 5
    assert diff_count([1, 3, 5], [3]) == 2
    assert diff_count([1], [1, 3, 5]) == 2
    assert diff_count([1, 3, 5], [1, 3, 5]) == 0
    assert diff_count([1], [1, 2, 4]) == 2