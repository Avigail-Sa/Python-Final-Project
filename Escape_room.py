from operator import truediv

import pygame
import random
import sys




pygame.init()

# צבעים
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRAUN= (118,57 ,13)
EVEN= (238,155,31)
GREENGRAY=(92,138,125)
RED=(255,0,0)
GRAY = (200, 200, 200)


# גודל המסך
SCREEN_WIDTH, SCREEN_HEIGHT = 600 ,500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Escape room")



def entry():
    # טעינת תמונת הרקע
    background_image = pygame.image.load("open.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # טעינת המפתחות
    keys = []
    for i in range(1, 11):
            key_image = pygame.image.load("key (4).png")
            key_image = pygame.transform.scale(key_image, (31,62))
            key_rect = key_image.get_rect(topleft=(random.randint(280,580),random.randint(380,430)))
            keys.append({'image': key_image, 'rect': key_rect})

    # טעינת הטקסט עם גופן מותאם אישית
    font = pygame.font.Font("waltograph42.otf", 40)  # גודל גופן מותאם
    text_lines = [
        "    Welcome",
        "  to the game!",
        " There's a keys ",
        " here. Find out",
        "which key opens",
        "the door to the",
        " escape room!"
    ]

    # טעינת חור המנעול
    holekey_image = pygame.image.load('holekey.png')
    holekey_image = pygame.transform.scale(holekey_image, (25, 75))
    holekey_rect = holekey_image.get_rect(topleft=(270, 160))

    dragging = False
    selected_key = None
    mouse_offset_x, mouse_offset_y = 0, 0
    CORECT=False
    running = True


#םונקציה שבודקת איזה מפתח נגע בחור המנעול
    def how_key(x, y):
        for idx, key in enumerate(keys):
            if key['rect'].collidepoint(x, y):
                return idx
        return None


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                key_x, key_y = event.pos
                key_idx = how_key(key_x, key_y)
                if key_idx is not None:
                    selected_key = keys[key_idx]
                    mouse_offset_x = selected_key['rect'].x - key_x
                    mouse_offset_y = selected_key['rect'].y - key_y
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                if selected_key and selected_key==keys[4] and selected_key['rect'].colliderect(holekey_rect):
                    CORECT=True
            elif event.type == pygame.MOUSEMOTION:
                if dragging and selected_key:
                    selected_key['rect'].x = event.pos[0] + mouse_offset_x
                    selected_key['rect'].y = event.pos[1] + mouse_offset_y
        if CORECT:
            # הצגת טקסט הצלחה
            font2 = pygame.font.Font('orange juice 2.0.ttf', 150)
            corect_text = font2.render("CORECT!", True, RED)
            screen.blit(corect_text, (20, 200))
            pygame.display.flip()
            pygame.time.delay(1000)

            # מעבר לחדר הבריחה
            escape_room()
            return

        # ציור הרקע
        screen.blit(background_image, (0, 0))

        # ציור חור המנעול
        screen.blit(holekey_image, holekey_rect)

        # ציור המפתחות
        for key in keys:
            screen.blit(key['image'], key['rect'])

        # ציור הטקסט
        y_offset = 200
        for line in text_lines:
            rendered_line = font.render(line, True, GREENGRAY)
            screen.blit(rendered_line, (80, y_offset))
            y_offset += 40

        pygame.display.flip()




def room1():
    #טעינת תמונה
    background_image = pygame.image.load("room1.avif")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


    # טעינת תמונת הטקסט
    ceiling_image = pygame.image.load("text3.png")
    ceiling_image = pygame.transform.scale(ceiling_image, (80,120))

    #טעינת תמונות הלכלוכים שמכסים את הקוד ויצירת כפתורים
    dirt_image = pygame.image.load("dirt.png")
    dirt_image = pygame.transform.scale(dirt_image, (85, 20))
    dirt_rect = dirt_image.get_rect(topleft=(270, 85))
    dirt_image2 = pygame.image.load("dirt2.png")
    dirt_image2 = pygame.transform.scale(dirt_image2, (85, 20))
    dirt_rect2 = dirt_image2.get_rect(topleft=(270, 85))


    #טעינת תמונת המברשת ויצירת כפתור
    brush_image = pygame.image.load("brush.png")
    brush_image = pygame.transform.scale(brush_image, (50,50))
    brush_rect = brush_image.get_rect(topleft=(430, 300))

    #טעינת כפתור חזרה
    go_back_image = pygame.image.load("Go_back1.png")
    go_back_image = pygame.transform.scale(go_back_image, (50, 50))
    go_back_rect = go_back_image.get_rect(topleft=(10,10))

    #טעינת טקסט הקוד
    font3 = pygame.font.Font('28 Days Later.ttf', 8)
    Code_text = font3.render(" Your namber  is   2", True, BLACK)


    clean=0
    dragging = False
    mouse_offset_x, mouse_offset_y = 0, 0

    #לולאת המשחק
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if brush_rect.collidepoint(x, y):
                    mouse_offset_x = brush_rect.x - x
                    mouse_offset_y = brush_rect.y - y
                    dragging = True
                elif go_back_rect.collidepoint(x, y):  # חזרה לחדר הקודם
                    escape_room()
                    return
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                if brush_rect.colliderect(dirt_rect):  # בדיקת ניקוי הראשון
                    clean += 1
            elif event.type == pygame.MOUSEMOTION and dragging:
                brush_rect.x = event.pos[0] + mouse_offset_x
                brush_rect.y = event.pos[1] + mouse_offset_y

        # ציור המסך בהתאם למצב
        screen.blit(background_image, (0, 0))
        screen.blit(ceiling_image, (480,130))

        if clean == 0:
            screen.blit(dirt_image, dirt_rect)
            screen.blit(dirt_image2, dirt_rect2)
        elif clean == 1:
            screen.blit(dirt_image2, dirt_rect2)  # רק הלכלוך השני
        elif clean >= 2:
            pass  # שני הלכלוכים נוקו, לא מצייר לכלוך

        # ציור המברשת כפתור החזרה והקוד
        screen.blit(go_back_image, go_back_rect)
        screen.blit(Code_text, (270,85))
        screen.blit(brush_image, brush_rect)

        pygame.display.flip()




def room2():
    # טעינת תמונת הרקע
    background_image = pygame.image.load("room2.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # טעינת תמונת מצפן
    compass_image = pygame.image.load("compass.png")
    compass_image = pygame.transform.scale(compass_image, (80, 80))
    compass_rect = compass_image.get_rect(topleft=(390, 120))

    # טעינת גופן
    font = pygame.font.Font("Montague.ttf", 20)

    # טקסטים
    initial_text_lines = [
        "a b c d e f g h i j k l m",
        "n o p q r s t u v w x y z",
        "",
        "      Gb  trg  lbhe",
        "       ahzore  lbh",
        "    arrq  gb  pyvpx",
        " ba  bar  bs  gur  vgrzf",
        "      va  gur  ebbz",
        "       sbhe  gvzrf."
    ]
    code_text_lines = [
        "      Your code is:",
        "            8"
    ]

    # תמונת הנייר
    paper_image = pygame.image.load("paper.png")
    paper_image = pygame.transform.scale(paper_image, (300, 450))

    # כפתור חזרה
    go_back_image = pygame.image.load("Go_back1.png")
    go_back_image = pygame.transform.scale(go_back_image, (50, 50))
    go_back_rect = go_back_image.get_rect(topleft=(10, 10))

    # מצב המשחק
    click_count = 0  # כמה פעמים לחצו על המצפן
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                # בדיקה אם לחצו על המצפן
                if compass_rect.collidepoint(mouse_pos):
                    click_count += 1
                # בדיקה אם לחצו על כפתור החזרה
                elif go_back_rect.collidepoint(mouse_pos):
                    escape_room()  # מעבר לפונקציה escape_room
                    return

        # ציור הרקע ותמונות
        screen.blit(background_image, (0, 0))
        screen.blit(compass_image, compass_rect)
        screen.blit(paper_image, (150, 30))
        screen.blit(go_back_image, go_back_rect)

        # ציור טקסטים
        y_offset = 90
        if click_count >= 3:  # אם לחצו 3 פעמים או יותר
            for line in code_text_lines:
                rendered_line = font.render(line, True, BLACK)
                screen.blit(rendered_line, (165, y_offset))
                y_offset += 40
        else:  # אם לחצו פחות מ-3 פעמים
            for line in initial_text_lines:
                rendered_line = font.render(line, True, BLACK)
                screen.blit(rendered_line, (165, y_offset))
                y_offset += 40

        pygame.display.flip()


def room3():
    # טעינת תמונת הרקע
    background_image = pygame.image.load("room3.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # טעינת כפתור חזרה
    go_back_image = pygame.image.load("Go_back1.png")
    go_back_image = pygame.transform.scale(go_back_image, (50, 50))
    go_back_rect = go_back_image.get_rect(topleft=(10, 10))

    # טעינת הטקסט
    font = pygame.font.Font("28 Days Later.ttf", 30)
    text_lines = [
        "      In this room time is working against you",
        "  Your task Press each cube as many times as",
        "                  the number written on it",
        "            But hurry  the clock is ticking",
        "                               Good luck"
    ]

    # טעינת טקסט הקוד
    font_code = pygame.font.Font('28 Days Later.ttf', 20)
    Code_text = font_code.render("Your number is 9", True, WHITE)

    # טעינת הקוביות
    dice = []
    for i in range(1, 7):
        dice_image = pygame.image.load(f"dice{i}.png")
        dice_image = pygame.transform.scale(dice_image, (70,90))
        dice_rect = dice_image.get_rect(topleft=(random.randint(80, 580), random.randint(300, 430)))
        dice.append({'image': dice_image, 'rect': dice_rect})

    # משתנה לזמן הצגת הטקסט
    show_text_duration = 10000  # משך הזמן להצגת הטקסט (במילישניות)
    start_ticks = pygame.time.get_ticks()  # תחילת הזמן

    # משתנה לטיימר
    TIME_LIMIT = 13
    timer_start_ticks = None  # מתי מתחיל הטיימר האמיתי

    # משתנה למעקב אחרי הקלקות
    types = [0] * 6

    # פונקציה לבדיקה אם המשחק הצליח
    def is_succeeded(t):
        return all(count == idx + 1 for idx, count in enumerate(t))

    running = True
    while running:
        # טיפול באירועים
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                dice_x, dice_y = event.pos
                dice_idx = next((idx for idx, d in enumerate(dice) if d['rect'].collidepoint(dice_x, dice_y)), None)
                if dice_idx is not None:
                    types[dice_idx] += 1
                elif go_back_rect.collidepoint(mouse_pos):
                    escape_room()
                    return

        # חישוב הזמן שחלף
        current_ticks = pygame.time.get_ticks()
        time_since_start = current_ticks - start_ticks

        # ציור המסך
        screen.blit(background_image, (0, 0))
        screen.blit(go_back_image, go_back_rect)

        if time_since_start < show_text_duration:
            # הצגת הטקסט
            y_offset = 180
            for line in text_lines:
                rendered_line = font.render(line, True, RED)
                screen.blit(rendered_line, (10, y_offset))
                y_offset += 40
        else:
            if timer_start_ticks is None:
                # הפעלת הטיימר כשהטקסט נעלם
                timer_start_ticks = pygame.time.get_ticks()

            # חישוב הזמן שנותר
            seconds_passed = (pygame.time.get_ticks() - timer_start_ticks) / 1000
            time_left = max(0, TIME_LIMIT - seconds_passed)

            # הצגת הזמן
            font_timer = pygame.font.Font("CollegiateFLF.ttf", 74)
            timer_text = font_timer.render(f"{int(time_left)}", True, RED)
            screen.blit(timer_text, (270, 150))

            # ציור הקוביות או הצגת הקוד
            if is_succeeded(types):
                screen.blit(Code_text, (230, 450))
            else:
                for d in dice:
                    screen.blit(d['image'], d['rect'])

            # סיום המשחק אם הזמן נגמר
            if time_left <= 0 and not is_succeeded(types):
                escape_room()
                return

        pygame.display.flip()


def room4():
    # טעינת תמונת הרקע
    background_image = pygame.image.load("room4.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # טעינת תמונת הלוח
    board_image = pygame.image.load("board1.png")
    board_image = pygame.transform.scale(board_image, (170, 130))

    # טעינת כפתור חזרה
    go_back_image = pygame.image.load("Go_back1.png")
    go_back_image = pygame.transform.scale(go_back_image, (50, 50))
    go_back_rect = go_back_image.get_rect(topleft=(10, 10))

    # יצירת כף המאזניים
    scale_rect = pygame.Rect(295, 210, 100, 100)

    # טעינת טקסט הקוד
    font_code = pygame.font.Font('28 Days Later.ttf', 50)
    Code_text = font_code.render("Your number is 0", True, RED)

    # טעינת החפצים
    objects = []
    for j in range(0, 2):  # כל אובייקט נטען פעמיים
        for i in range(1, 5):  # ארבעה אובייקטים
            object_image = pygame.image.load(f"object{i}.png")
            object_image = pygame.transform.scale(object_image, (70, 90))
            object_rect = object_image.get_rect(topleft=(random.randint(80, 530), random.randint(300, 450)))
            objects.append({'image': object_image, 'rect': object_rect, 'id': i})

    # רשימה שתעקוב אחר החפצים שנמצאים על כף המאזניים
    on_scale = []

    dragging = False
    selected_object = None
    mouse_offset_x, mouse_offset_y = 0, 0
    running = True

    # בדיקה אם החפצים שעל כף המאזניים תואמים לחפצים הנכונים
    def check_scale_items():
        current_ids = [obj['id'] for obj in on_scale]
        # תנאים: אובייקט 1 פעם אחת, אובייקט 3 פעמיים
        return current_ids.count(1) == 2 and current_ids.count(3) == 1

    success = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # בדיקה אם נלחץ על כפתור החזרה
                if go_back_rect.collidepoint(event.pos):
                    escape_room()
                    return
                # בדיקה אם נלחץ על חפץ
                for obj in objects:
                    if obj['rect'].collidepoint(event.pos):
                        selected_object = obj
                        mouse_offset_x = obj['rect'].x - event.pos[0]
                        mouse_offset_y = obj['rect'].y - event.pos[1]
                        dragging = True
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                if selected_object:
                    # בדיקה אם החפץ הונח על כף המאזניים
                    if selected_object['rect'].colliderect(scale_rect):
                        if selected_object not in on_scale:
                            on_scale.append(selected_object)
                    else:
                        if selected_object in on_scale:
                            on_scale.remove(selected_object)
                selected_object = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging and selected_object:
                    selected_object['rect'].x = event.pos[0] + mouse_offset_x
                    selected_object['rect'].y = event.pos[1] + mouse_offset_y

        # ציור האלמנטים
        screen.blit(background_image, (0, 0))
        screen.blit(go_back_image,(10,10))
        screen.blit(board_image, (421, 160))  # ציור הלוח

        # ציור החפצים
        for obj in objects:
            screen.blit(obj['image'], obj['rect'])

        # בדיקה אם כל החפצים על כף המאזניים נכונים וכתיבת הקוד
        if check_scale_items():
            success = True

        # ציור הקוד אם ההצלחה הושגה
        if success:
            screen.blit(Code_text, (230, 450))

        pygame.display.flip()


def room5():
    # טוען את תמונת הרקע
    background = pygame.image.load("room5.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # טעינת כפתור חזרה
    go_back_image = pygame.image.load("Go_back1.png")
    go_back_image = pygame.transform.scale(go_back_image, (50, 50))
    go_back_rect = go_back_image.get_rect(topleft=(10, 10))


    # טעינת טקסט הקוד
    font_code = pygame.font.Font('28 Days Later.ttf', 20)
    Code_text = font_code.render("Your number is 3", True, RED)


    # לוח סודוקו פתיר
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    # עוקבים אחר שינויים של המשתמש
    user_changes = [[False for _ in range(9)] for _ in range(9)]


    # מיקום התחלה של לוח הסודוקו
    START_X = 194 # נקודת התחלה בציר X
    START_Y = 230  # נקודת התחלה בציר Y
    CELL_SIZE = 28  # גודל תא בודד

    selected_cell = None

    def draw_board():
        """מצייר את לוח הסודוקו"""
        # מציגים את הרקע
        screen.blit(background, (0, 0))

        # מציירים את קווי הרשת
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(screen, WHITE, (START_X + i * CELL_SIZE, START_Y),
                             (START_X + i * CELL_SIZE, START_Y + 9 * CELL_SIZE), line_width)
            pygame.draw.line(screen, WHITE, (START_X, START_Y + i * CELL_SIZE),
                             (START_X + 9 * CELL_SIZE, START_Y + i * CELL_SIZE), line_width)


        # מציירים את המספרים בלוח
        FONT = pygame.font.SysFont("comicsans", 20)
        for row in range(9):
            for col in range(9):
                if sudoku_board[row][col] != 0:
                    text_color = WHITE if not user_changes[row][col] else GRAY
                    text = FONT.render(str(sudoku_board[row][col]), True, text_color)
                    text_rect = text.get_rect(
                        center=(START_X + col * CELL_SIZE + CELL_SIZE // 2, START_Y + row * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text, text_rect)

    #פונקציה בדיקה שהסודוקו הושלם
    def is_sudoku_complete():
        # בדיקה שכל התאים מלאים
        for row in sudoku_board:
            if 0 in row:
                return False

        # בדיקה שאין כפילויות בשורות, בעמודות ובתת-ריבועים
        for i in range(9):
            if len(set(sudoku_board[i])) != 9:  # שורות
                return False
            if len(set(sudoku_board[j][i] for j in range(9))) != 9:  # עמודות
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [sudoku_board[r][c] for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3)]
                if len(set(box)) != 9:  # תת-ריבועים
                    return False

        return True

    running = True

    while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = event.pos
                    if START_X <= x <= START_X + 9 * CELL_SIZE and START_Y <= y <= START_Y + 9 * CELL_SIZE:
                        selected_cell = ((y - START_Y) // CELL_SIZE, (x - START_X) // CELL_SIZE)
                    elif go_back_rect.collidepoint(mouse_pos):
                        escape_room()
                        return
                elif event.type == pygame.KEYDOWN:
                    if selected_cell:
                        row, col = selected_cell
                        if user_changes[row][col] or sudoku_board[row][col] == 0:
                            if event.key == pygame.K_BACKSPACE:
                                sudoku_board[row][col] = 0
                                user_changes[row][col] = False
                            else:
                                num = event.key - pygame.K_0
                                if 1 <= num <= 9:
                                    sudoku_board[row][col] = num
                                    user_changes[row][col] = True


            #בדיקה אם הסודוקו הושלם אום כן נכתב הקוד
            if is_sudoku_complete():
                screen.blit(Code_text,(230,450))
            else:
               # ציור לוח הסודוקו
               draw_board()

            screen.blit(go_back_image, go_back_rect)  # ציור כפתור חזרה

            # ציור התא הנבחר
            if selected_cell:
                row, col = selected_cell
                pygame.draw.rect(screen, RED,
                                 (START_X + col * CELL_SIZE, START_Y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)



            pygame.display.flip()




#חדר עם פאזל 8
def room6():

    # טעינת תמונת הרקע
 background_image = pygame.image.load("room6.jpg")
 background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

  # טעינת כפתור חזרה
 go_back_image = pygame.image.load("Go_back1.png")
 go_back_image = pygame.transform.scale(go_back_image, (50, 50))
 go_back_rect = go_back_image.get_rect(topleft=(10, 10))

# טעינת טקסט הקוד
 font_code = pygame.font.Font('28 Days Later.ttf', 20)
 Code_text = font_code.render("Your number is 6", True, BLACK)

 # הגדרת ריבועי המשחק
 TILE_SIZE = 50
 GRID_POSITIONS = [(x, y) for y in range(80, 200, TILE_SIZE) for x in range(120, 240, TILE_SIZE)]

 # יצירת רשימת כפתורים
 tiles = list(range(1, 9)) + [None]
 random.shuffle(tiles)

 # פונקציה לציור הריבועים
 def draw_tiles():
    for idx, tile in enumerate(tiles):
        x, y = GRID_POSITIONS[idx]
        if tile is not None:
            pygame.draw.rect(screen, BRAUN, (x, y, TILE_SIZE, TILE_SIZE))
            font = pygame.font.Font('Alexandria Whitehouse.otf', 60)
            text = font.render(str(tile), True, EVEN)
            text_rect = text.get_rect(center=(x + TILE_SIZE // 2, (y + TILE_SIZE // 2)-10))
            screen.blit(text, text_rect)

 # פונקציה לחישוב המיקום הריק
 def get_empty_index():
    return tiles.index(None)

 # פונקציה להחלפת אריחים
 def swap_tiles(idx1, idx2):
    tiles[idx1], tiles[idx2] = tiles[idx2], tiles[idx1]

 # פונקציה לבדוק אם המשחק הושלם
 def is_solved():
    return tiles == list(range(1, 9)) + [None]

 # לולאת המשחק
 running = True
 while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = event.pos
            clicked_index = None
            for idx, (x, y) in enumerate(GRID_POSITIONS):
                if x <= mouse_x < x + TILE_SIZE and y <= mouse_y < y + TILE_SIZE:
                    clicked_index = idx
                    break
            if clicked_index is not None:
                empty_index = get_empty_index()
                if clicked_index in [empty_index - 1, empty_index + 1, empty_index - 3, empty_index + 3]:
                    swap_tiles(clicked_index, empty_index)
            elif go_back_rect.collidepoint(mouse_pos):
                escape_room()
                return
    # ציור הרקע
    screen.blit(background_image, (0, 0))

    if is_solved():
        screen.blit(Code_text,(120,150))
    else:
        # ציור האריחים
        draw_tiles()


    # ציור כפתור חזרה
    screen.blit(go_back_image, go_back_rect)

    # עדכון המסך
    pygame.display.flip()


def room7():
    font = pygame.font.Font("Moon Flower Bold.ttf", 36)
    input_rect = pygame.Rect(300, 250, 200, 50)  # שדה הקלט
    button_rect = pygame.Rect(320, 320, 160, 50)  # כפתור הבדיקה
    user_text = ""
    correct_code = "289036"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]  # מחיקת התו האחרון
                elif event.key == pygame.K_RETURN:
                    if user_text == correct_code:
                       exit()
                       return
                else:
                    user_text += event.unicode  # הוספת התו שהוקלד
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    if user_text == correct_code:
                        exit()
                        return
                else:
                    escape_room()
                    return


        # ציור שדה הקלט
        pygame.draw.rect(screen, BLACK, input_rect)
        text_surface = font.render(user_text, True, WHITE)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 10))

        # ציור כפתור הבדיקה
        pygame.draw.rect(screen, BLACK, button_rect)
        button_text = font.render("Check", True, WHITE)
        screen.blit(button_text, (button_rect.x + 50, button_rect.y + 10))


        pygame.display.flip()




def exit():
    # טעינת תמונת הרקע
    background_image = pygame.image.load("EXIT.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # טעינת הטקסט
    font = pygame.font.Font("Moon Flower Bold.ttf", 30)
    text_lines = [
        " *******************Congratulations!*********************",
        " You've successfully escaped the escape room and solved every puzzle. ",
        "          Your intelligence and perseverance led you to victory.",
        "                            Thank you for playing.",
        "     The journey may be over, but the experience will stay with you.",
        "*********************Until next time!********************",
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ציור הרקע
        screen.blit(background_image, (0, 0))

        # הצגת הטקסט
        y_offset = 300
        for line in text_lines:
            rendered_line = font.render(line, True, RED)
            screen.blit(rendered_line, (2, y_offset))
            y_offset += 32

        pygame.display.flip()


def escape_room():
    # טעינת תמונת הרקע
    background_image = pygame.image.load("allroom1.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    #יצירת כפתורים לדלתות
    doors=[]
    for i in range (0,7):
        scale_rect = pygame.Rect(15+i*86, 130, 45, 150)
        doors.append(scale_rect)

    #טעינת טקסט
    font = pygame.font.Font("Moon Flower Bold.ttf", 27)
    text_lines = [
        "     Welcome to the escape room!   There are six rooms and an exit, ",
        " to get out you need a 6-digit code and each room you solve successfully ",
        "  will give you a digit. To get back out to the corridor from the rooms, ",
        " you have a back button installed. In rooms where there is no explanation,",
        "try to find clues, objects that move and try to see why they will help you.",
        "                               Good luck!",
    ]

    # מילון למיפוי הדלתות לפונקציות
    room_functions = {
        0: room1,
        1: room2,
        2: room3,
        3: room4,
        4: room5,
        5: room6,
        6: room7
    }

    # םונקציה שבודקת איזה דלת נלחצה
    def how_door(x, y):
        for idx, d in enumerate(doors):
            if d.collidepoint(x, y):
                return idx
        return None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                idx = how_door(x, y)
                if idx is not None:
                    room_functions[idx]()
                    running = False
                    return
        # ציור הרקע
        screen.blit(background_image, (0, 0))

        # הצגת הטקסט
        y_offset = 300
        for line in text_lines:
            rendered_line = font.render(line, True, BLACK)
            screen.blit(rendered_line, (8, y_offset))
            y_offset += 32

        pygame.display.flip()



entry()










pygame.quit()


