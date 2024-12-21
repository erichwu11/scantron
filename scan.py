import cv2
import cv2.aruco as aruco
import numpy as np
import pandas as pd
from PIL import Image

def read(image_path, questions):
    # Load the image
    # image_path = 'lol.png'
    image = cv2.imread(image_path)

    top_left_id = 0
    top_right_id = 1
    bottom_left_id = 2
    bottom_right_id = 7

    original_x = 320 + 30 * questions - 10
    original_y = 370 - 10
    original_0 = (10, 10)

    homo_matrix = None

    # skewed correction
    def map_to_original(x, y):
        point = np.array([x, y, 1], dtype='float32')
        inverse_homography = np.linalg.inv(homo_matrix)
        skewed_point = np.dot(inverse_homography, point)

        skewed_x = skewed_point[0] / skewed_point[2]
        skewed_y = skewed_point[1] / skewed_point[2]
        return int(skewed_x), int(skewed_y)

    # check for multiple pixels to make sure
    def save_check(x, y, img):
        vote = 0
        move_x = [0, 0, 0, -3, -3, -3, 3, 3, 3, 0, -5, 5, 0]
        move_y = [0, -3, 3, 0, -3, 3, 0, -3, 3, -5, 0, 0, 5]
        # cope = img.copy()
        for i in range(len(move_x)):
            temp_x, temp_y = map_to_original(x + move_x[i], y + move_y[i])
            if 0 <= temp_x < img.shape[1] and 0 <= temp_y < img.shape[0]:
                if img[temp_y, temp_x] == 0:
                    vote += 1
                else:
                    vote -= 1
        #         cope[temp_y, temp_x] = 0
        # for i in range(30):
        #     for j in range(30):
        #         temp_x, temp_y = map_to_original(x + i, y + j)
        #         cope[temp_y, temp_x] = 0
        # new_size = (int(cope.shape[1] * 0.3), int(cope.shape[0] * 0.3))
        # cv2.imshow('bbb', cv2.resize(cope, new_size))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return vote > -6

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # threshold of splitting black and white
    _, gray = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    # Load the ArUco dictionary and parameters
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
    parameters =  aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejected = detector.detectMarkers(gray)

    # color_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    # if ids is not None:
    #     # Draw the detected markers and their IDs
    #     image_with_markers = aruco.drawDetectedMarkers(color_image, corners, ids)
        
    #     # Draw boundaries around each marker
    #     for i, corner in enumerate(corners):
    #         # Convert the corner points to integers
    #         pts = corner[0].astype(int)
    #         # Draw the boundary using polylines
    #         cv2.polylines(image_with_markers, [pts], True, (0, 255, 0), 2)  # Green boundary with thickness 2
    #         # Print detected marker ID
    #         print(f"Detected marker ID: {ids[i][0]}")
    # else:
    #     image_with_markers = color_image.copy()
    #     print("No markers detected")

    # new_size = (int(image_with_markers.shape[1] * 0.3), int(image_with_markers.shape[0] * 0.3))
    # cv2.imshow('Detected ArUco Markers', cv2.resize(image_with_markers, new_size))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ids = ids.flatten()
    corners = [tuple(map(int, x[0][0])) for x in corners]
    # assert len(ids) == 4
    if len(ids) != 4:
        return f"Found {len(ids)} aruco markers, not 4"

    for i, marker_id in enumerate(ids):
        if marker_id == top_left_id:
            top_left_corner = corners[i]  # First point in the marker's corner list
        elif marker_id == top_right_id:
            top_right_corner = corners[i]
        elif marker_id == bottom_left_id:
            bottom_left_corner = corners[i]
        elif marker_id == bottom_right_id:
            bottom_right_corner = corners[i]


    skewed_corners = np.array([top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner], dtype='float32')
    correct_corners = np.array([
        original_0,
        [original_0[0] + original_x, original_0[1]],
        [original_0[0] + original_x, original_0[1] + original_y],
        [original_0[0], original_0[1] + original_y]
    ], dtype='float32')

    homo_matrix, _ = cv2.findHomography(skewed_corners, correct_corners)

    # # check if transfer correctly
    # img = gray.copy()
    # for i in range(30):
    #     for j in range(30):
    #         change_i, change_j = map_to_original(i + 320 + questions * 30, j + 340)
    #         img[change_j, change_i] = 0
    # new_size = (int(img.shape[1] * 0.3), int(img.shape[0] * 0.3))
    # cv2.imshow('nnn', cv2.resize(img, new_size))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Student ID part
    stud_id = []
    for col in range(9):
        col_x = 60 + col * 30
        cur = []
        for row in range(10):  # Draw bubbles for each row (0–9)
            bubble_y = 80 + row * 30
            if save_check(col_x, bubble_y, gray):
                cur.append(row)
        if len(cur) == 1:
            stud_id.append(cur[0])
        elif len(cur) > 1 or not (stud_id[0] != 1 and col == 8): # if multiple, or if none but not x113...
            # print("error at student id", col, cur, stud_id)
            # assert 0
            return f"Student ID Error: Column: {col}, Scanned: {' '.join(map(str, cur))}, All: {stud_id}"

    # if id starts with x, tell them to go for random number other than 1
    if stud_id[0] != 1:
        stud_id[0] = 'x'
    if len(stud_id) < 9 and stud_id[0] != 'x' or len(stud_id) < 8:
        return f"Student ID length error {stud_id}"
    stud_id = ''.join(map(str, stud_id))

    
    # Answer parts
    stud_ans = []
    for col in range(questions):
        col_x = 340 + col * 30
        cur = []
        for row in range(10):
            bubble_y = 80 + row * 30
            if save_check(col_x, bubble_y, gray):
                cur.append(row)
        stud_ans.append(cur)

    return stud_id, stud_ans

