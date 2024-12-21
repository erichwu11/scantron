from scan import read
from math import ceil

def diff_count(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    difference = (set1 - set2) | (set2 - set1)
    return len(difference)

def checky(ans, points, choices, img_path, have = 0):
    # assert isinstance(img_path, str)
    stud_id = 0
    stud_ans = []

    # first time auto-read, if doesn't fit answer format, return error
    if have == 0:
        temp_out = read(img_path, len(ans))
        # Return if error from read
        if type(temp_out) == str:
            return "From read(): " + temp_out
        stud_id, stud_ans = temp_out
    # means manual checked
    else:
        stud_id = img_path[0]
        stud_ans = img_path[1:]
        if len(stud_ans) != len(ans):
            return f"incorrect length for answers"

    total = 0
    i = 0
    while i < len(ans):
        # print(i + 1, total)
        if choices[i] == 1: # single answer
            if len(stud_ans[i]) == 1 and stud_ans[i][0] in ans[i]: # if only picked single, and belongs in answers
                total += points[i]
            elif len(stud_ans[i]) != 1 and have == 0: # maybe scanned wrongly?
                return f"Scan error: Column: {i}, Type: Single, Scanned: {' '.join(map(str, stud_ans[i]))}"
            i += 1
        elif choices[i] > 1: # multi answers
            if len(stud_ans[i]) > 0: # making sure if it is filled in
                # diff = diff_count([int(x) for x in ans[i]], stud_ans[i])
                diff = choices[i] # starting from max, which is all the choices wrong
                if max(stud_ans[i]) >= choices[i] and have == 0:
                    return f"Scan error: Column: {i}, Type: Multi, Scanned: {stud_ans[i]}"
                for sets in ans[i]:
                    diff = min(diff, diff_count([int(x) for x in sets], stud_ans[i])) # find which set of answer have the lowest diff
                total += max(0, ceil(points[i] * (1 - diff * 2 / choices[i])))
            elif have == 0:
                return f"Scan error: Column: {i}, Type: Multi, Scanned: {' '.join(map(str, stud_ans[i]))}"
            i += 1
        else: # linked answer
            if any(len(x) != 1 for x in stud_ans[i:i + (-choices[i])]) and have == 0:
                return f"Scan error: Column: {i}, Type: Linked, Scanned: {stud_ans[i:i + (-choices[i])]}"
            stud = ''.join(str(num) for sublist in stud_ans[i:i + (-choices[i])] for num in sublist)

            # print(real, stud)
            if stud in ans[i]:
                total += points[i]
            i += (-choices[i])

    return total, stud_id, stud_ans

# def test_works_with_arrays_of_different_lengths():
#     assert diff_count([1, 3, 5], [2, 4]) == 5
#     assert diff_count([1, 3, 5], [3]) == 2
#     assert diff_count([1], [1, 3, 5]) == 2
#     assert diff_count([1, 3, 5], [1, 3, 5]) == 0
#     assert diff_count([1], [1, 2, 4]) == 2