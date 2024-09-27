from check import checky
from scan import read, read_csv
# read function returns two values
# student_id: a string, 9 digits, if drawn any other value other than 1 on first column will be changed to 'x'
# student_ans: a list, with each elements being lists(in case of multiple choices on same answer)
# for multiple answers questions, each wrong option will cause 2/n of the question, no below 0, and ceil(). n has to be written in array 'choices'
# for single answer questions, either all points or no points. Write 1 in 'choices'
# for linked question(need more than one column) write negative column number you need on first col, and 0 for rest in 'choices. All or 0 points\
#   Example you need 3 columns to linked together, and the question is 10 points. [-3, 0, 0] in 'choices', and [10, 0, 0] in 'points'

def main():
    # ans = [0, 1, 0, 1, 4, 5, 7, 7, 1, 1,
    #        [8, 9], [4, 5, 6], [5, 7, 8, 9], 1, 1, 9, 5, 5, 5, 5]
    # points = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    #           10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    # choices = [1, 1, 1, 1, -2, 0, -2, 0, -2, 0,
    #             2, 3, 6, 1, 1, 1, -4, 0, 0, 0]
    ans, choices, points, _ = read_csv("read.csv")
    print(checky(ans, points, choices, "test/setA/1000041661.jpg"))

if __name__ == "__main__":
    main()  # Call the main function
    # print(read("./test/scanned.jpg", 15))
    # print(read_csv("read.csv"))