def read_csv(image_path):
    # Read the CSV file using pandas
    def error_handle(msg, index):
        print(f"Read Answers Error: row {index} error:" + msg)
        exit(1)

    df = pd.read_csv(image_path, dtype={"Answers": "string", "Choices": int, "Points": int})
    ans = []
    choices = []
    points = []
    total_row = 0
    
    for index, row in df.iterrows():
        # print(f"Row {index}: {row}")
        cur_ans = row['Answers'].split(':')
        if row['Choices'] == 1: # Should be int ex. 0
            if any(len(x) != 1 for x in cur_ans): # Single choice questions
                error_handle("answer length should be 1", index)
            ans.append(list(map(int, cur_ans)))
            choices.append(row['Choices'])
            points.append(row['Points'])
            total_row += 1
        elif row['Choices'] > 1: # Multi choices question, should be list ex. [0, 1, 4]
            if any(len(x) > row['Choices'] for x in cur_ans):
                error_handle("answers more than choices", index)
            ans.append(list(map(lambda s: list(map(int, s)), cur_ans)))
            choices.append(row['Choices'])
            points.append(row['Points'])
            total_row += 1
        elif row['Choices'] < 0: # should be string ex. '14'
            # if len(row['Answers']) != -row['Choices']:
            if any(len(x) != -row['Choices'] for x in cur_ans):
                error_handle("answers length doesnt equal to given columns(Choices)", index)
            for i in range(-row['Choices']):
                ans.append(cur_ans)
                if i == 0:
                    choices.append(row['Choices'])
                    points.append(row['Points'])
                else:
                    choices.append(0)
                    points.append(0)
            total_row += -row['Choices']
        else:
            error_handle("choices incorrect, shouldn't be happening", index)
    
    # Final check
    assert isinstance(ans, list)
    assert isinstance(points, list) and all(isinstance(i, int) for i in points)
    assert isinstance(choices, list) and all(isinstance(i, int) for i in choices)
        
    return ans, choices, points, total_row