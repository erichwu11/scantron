# Scantron
Hello, this is a file reading scantron, where you take a photo or scan a made(using our [create.py](#create.py)) test paper. In this scantron, we use 4 aruco markers to determine where the circles are, and also do skew correction. We then can use [main.py](#main.py) to check the answers from [answers.csv](#answers.csv), allowing quick and accurate grading.

## Warning
Student ID is for NTHU. For ids starting with 'x', fill in any other numbers other than '1'.
To be honest, I have completely no idea what im doing, whether the code or this README file. I have never joined a big project where you create neat and readable code, and write clear README. So you are always welcome to change the files, or fork and improve it.

## The Basic Idea
1. Create a picture of columns of bubbles and aruco markers. Please dont paste it too close to the edge of the paper, or the code cannot detect them.
2. After filling in, you can either scan it or take a picture of it, as long as its clear.
3. Grade the paper using main.py. Fill in`dir_path`, `ans_path`, `out_path`, `save`. Then it should automatically grade it.
4. If somehow the picture is unreadable, the code will pop out the picture, and you can fill it in manually.

## Files
### create.py
This is for creating a scantron paper .png(or any picture file) which can be put on your test paper for students to fill out. `questions` are for how many columns you want. If you want to change the ids of the aruco markers, it should near bottom of the code, but remember to also change the ids in [scan.py](#scan.py)
### answers.csv
There should 3 columns in the .csv file, "Answers", "Choices", and "Points". First column should be correct answers. Second column is "Choices", which means single, multi, or linking choices. "Points" column is for how many points will be given for getting the question right.
- "Single" choice questions are only **one correct answer**. Either you get it right and have all the points, or get it wrong and no points. For the "Choices" section, should fill in 1, as in only one choice. Example: correct answer: 2, choices: 1, points: 10. If student's answer is 0, then 0 points are given, if its 2, then 10 points.
- "Multi" choices questions are **questions having multiple answers**, and will deduce points if choosing wrongly. For ***N*** choices, for each wrong selection ***1 - 2 / N*** part of the points will be deduced, at least 0 points are given for the question. "Choices" part should fill in ***N***. For example, answer: 013, choices: 5, points: 15. So each wrong option is 15 * (1 - 2 / N) = 6. So if the student answered 013, he gets 15 points, 01 or 0134 is 9(15 - 6). 014 will be 3, and 24 will be 0.
- "Linked" questions are for **questions that need multiple columns**, if one of the column is wrong answers, then no points will be given. Such question type is good for calculation questions. For the "choices" part, negative numbers of how many columns you need should be the input. For example: answer: 524, choices: -3(since there are 3 digits), points: 10. So 524 will get 10 points, will any other submissions will not have no points.
### main.py
Fill in`dir_path`, `ans_path`, `out_path`, `save`. Then it should automatically grade it.
- `dir_path`: the "folder" where the pictures are
- `ans_path`: where the [answer.csv](#answer.csv) is
- `out_path`: the filename you want to call for output
- `save`: whether you want to create a csv file(`save` = 1) or not
- `to_know`: if you want to search the picture name that some ids belong to, you can use this list
#### check.py
Some of the functions are written here
#### scan.py
Some other functions are here
### Other Files
#### README.md
This :D
#### change_score.py
This is for if you need to change answers and recalculate the scores, but dont want to rescan or re-manually-input.
- `file_path`: the output csv from original `main.py`
- `changed.csv`: the output name
#### counting.py
Summarize choices all the students choose for every question
#### mean.py
Calculate average and see the distribution
