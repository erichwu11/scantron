import cv2
import cv2.aruco as aruco
import numpy as np

def read(image_path, questions):
    # Load the image
    # image_path = 'lol.png'
    image = cv2.imread(image_path)

    top_left_id = 0
    top_right_id = 1
    bottom_left_id = 2
    bottom_right_id = 3

    original_x = 320 + 30 * questions - 10
    original_y = 370 - 10
    original_0 = (10, 10)

    homo_matrix = None

    def map_to_original(x, y):
        point = np.array([x, y, 1], dtype='float32')
        inverse_homography = np.linalg.inv(homo_matrix)
        skewed_point = np.dot(inverse_homography, point)

        skewed_x = skewed_point[0] / skewed_point[2]
        skewed_y = skewed_point[1] / skewed_point[2]
        return int(skewed_x), int(skewed_y)

    def save_check(x, y, img):
        vote = 0
        move_x = [0, 0, 0, -3, -3, -3, 3, 3, 3, 0, -5, 5, 0]
        move_y = [0, -3, 3, 0, -3, 3, 0, -3, 3, -5, 0, 0, 5]
        cope = img.copy()
        for i in range(len(move_x)):
            temp_x, temp_y = map_to_original(x + move_x[i], y + move_y[i])
            if 0 <= temp_x < img.shape[1] and 0 <= temp_y < img.shape[0]:
                if img[temp_y, temp_x] == 0:
                    vote += 1
                else:
                    vote -= 1
                cope[temp_y, temp_x] = 0
        # cv2.imshow('bbb', cope)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return vote > 0

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Load the ArUco dictionary and parameters
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
    parameters =  aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejected = detector.detectMarkers(gray)

    # if ids is not None:
    #     image_with_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids)
    #     for i in range(len(ids)):
    #         print(f"Detected marker ID: {ids[i][0]}")
    # else:
    #     image_with_markers = gray.copy()
    #     print("No markers detected")
    # cv2.imshow('Detected ArUco Markers', image_with_markers)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ids = ids.flatten()
    corners = [tuple(map(int, x[0][0])) for x in corners]
    assert len(ids) == 4


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
    #         change_i, change_j = map_to_original(i + 770, j + 340)
    #         img[change_j, change_i] = 0
    # cv2.imshow('nnn', img)
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
        elif col < 8:
            print("error at student id", col, cur, stud_id)
            # assert 0

    # if id starts with x, tell them to go for random number other than 1
    if stud_id[0] != 1:
        stud_id[0] = 'x'
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