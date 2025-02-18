import cv2
import numpy as np
import easyocr

SIZE = 1800

def sudo(image):
    print('cuo')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un flou gaussien et un seuillage adaptatif
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Trouver les contours et trier par aire décroissante
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Trouver la grille du sudoku
    sudoku_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            sudoku_contour = approx
            break

    # Trier les points du contour
    pts = sudoku_contour.reshape(4, 2)
    pts = sorted(pts, key=lambda x: x[0])
    left_points, right_points = sorted(pts[:2], key=lambda x: x[1]), sorted(pts[2:], key=lambda x: x[1])
    ordered_pts = np.array([left_points[0], left_points[1], right_points[1], right_points[0]], dtype="float32")

    # Transformer la perspective
    dst_pts = np.array([[0, 0], [0, SIZE - 1], [SIZE - 1, SIZE - 1], [SIZE - 1, 0]], dtype="float32")
    M = cv2.getPerspectiveTransform(ordered_pts, dst_pts)
    warped = cv2.warpPerspective(image, M, (SIZE, SIZE))

    # Convertir en niveaux de gris et seuiller
    gray_warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    thresh_warped = cv2.adaptiveThreshold(cv2.GaussianBlur(gray_warped, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Découper l'image en cellules
    cell_size = SIZE // 9
    cells = [warped[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size] for i in range(9) for j in range(9)]

    # Appliquer OCR
    reader = easyocr.Reader(['en'])
    def ocr_digit_easyocr(cell_image):
        gray_cell = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
        _, threshold_cell = cv2.threshold(gray_cell, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        result = reader.readtext(threshold_cell)
        for detection in result:
            if detection[1].strip().isdigit():
                return int(detection[1].strip())
        return 0

    digits = [ocr_digit_easyocr(cell) for cell in cells]

    # Résolution du Sudoku
    def is_safe(board, row, col, num):
        return not (num in board[row] or num in board[:, col] or num in board[row - row % 3:row - row % 3 + 3, col - col % 3:col - col % 3 + 3])

    def solve_sudoku(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_safe(board, row, col, num):
                            board[row][col] = num
                            if solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    board = np.array(digits).reshape(9, 9)
    solve_sudoku(board)


    # Charger l'image de la grille du Sudoku (ajustée à l'étape précédente)
    height, width = warped.shape[:2]

    # Définir la taille des cases du Sudoku (en pixels)
    cell_width = width // 9
    cell_height = height // 9

    # Pour chaque case, ajouter le chiffre sur l'image
    for i in range(9):
        for j in range(9):
            digit = board[i][j]
            if digit != 0:  # On n'affiche que les chiffres non nuls
                # Positionner le texte dans chaque case (centrer)
                x = j * cell_width + cell_width // 2
                y = i * cell_height + cell_height // 2
                # Placer le texte (numéro) sur l'image
                cv2.putText(warped, str(digit), (x - 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2)

    return warped