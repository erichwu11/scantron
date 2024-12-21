from check import checky
from scan import read, read_csv
import os
import csv
import cv2
# read function returns two values
# student_id: a string, 9 digits, if drawn any other value other than 1 on first column will be changed to 'x'
# student_ans: a list, with each elements being lists(in case of multiple choices on same answer)
# for multiple answers questions, each wrong option will cause 2/n of the question, no below 0, and ceil(). n has to be written in array 'choices'
# for single answer questions, either all points or no points. Write 1 in 'choices'
# for linked question(need more than one column) write negative column number you need on first col, and 0 for rest in 'choices. All or 0 points\
#   Example you need 3 columns to linked together, and the question is 10 points. [-3, 0, 0] in 'choices', and [10, 0, 0] in 'points'

# todo:
# 1O change error files to easier read and type
# 2O add to_know
# 3O clearer error messages
# 4. rewrite readme
# 5. write comments in code

def main():
    dir_path = "./three/" # the folder of all photos
    ans_path = "./exam3_ans.csv" # format of answers should be in readme
    out_path = "./output.csv"
    save = 0 # 0 for no save, 1 for save
    to_know = ['109021115'] # to know which files they are

    # read out answers
    ans, choices, points, _ = read_csv(ans_path)

    files = os.listdir(dir_path)
    # files = ['20241210114401-0058.jpg']

    # csv part
    data = []
    out_to_know = []
    heads = ['id', 'score', 'file']
    i = 1
    for a in points:
        if a > 0:
            heads.append(i)
            i += 1
    
    for file in files:
        if file[-4:] != '.jpg':
            print(file, "not .jpg, skipped")
            continue
        
        # scan[read()] and check[checky()] student answers
        cur = checky(ans, points, choices, dir_path + file)

        # if output is error
        if type(cur) is str:
            print(file, cur)

            # manually check
            while 1:
                # show image
                # todo: not sure how to show the image while accepting input
                img = cv2.imread(dir_path + file)
                new_size = (int(img.shape[1] * 0.3), int(img.shape[0] * 0.3))
                cv2.imshow(file, cv2.resize(img, new_size))
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                print("key in id and what they put for \"each column\", seperated by space, ex. 109062323 1 012 3 2")
                zzr = input("-1 to force exit, -2 to see again")
                if zzr == "-1":
                    break
                elif zzr == "-2":
                    continue

                zzr = zzr.split()
                # zzr = [list(map(int, element)) for element in zzr

                # convert to int, then id to string, along with adding x
                for i in range(len(zzr)):
                    lol = []
                    for j in zzr[i]:
                        if j in '0123456789':
                            lol.append(int(j))
                    zzr[i] = lol
                zzr[0] = [str(x) for x in zzr[0]]
                if zzr[0][0] != '1':
                    zzr[0][0] = 'x'
                zzr[0] = ''.join(zzr[0])
                print(zzr)

                # check, but forcing incorrect type of answers
                cur = checky(ans, points, choices, zzr, 1)

                # if error, retry
                if type(cur) == str:
                    print(cur)
                    continue

                # translate to output form
                ddd = [cur[1], str(cur[0]), file]
                
                if cur[1] in to_know:
                    out_to_know.append(file)

                i = 0
                while i < len(cur[2]):
                    # if its single or multi, append, else concatenate the linked questions
                    if choices[i] > 0:
                        ddd.append(''.join(map(str, cur[2][i])))
                        i += 1
                    else:
                        ddd.append(''.join(str(num) for sublist in cur[2][i:i+(-choices[i])] for num in sublist))
                        i -= choices[i]   

                data.append(ddd)
                print(ddd)

                break

            continue

        # translate to output form
        ddd = [cur[1], str(cur[0]), file]
        if cur[1] in to_know:
            out_to_know.append(file)

        i = 0
        while i < len(cur[2]):
            if choices[i] > 0:
                ddd.append(''.join(map(str, cur[2][i])))
                i += 1
            else:
                ddd.append(''.join(str(num) for sublist in cur[2][i:i+(-choices[i])] for num in sublist))
                i -= choices[i]   
        data.append(ddd)

    # while 1:
    #     zzr = input("-1 to exit\n")
    #     if zzr == "-1":
    #         break
    #     zzr = zzr.split()
    #     # zzr = [list(map(int, element)) for element in zzr]
    #     for i in range(len(zzr)):
    #         lol = []
    #         for j in zzr[i]:
    #             if j in '0123456789':
    #                 lol.append(int(j))
    #         zzr[i] = lol
    #     zzr[0] = [str(x) for x in zzr[0]]
    #     if zzr[0][0] != '1':
    #         zzr[0][0] = 'x'
    #     zzr[0] = ''.join(zzr[0])
    #     print(zzr)
        
    #     cur = checky(ans, points, choices, zzr, 1)
    #     if type(cur) == str:
    #         print(cur)
    #         continue

    #     ddd = [cur[1], str(cur[0]), "?"]
    #     i = 0
    #     while i < len(cur[2]):
    #         if choices[i] > 0:
    #             ddd.append(''.join(map(str, cur[2][i])))
    #             i += 1
    #         else:
    #             ddd.append(''.join(str(num) for sublist in cur[2][i:i+(-choices[i])] for num in sublist))
    #             i -= choices[i]   
    #     data.append(ddd)
    #     print(ddd)

    if len(out_to_know) > 0:
        print("To know:", out_to_know)

    if save == 0:
        print("Data not saved")
        print(data)
        exit()        
    
    with open(out_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(heads)

        writer.writerows(data)


if __name__ == "__main__":
    main()  # Call the main function
    # print(read("./one/20241008133408-0001.jpg", 14))
    # print(read_csv("exam3_ans.csv"))