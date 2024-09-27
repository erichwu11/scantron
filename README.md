# Scantron
Hello, this is a file reading scantron, where you take a photo or scan a made(using our create.py) test paper. In this scantron, we use 4 aruco markers to determine where the circles are, and also do skew correction. We then can use "read.csv" to check the answers, allowing quick and accurate grading.

## Warning
Student ID is for NTHU.

## create.py
This is for creating a scantron paper .png(or any picture file) which can be put on your test paper for students to fill out.

## Columns
### read.csv
There are 3 columns in the .csv file, "Answers", "Choices", and "Points". In this part, the columns will just be explained slightly, further explanation will be in the next 3 parts.
First column should be correct answers.
Second column is "Choices", which means single, multi, or linking choices. Linking choices are for those questions that need multiple columns. For example, the correct answer to a question is 123, which will be needing 3 columns. Linking choices questions are suitable for these kinds of questions.
"Points" column is for how many points will be given for getting the question right.
### Answers
Single multiple choices are intuitive, just insert "1", "2", or "135", "124" for those kinds of questions. For linking choices questions, please type out all the digits in the same cell. For example, "1122", or even if the answer is 0, and you gave 4 columns to the question, type in "0000".
### Choices
Typing in 1 in the "Choices" column means the question is a single choice question. Typing in a number more than 1, lets say 5, for example, will denote that the question is multiple choices, and there are total 5 choices for the question, the reason why we need total choices is how the points are given, which will be elaborated on the next part. For linking choices question, negative numbers should be inserted, for example, -3 will mean this is a linking choice question with 3 columns.
### main.py
it should be simple code, just imitate whats on there, and change the input to your picture, and it should work.