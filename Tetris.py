import pygame
import random
import csv

# #####################PARAMETERS########################
pygame.init()
win_width = 1200
win_height = 810
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Tetris by Nir")
clock = pygame.time.Clock()
pygame.display.update()
run = True
alive = True
shape_num = 0
score = 0
level = 0
lines = 0
black = (0, 0, 0)
blue = (51, 102, 255)
bright_blue = (0, 255, 255)
yellow = (255, 255, 0)
orange1 = (255, 102, 0)
orange2 = (255, 153, 0)
red = (255, 128, 128)
time_elapsed_since_last_action = 0
time_to_game_over = 0
image = pygame.image.load("tetrisdone.png")
cube_width = 32
cube_height = 32
cube_jump = 35
display_x = 410
display_y = 74
next_x = 945
next_y = 270
myFont = pygame.font.SysFont("Times New Roman", 30)
path = "highscore.csv"
High_score_reader_file = open(path, newline='')
High_score_reader = csv.reader(High_score_reader_file)
High_score = int(next(High_score_reader)[0])
main_lst = [[0 for i in range(11)] for x in range(20)]
next_lst = [[0 for g in range(4)] for n in range(4)]
################################################################


def time_delay():
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        return 5
    else: return 500 - ((score//100)*50)


def display():
    for line in range(0, 19):
        for cube in range(0, 11):
            if main_lst[line][cube] == 0:
                pygame.draw.rect(win, black, (display_x+cube_jump*cube, display_y+cube_jump*line, cube_width, cube_height))
            elif main_lst[line][cube] == 1:
                pygame.draw.rect(win, blue, (display_x+cube_jump*cube, display_y+cube_jump*line, cube_width, cube_height))
            elif main_lst[line][cube] == 2:
                pygame.draw.rect(win, red, (display_x+cube_jump*cube, display_y+cube_jump*line, cube_width, cube_height))
            elif main_lst[line][cube] == 3:
                pygame.draw.rect(win, yellow, (display_x+cube_jump*cube, display_y+cube_jump*line, cube_width, cube_height))
            elif main_lst[line][cube] == 4:
                pygame.draw.rect(win, orange1, (display_x+cube_jump*cube, display_y+cube_jump*line, cube_width, cube_height))
            elif main_lst[line][cube] == 5:
                pygame.draw.rect(win, orange2, (display_x+cube_jump*cube, display_y+cube_jump*line, cube_width, cube_height))
            elif main_lst[line][cube] == 6:
                pygame.draw.rect(win, bright_blue, (display_x+cube_jump*cube, display_y+cube_jump*line, cube_width, cube_height))
    pygame.display.update()


def display_next():
    for line in range(4):
        for cube in range(4):
            if next_lst[line][cube] == 0:
                pygame.draw.rect(win, black, (next_x+cube_jump*cube, next_y+cube_jump*line, cube_width, cube_height))
            elif next_lst[line][cube] == 1:
                pygame.draw.rect(win, blue,(next_x + cube_jump * cube, next_y + cube_jump * line, cube_width, cube_height))
            elif next_lst[line][cube] == 2:
                pygame.draw.rect(win, red,(next_x + cube_jump * cube, next_y + cube_jump * line, cube_width, cube_height))
            elif next_lst[line][cube] == 3:
                pygame.draw.rect(win, yellow,(next_x + cube_jump * cube, next_y + cube_jump * line, cube_width, cube_height))
            elif next_lst[line][cube] == 4:
                pygame.draw.rect(win, orange1,(next_x + cube_jump * cube, next_y + cube_jump * line, cube_width, cube_height))
            elif next_lst[line][cube] == 5:
                pygame.draw.rect(win, orange2,(next_x + cube_jump * cube, next_y + cube_jump * line, cube_width, cube_height))
            elif next_lst[line][cube] == 6:
                pygame.draw.rect(win, bright_blue,(next_x + cube_jump * cube, next_y + cube_jump * line, cube_width, cube_height))
    pygame.display.update()


def game_over():
    global alive
    global time_to_game_over
    if main_lst[0][5] != 0:
        time_to_game_over += clock.tick(30)
        if time_to_game_over > 550:
            alive = False
    else: time_to_game_over = 0


def del_line():
    global lines
    global score
    for i in range(19):
        if 0 not in main_lst[i]:
            score += 10
            lines += 1
            for k in range(i,0,-1):
                for j in range(11):
                    main_lst[k][j] = main_lst[k-1][j]


def del_next():
    for i in range(4):
        for n in range(4):
            next_lst[i][n] = 0


def clear_board():
    global main_lst
    main_lst = [[0 for i in range(11)] for x in range(20)]


def message(msg, color):
    mesg = myFont.render(msg, True, color)
    win.blit(mesg, [win_width / 5, win_height / 2])


# class shape:
class shape:
    def __init__(self):
        self.y = 0
        self.x = 0
        self.random_num = random.choice(range(1, 7))
        self.time_elapsed = 0
        self.time_elapsed_to_finish = 0

    def move_down(self):
        if self.down_restrict():
            self.del_prev()
            self.y += 1

    def finish(self):
        global score
        if not self.down_restrict():
            self.time_elapsed_to_finish += clock.tick(30)
            if self.time_elapsed_to_finish > 300:
                del_next()
                return False
            else: return True
        else: return True


class plus_shape(shape):
    def __init__(self):
        shape.__init__(self)
        self.rotate = 0

    def del_prev(self):
        if self.rotate % 4 == 0:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][6 + self.x] = 0
        if self.rotate % 4 == 1:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[2 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][6 + self.x] = 0
        if self.rotate % 4 == 2:
            main_lst[2 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][6 + self.x] = 0
        if self.rotate % 4 == 3:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[2 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0

    def next(self):
        next_lst[0][2] = self.random_num
        next_lst[1][2] = self.random_num
        next_lst[1][1] = self.random_num
        next_lst[1][3] = self.random_num


    def side_restrict(self,side):
        if side == "right":
            if (self.rotate % 4 == 0 and self.x == 4) or (self.rotate % 4 == 0 and (main_lst[0 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][6 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 1 and self.x == 4) or (self.rotate % 4 == 1 and (main_lst[1 + self.y][6 + self.x+1] != 0 or main_lst[0 + self.y][5 + self.x+1] != 0 or main_lst[2 + self.y][5 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 2 and self.x == 4) or (self.rotate % 4 == 2 and (main_lst[2 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][6 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 3 and self.x == 5) or (self.rotate % 4 == 3 and (main_lst[0 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][5 + self.x+1] != 0 or main_lst[2 + self.y][5 + self.x+1] != 0)):
                return False
            else: return True
        elif side == "left":
            if (self.rotate % 4 == 0 and self.x == -4) or (self.rotate % 4 == 0 and (main_lst[0 + self.y][3 + self.x+1] != 0 or main_lst[1 + self.y][2 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 1 and self.x == -5) or (self.rotate % 4 == 1 and (main_lst[1 + self.y][3 + self.x+1] != 0 or main_lst[0 + self.y][3 + self.x+1] != 0 or main_lst[2 + self.y][3 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 2 and self.x == -4) or (self.rotate % 4 == 2 and (main_lst[2 + self.y][3 + self.x+1] != 0 or main_lst[1 + self.y][2 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 3 and self.x == -4) or (self.rotate % 4 == 3 and (main_lst[0 + self.y][3 + self.x+1] != 0 or main_lst[1 + self.y][2 + self.x+1] != 0 or main_lst[2 + self.y][3 + self.x+1] != 0)):
                return False
            else: return True

    def down_restrict(self):
        if (self.rotate % 4 == 0 and self.y == 17) or (self.rotate % 4 == 0 and (main_lst[1 + self.y+1][5 + self.x] != 0 or main_lst[1 + self.y+1][4 + self.x] != 0 or main_lst[1 + self.y+1][6 + self.x] != 0)):
            return False
        if (self.rotate % 4 == 1 and self.y == 16) or (self.rotate % 4 == 1 and (main_lst[2 + self.y+1][5 + self.x] != 0 or main_lst[1 + self.y+1][6 + self.x] != 0)):
            return False
        if (self.rotate % 4 == 2 and self.y == 16) or (self.rotate % 4 == 2 and (main_lst[2 + self.y+1][5 + self.x] != 0 or main_lst[1 + self.y+1][4 + self.x] != 0 or main_lst[1 + self.y+1][6 + self.x] != 0)):
            return False
        if self.rotate % 4 == 3 and self.y == 16 or (self.rotate % 4 == 3 and (main_lst[2 + self.y+1][5 + self.x] != 0 or main_lst[1 + self.y+1][4 + self.x] != 0)):
            return False
        else: return True

    def rotation_restrict(self):
        if self.rotate % 4 == 0 and (main_lst[1 + self.y+1][5 + self.x] !=0 or self.y == 17):
            return False
        elif self.rotate % 4 == 1 and (main_lst[1 + self.y][5 + self.x-1] !=0 or self.y == 16):
            return False
        elif self.rotate % 4 == 2 and (main_lst[1 + self.y-1][5 + self.x] !=0 or self.y == 16):
            return False
        elif self.rotate % 4 == 3 and (main_lst[1 + self.y][5 + self.x+1] !=0 or self.y == 16):
            return False
        else: return True

    def draw(self):
        if self.finish():
            key_pressed = pygame.key.get_pressed()
            self.time_elapsed += clock.tick(30)
            if self.time_elapsed > 100:
                if key_pressed[pygame.K_RIGHT] and self.side_restrict("right"):
                        self.del_prev()
                        self.x += 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_LEFT] and self.side_restrict("left"):
                        self.del_prev()
                        self.x -= 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_UP] and self.x != 5 and self.x != -5 and self.rotation_restrict() and self.down_restrict():
                        self.del_prev()
                        self.rotate += 1
                        self.time_elapsed = 0
            if self.rotate % 4 == 0:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][6 + self.x] = self.random_num
            if self.rotate % 4 == 1:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[2 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][6 + self.x] = self.random_num
            if self.rotate % 4 == 2:
                main_lst[2 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][6 + self.x] = self.random_num
            if self.rotate % 4 == 3:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[2 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
        else:
            global score
            global shape_num
            global shapes_lst
            shapes_lst.append(random.choice([plus_shape(), O_shape(), I_shape(), J_shape(), L_shape(), S_shape(), Z_shape()]))
            shape_num += 1
            del_line()
            score += 1


class O_shape(shape):
    def __init__(self):
        shape.__init__(self)

    def del_prev(self):
        main_lst[0 + self.y][5 + self.x] = 0
        main_lst[1 + self.y][5 + self.x] = 0
        main_lst[0 + self.y][4 + self.x] = 0
        main_lst[1 + self.y][4 + self.x] = 0

    def next(self):
        next_lst[1][1] = self.random_num
        next_lst[1][2] = self.random_num
        next_lst[2][1] = self.random_num
        next_lst[2][2] = self.random_num

    def side_restrict(self,side):
        if side == "right":
            if self.x == 5 or main_lst[0 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][5 + self.x+1] != 0:
                return False
            else: return True
        elif side == "left":
            if self.x == -4 or main_lst[0 + self.y][4 + self.x-1] != 0 or main_lst[1 + self.y][4 + self.x-1] != 0:
                return False
            else: return True

    def down_restrict(self):
        if self.y == 17 or main_lst[1 + self.y+1][5 + self.x] != 0 or main_lst[1 + self.y+1][4 + self.x] != 0:
            return False
        else: return True

    def draw(self):
        if self.finish():
            key_pressed = pygame.key.get_pressed()
            self.time_elapsed += clock.tick(30)
            if self.time_elapsed > 100:
                if key_pressed[pygame.K_RIGHT] and self.side_restrict("right"):
                        self.del_prev()
                        self.x += 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_LEFT] and self.side_restrict("left"):
                        self.del_prev()
                        self.x -= 1
                        self.time_elapsed = 0
            main_lst[0 + self.y][5 + self.x] = self.random_num
            main_lst[1 + self.y][5 + self.x] = self.random_num
            main_lst[0 + self.y][4 + self.x] = self.random_num
            main_lst[1 + self.y][4 + self.x] = self.random_num
        else:
            global score
            global shape_num
            global shapes_lst
            shapes_lst.append(random.choice([plus_shape(), O_shape(),I_shape(), J_shape(), L_shape(), S_shape(), Z_shape()]))
            shape_num += 1
            del_line()
            score += 1


class I_shape(shape):
    def __init__(self):
        shape.__init__(self)
        self.rotate = 0

    def del_prev(self):
        if self.rotate % 2 == 0:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[0 + self.y][6 + self.x] = 0
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[0 + self.y][3 + self.x] = 0
        if self.rotate % 2 == 1:
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[2 + self.y][4 + self.x] = 0
            main_lst[3 + self.y][4 + self.x] = 0

    def next(self):
        next_lst[1][0] = self.random_num
        next_lst[1][2] = self.random_num
        next_lst[1][1] = self.random_num
        next_lst[1][3] = self.random_num

    def side_restrict(self,side):
        if side == "right":
            if (self.rotate % 2 == 0 and self.x == 4) or (self.rotate % 2 == 0 and main_lst[0 + self.y][6 + self.x+1] != 0):
                return False
            elif (self.rotate % 2 == 1 and self.x == 6) or (self.rotate % 2 == 1 and (main_lst[0 + self.y][4 + self.x+1] != 0 or main_lst[1 + self.y][4 + self.x+1] != 0 or main_lst[2 + self.y][4 + self.x+1] != 0 or main_lst[3 + self.y][4 + self.x+1] != 0)):
                return False
            else: return True
        elif side == "left":
            if (self.rotate % 2 == 0 and self.x == -3) or (self.rotate % 2 == 0 and (main_lst[0 + self.y][3 + self.x-1] != 0)):
                return False
            elif (self.rotate % 2 == 1 and self.x == -4) or (self.rotate % 2 == 1 and (main_lst[0 + self.y][4 + self.x-1] != 0 or main_lst[1 + self.y][4 + self.x-1] != 0 or main_lst[2 + self.y][4 + self.x-1] != 0 or main_lst[3 + self.y][4 + self.x-1] != 0)):
                return False
            else: return True

    def down_restrict(self):
        if (self.rotate % 2 == 0 and self.y == 18) or (self.rotate % 2 == 0 and (main_lst[0 + self.y+1][5 + self.x] != 0 or main_lst[0 + self.y+1][4 + self.x] != 0 or main_lst[0 + self.y+1][6 + self.x] != 0 or main_lst[0 + self.y+1][3 + self.x] != 0)):
            return False
        if (self.rotate % 2 == 1 and self.y == 15) or (self.rotate % 2 == 1 and main_lst[3 + self.y+1][4 + self.x] != 0):
            return False
        else: return True

    def rotation_restrict(self):
        if self.x == -4 or self.x > 4 or self.y > 15:
            return False
        elif self.rotate % 2 == 0 and (main_lst[1 + self.y][4 + self.x] !=0 or main_lst[2 + self.y][4 + self.x] !=0 or main_lst[3 + self.y][4 + self.x] !=0 or self.y  == 17):
            return False
        elif self.rotate % 2 == 1 and (main_lst[0 + self.y][3 + self.x] !=0 or main_lst[0 + self.y][5 + self.x] !=0 or main_lst[0 + self.y][6 + self.x] !=0 or self.y == 16):
            return False
        else: return True

    def draw(self):
        if self.finish():
            key_pressed = pygame.key.get_pressed()
            self.time_elapsed += clock.tick(30)
            if self.time_elapsed > 100:
                if key_pressed[pygame.K_RIGHT] and self.side_restrict("right"):
                        self.del_prev()
                        self.x += 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_LEFT] and self.side_restrict("left"):
                        self.del_prev()
                        self.x -= 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_UP] and self.x != 5 and self.x != -5 and self.rotation_restrict() and self.down_restrict():
                        self.del_prev()
                        self.rotate += 1
                        self.time_elapsed = 0
            if self.rotate % 2 == 0:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[0 + self.y][3 + self.x] = self.random_num
                main_lst[0 + self.y][6 + self.x] = self.random_num
            if self.rotate % 2 == 1:
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[2 + self.y][4 + self.x] = self.random_num
                main_lst[3 + self.y][4 + self.x] = self.random_num
        else:
            global score
            global shape_num
            global shapes_lst
            shapes_lst.append(random.choice([plus_shape(), O_shape(),I_shape(), J_shape(), L_shape(), S_shape(), Z_shape()]))
            shape_num += 1
            del_line()
            score += 1


class J_shape(shape):
    def __init__(self):
        shape.__init__(self)
        self.rotate = 0

    def del_prev(self):
        if self.rotate % 4 == 0:
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][6 + self.x] = 0
            main_lst[0 + self.y][6 + self.x] = 0
        if self.rotate % 4 == 1:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[2 + self.y][5 + self.x] = 0
            main_lst[2 + self.y][4 + self.x] = 0
        if self.rotate % 4 == 2:
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][6 + self.x] = 0
        if self.rotate % 4 == 3:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[2 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0

    def next(self):
        next_lst[1][1] = self.random_num
        next_lst[1][2] = self.random_num
        next_lst[2][3] = self.random_num
        next_lst[1][3] = self.random_num

    def side_restrict(self,side):
        if side == "right":
            if (self.rotate % 4 == 0 and self.x == 4) or (self.rotate % 4 == 0 and (main_lst[0 + self.y][6 + self.x+1] != 0 or main_lst[1 + self.y][6 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 1 and self.x == 5) or (self.rotate % 4 == 1 and (main_lst[0 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][5 + self.x+1] != 0 or main_lst[2 + self.y][5 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 2 and self.x == 4) or (self.rotate % 4 == 2 and (main_lst[0 + self.y][4 + self.x+1] != 0 or main_lst[1 + self.y][6 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 3 and self.x == 5) or (self.rotate % 4 == 3 and (main_lst[0 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][4 + self.x+1] != 0 or main_lst[2 + self.y][4 + self.x+1] != 0)):
                return False
            else: return True
        elif side == "left":
            if (self.rotate % 4 == 0 and self.x == -4) or (self.rotate % 4 == 0 and (main_lst[0 + self.y][4 + self.x-1] != 0 or main_lst[1 + self.y][6 + self.x-1] != 0)):
                return False
            elif (self.rotate % 4 == 1 and self.x == -4) or (self.rotate % 4 == 1 and (main_lst[0 + self.y][5 + self.x-1] != 0 or main_lst[1 + self.y][5 + self.x-1] != 0 or main_lst[2 + self.y][4 + self.x-1] != 0)):
                return False
            elif (self.rotate % 4 == 2 and self.x == -4) or (self.rotate % 4 == 2 and (main_lst[0 + self.y][4 + self.x-1] != 0 or main_lst[1 + self.y][4 + self.x-1] != 0)):
                return False
            elif (self.rotate % 4 == 3 and self.x == -4) or (self.rotate % 4 == 3 and (main_lst[0 + self.y][4 + self.x-1] != 0 or main_lst[1 + self.y][4 + self.x-1] != 0 or main_lst[2 + self.y][4 + self.x-1] != 0)):
                return False
            else: return True

    def down_restrict(self):
        if (self.rotate % 4 == 0 and self.y == 17) or (self.rotate % 4 == 0 and (main_lst[1 + self.y+1][6 + self.x] != 0 or main_lst[0 + self.y+1][5 + self.x] != 0 or main_lst[0 + self.y+1][4 + self.x] != 0)):
            return False
        if (self.rotate % 4 == 1 and self.y == 16) or (self.rotate % 4 == 1 and (main_lst[2 + self.y+1][4 + self.x] != 0 or main_lst[2 + self.y+1][5 + self.x] != 0)):
            return False
        if (self.rotate % 4 == 2 and self.y == 17) or (self.rotate % 4 == 2 and (main_lst[1 + self.y+1][4 + self.x] != 0 or main_lst[1 + self.y+1][5 + self.x] != 0 or main_lst[1 + self.y+1][6 + self.x] != 0)):
            return False
        if self.rotate % 4 == 3 and self.y == 16 or (self.rotate % 4 == 3 and (main_lst[0 + self.y+1][5 + self.x] != 0 or main_lst[2 + self.y+1][4 + self.x] != 0)):
            return False
        else: return True

    def rotation_restrict(self):
        if (self.rotate % 4 == 1 and self.x == 5) or (self.rotate % 4 == 3 and self.x == 5):
            return False
        elif self.rotate % 4 == 0 and (main_lst[1 + self.y][5 + self.x] !=0 or main_lst[2 + self.y][5 + self.x] !=0 or main_lst[2 + self.y][4 + self.x] !=0 or self.y == 17):
            return False
        elif self.rotate % 4 == 1 and (main_lst[0 + self.y][4 + self.x] !=0 or main_lst[1 + self.y][4 + self.x] !=0 or main_lst[1 + self.y][6 + self.x] !=0):
            return False
        elif self.rotate % 4 == 2 and (main_lst[2 + self.y][4 + self.x] !=0 or main_lst[0 + self.y][5 + self.x] !=0 or self.y == 17):
            return False
        elif self.rotate % 4 == 3 and (main_lst[0 + self.y][6 + self.x] !=0 or main_lst[1 + self.y][6 + self.x] !=0):
            return False
        else: return True

    def draw(self):
        if self.finish():
            key_pressed = pygame.key.get_pressed()
            self.time_elapsed += clock.tick(30)
            if self.time_elapsed > 100:
                if key_pressed[pygame.K_RIGHT] and self.side_restrict("right"):
                        self.del_prev()
                        self.x += 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_LEFT] and self.side_restrict("left"):
                        self.del_prev()
                        self.x -= 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_UP] and self.rotation_restrict() and self.down_restrict():
                        self.del_prev()
                        self.rotate += 1
                        self.time_elapsed = 0
            if self.rotate % 4 == 0:
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][6 + self.x] = self.random_num
                main_lst[0 + self.y][6 + self.x] = self.random_num
            if self.rotate % 4 == 1:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[2 + self.y][5 + self.x] = self.random_num
                main_lst[2 + self.y][4 + self.x] = self.random_num
            if self.rotate % 4 == 2:
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][6 + self.x] = self.random_num
            if self.rotate % 4 == 3:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[2 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
        else:
            global score
            global shape_num
            global shapes_lst
            shapes_lst.append(random.choice([plus_shape(), O_shape(), I_shape(), J_shape(), L_shape(), S_shape(), Z_shape()]))
            shape_num += 1
            del_line()
            score += 1


class L_shape(shape):
    def __init__(self):
        shape.__init__(self)
        self.rotate = 0

    def del_prev(self):
        if self.rotate % 4 == 0:
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[0 + self.y][6 + self.x] = 0
        if self.rotate % 4 == 1:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[2 + self.y][5 + self.x] = 0
            main_lst[0 + self.y][4 + self.x] = 0
        if self.rotate % 4 == 2:
            main_lst[0 + self.y][6 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][6 + self.x] = 0
        if self.rotate % 4 == 3:
            main_lst[2 + self.y][5 + self.x] = 0
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[2 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0

    def next(self):
        next_lst[1][1] = self.random_num
        next_lst[1][2] = self.random_num
        next_lst[1][3] = self.random_num
        next_lst[2][1] = self.random_num

    def side_restrict(self,side):
        if side == "right":
            if (self.rotate % 4 == 0 and self.x == 4) or (self.rotate % 4 == 0 and (main_lst[0 + self.y][6 + self.x+1] != 0 or main_lst[1 + self.y][4 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 1 and self.x == 5) or (self.rotate % 4 == 1 and (main_lst[0 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][5 + self.x+1] != 0 or main_lst[2 + self.y][5 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 2 and self.x == 4) or (self.rotate % 4 == 2 and (main_lst[0 + self.y][6 + self.x+1] != 0 or main_lst[1 + self.y][6 + self.x+1] != 0)):
                return False
            elif (self.rotate % 4 == 3 and self.x == 5) or (self.rotate % 4 == 3 and (main_lst[2 + self.y][5 + self.x+1] != 0 or main_lst[1 + self.y][4 + self.x+1] != 0 or main_lst[0 + self.y][4 + self.x+1] != 0)):
                return False
            else: return True
        elif side == "left":
            if (self.rotate % 4 == 0 and self.x == -4) or (self.rotate % 4 == 0 and (main_lst[0 + self.y][4 + self.x-1] != 0 or main_lst[1 + self.y][4 + self.x-1] != 0)):
                return False
            elif (self.rotate % 4 == 1 and self.x == -4) or (self.rotate % 4 == 1 and (main_lst[2 + self.y][5 + self.x-1] != 0 or main_lst[1 + self.y][5 + self.x-1] != 0 or main_lst[0 + self.y][4 + self.x-1] != 0)):
                return False
            elif (self.rotate % 4 == 2 and self.x == -4) or (self.rotate % 4 == 2 and (main_lst[0 + self.y][6 + self.x-1] != 0 or main_lst[1 + self.y][4 + self.x-1] != 0)):
                return False
            elif (self.rotate % 4 == 3 and self.x == -4) or (self.rotate % 4 == 3 and (main_lst[0 + self.y][4 + self.x-1] != 0 or main_lst[1 + self.y][4 + self.x-1] != 0 or main_lst[2 + self.y][4 + self.x-1] != 0)):
                return False
            else: return True

    def down_restrict(self):
        if (self.rotate % 4 == 0 and self.y == 17) or (self.rotate % 4 == 0 and (main_lst[1 + self.y+1][4 + self.x] != 0 or main_lst[0 + self.y+1][5 + self.x] != 0 or main_lst[0 + self.y+1][6 + self.x] != 0)):
            return False
        if (self.rotate % 4 == 1 and self.y == 16) or (self.rotate % 4 == 1 and (main_lst[0 + self.y+1][4 + self.x] != 0 or main_lst[2 + self.y+1][5 + self.x] != 0)):
            return False
        if (self.rotate % 4 == 2 and self.y == 17) or (self.rotate % 4 == 2 and (main_lst[1 + self.y+1][4 + self.x] != 0 or main_lst[1 + self.y+1][5 + self.x] != 0 or main_lst[1 + self.y+1][6 + self.x] != 0)):
            return False
        if self.rotate % 4 == 3 and self.y == 16 or (self.rotate % 4 == 3 and (main_lst[2 + self.y+1][5 + self.x] != 0 or main_lst[2 + self.y+1][4 + self.x] != 0)):
            return False
        else: return True

    def rotation_restrict(self):
        if (self.rotate % 4 == 1 and self.x == 5) or (self.rotate % 4 == 3 and self.x == 5):
            return False
        elif self.rotate % 4 == 0 and (main_lst[1 + self.y][5 + self.x] !=0 or main_lst[2 + self.y][5 + self.x] !=0 or self.y == 17):
            return False
        elif self.rotate % 4 == 1 and (main_lst[0 + self.y][6 + self.x] !=0 or main_lst[1 + self.y][6 + self.x] !=0 or main_lst[1 + self.y][4 + self.x] !=0):
            return False
        elif self.rotate % 4 == 2 and (main_lst[0 + self.y][4 + self.x] !=0 or main_lst[2 + self.y][4 + self.x] !=0 or main_lst[2 + self.y][5 + self.x] !=0 or self.y == 17):
            return False
        elif self.rotate % 4 == 3 and (main_lst[0 + self.y][6 + self.x] !=0 or main_lst[0 + self.y][5 + self.x] !=0):
            return False
        else: return True

    def draw(self):
        if self.finish():
            key_pressed = pygame.key.get_pressed()
            self.time_elapsed += clock.tick(30)
            if self.time_elapsed > 100:
                if key_pressed[pygame.K_RIGHT] and self.side_restrict("right"):
                        self.del_prev()
                        self.x += 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_LEFT] and self.side_restrict("left"):
                        self.del_prev()
                        self.x -= 1
                        self.time_elapsed = 0
                if key_pressed[pygame.K_UP] and self.rotation_restrict() and self.down_restrict():
                        self.del_prev()
                        self.rotate += 1
                        self.time_elapsed = 0
            if self.rotate % 4 == 0:
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[0 + self.y][6 + self.x] = self.random_num
            if self.rotate % 4 == 1:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[2 + self.y][5 + self.x] = self.random_num
                main_lst[0 + self.y][4 + self.x] = self.random_num
            if self.rotate % 4 == 2:
                main_lst[0 + self.y][6 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][6 + self.x] = self.random_num
            if self.rotate % 4 == 3:
                main_lst[2 + self.y][5 + self.x] = self.random_num
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[2 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
        else:
            global score
            global shape_num
            global shapes_lst
            shapes_lst.append(random.choice([plus_shape(), O_shape(), I_shape(), J_shape(), L_shape(), S_shape(), Z_shape()]))
            shape_num += 1
            del_line()
            score += 1


class S_shape(shape):
    def __init__(self):
        shape.__init__(self)
        self.rotate = 0

    def del_prev(self):
        if self.rotate % 2 == 0:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[0 + self.y][6 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
        if self.rotate % 2 == 1:
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[2 + self.y][5 + self.x] = 0

    def next(self):
        next_lst[0][2] = self.random_num
        next_lst[0][3] = self.random_num
        next_lst[1][1] = self.random_num
        next_lst[1][2] = self.random_num

    def side_restrict(self, side):
        if side == "right":
            if (self.rotate % 2 == 0 and self.x == 4) or (self.rotate % 2 == 0 and (main_lst[0 + self.y][6 + self.x + 1] != 0 or main_lst[1 + self.y][5 + self.x + 1] != 0)):
                return False
            elif (self.rotate % 2 == 1 and self.x == 5) or (self.rotate % 2 == 1 and (main_lst[0 + self.y][4 + self.x + 1] != 0 or main_lst[1 + self.y][5 + self.x + 1] != 0 or main_lst[2 + self.y][5 + self.x + 1] != 0)):
                return False
            else:
                return True
        elif side == "left":
            if (self.rotate % 2 == 0 and self.x == -4) or (self.rotate % 2 == 0 and (main_lst[0 + self.y][5 + self.x - 1] != 0 or main_lst[1 + self.y][4 + self.x - 1] != 0)):
                return False
            elif (self.rotate % 2 == 1 and self.x == -4) or (self.rotate % 2 == 1 and (main_lst[2 + self.y][5 + self.x - 1] != 0 or main_lst[1 + self.y][4 + self.x - 1] != 0 or main_lst[0 + self.y][4 + self.x - 1] != 0)):
                return False
            else:
                return True

    def down_restrict(self):
        if (self.rotate % 2 == 0 and self.y == 17) or (self.rotate % 2 == 0 and (main_lst[1 + self.y + 1][5 + self.x] != 0 or main_lst[0 + self.y + 1][6 + self.x] != 0 or main_lst[1 + self.y + 1][4 + self.x] != 0)):
            return False
        if (self.rotate % 2 == 1 and self.y == 16) or (self.rotate % 2 == 1 and (main_lst[1 + self.y + 1][4 + self.x] != 0 or main_lst[2 + self.y + 1][5 + self.x] != 0)):
            return False
        else:
            return True

    def rotation_restrict(self):
        if self.rotate % 4 == 1 and self.x == 5:
            return False
        elif self.rotate % 4 == 0 and (main_lst[0 + self.y][4 + self.x] != 0 or main_lst[2 + self.y][5 + self.x] != 0):
            return False
        elif self.rotate % 4 == 1 and (main_lst[0 + self.y][6 + self.x] != 0 or main_lst[0 + self.y][5 + self.x] != 0):
            return False
        else:
            return True

    def draw(self):
        if self.finish():
            key_pressed = pygame.key.get_pressed()
            self.time_elapsed += clock.tick(30)
            if self.time_elapsed > 100:
                if key_pressed[pygame.K_RIGHT] and self.side_restrict("right"):
                    self.del_prev()
                    self.x += 1
                    self.time_elapsed = 0
                if key_pressed[pygame.K_LEFT] and self.side_restrict("left"):
                    self.del_prev()
                    self.x -= 1
                    self.time_elapsed = 0
                if key_pressed[pygame.K_UP] and self.rotation_restrict() and self.down_restrict():
                    self.del_prev()
                    self.rotate += 1
                    self.time_elapsed = 0
            if self.rotate % 2 == 0:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[0 + self.y][6 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
            if self.rotate % 2 == 1:
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[2 + self.y][5 + self.x] = self.random_num
        else:
            global score
            global shape_num
            global shapes_lst
            shapes_lst.append(random.choice([plus_shape(), O_shape(), I_shape(), J_shape(), L_shape(), S_shape(), Z_shape()]))
            shape_num += 1
            del_line()
            score += 1


class Z_shape(shape):
    def __init__(self):
        shape.__init__(self)
        self.rotate = 0

    def del_prev(self):
        if self.rotate % 2 == 0:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[0 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][6 + self.x] = 0
        if self.rotate % 2 == 1:
            main_lst[0 + self.y][5 + self.x] = 0
            main_lst[1 + self.y][4 + self.x] = 0
            main_lst[1 + self.y][5 + self.x] = 0
            main_lst[2 + self.y][4 + self.x] = 0

    def next(self):
        next_lst[0][1] = self.random_num
        next_lst[0][2] = self.random_num
        next_lst[1][2] = self.random_num
        next_lst[1][3] = self.random_num

    def side_restrict(self, side):
        if side == "right":
            if (self.rotate % 2 == 0 and self.x == 4) or (self.rotate % 2 == 0 and (main_lst[0 + self.y][5 + self.x + 1] != 0 or main_lst[1 + self.y][6 + self.x + 1] != 0)):
                return False
            elif (self.rotate % 2 == 1 and self.x == 5) or (self.rotate % 2 == 1 and (main_lst[0 + self.y][5 + self.x + 1] != 0 or main_lst[1 + self.y][5 + self.x + 1] != 0 or main_lst[2 + self.y][4 + self.x + 1] != 0)):
                return False
            else:
                return True
        elif side == "left":
            if (self.rotate % 2 == 0 and self.x == -4) or (self.rotate % 2 == 0 and (main_lst[0 + self.y][4 + self.x - 1] != 0 or main_lst[1 + self.y][5 + self.x - 1] != 0)):
                return False
            elif (self.rotate % 2 == 1 and self.x == -4) or (self.rotate % 2 == 1 and (main_lst[0 + self.y][5 + self.x - 1] != 0 or main_lst[1 + self.y][4 + self.x - 1] != 0 or main_lst[2 + self.y][4 + self.x - 1] != 0)):
                return False
            else:
                return True

    def down_restrict(self):
        if (self.rotate % 2 == 0 and self.y == 17) or (self.rotate % 2 == 0 and (main_lst[1 + self.y + 1][5 + self.x] != 0 or main_lst[1 + self.y + 1][6 + self.x] != 0 or main_lst[0 + self.y + 1][4 + self.x] != 0)):
            return False
        if (self.rotate % 2 == 1 and self.y == 16) or (self.rotate % 2 == 1 and (main_lst[1 + self.y + 1][5 + self.x] != 0 or main_lst[2 + self.y + 1][4 + self.x] != 0)):
            return False
        else:
            return True

    def rotation_restrict(self):
        if self.rotate % 4 == 1 and self.x == 5:
            return False
        elif self.rotate % 4 == 0 and (main_lst[1 + self.y][4 + self.x] != 0 or main_lst[2 + self.y][4 + self.x] != 0):
            return False
        elif self.rotate % 4 == 1 and (main_lst[0 + self.y][4 + self.x] != 0 or main_lst[1 + self.y][6 + self.x] != 0):
            return False
        else:
            return True

    def draw(self):
        if self.finish():
            key_pressed = pygame.key.get_pressed()
            self.time_elapsed += clock.tick(30)
            if self.time_elapsed > 100:
                if key_pressed[pygame.K_RIGHT] and self.side_restrict("right"):
                    self.del_prev()
                    self.x += 1
                    self.time_elapsed = 0
                if key_pressed[pygame.K_LEFT] and self.side_restrict("left"):
                    self.del_prev()
                    self.x -= 1
                    self.time_elapsed = 0
                if key_pressed[pygame.K_UP] and self.rotation_restrict() and self.down_restrict():
                    self.del_prev()
                    self.rotate += 1
                    self.time_elapsed = 0
            if self.rotate % 2 == 0:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[0 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][6 + self.x] = self.random_num
            if self.rotate % 2 == 1:
                main_lst[0 + self.y][5 + self.x] = self.random_num
                main_lst[1 + self.y][4 + self.x] = self.random_num
                main_lst[1 + self.y][5 + self.x] = self.random_num
                main_lst[2 + self.y][4 + self.x] = self.random_num
        else:
            global score
            global shape_num
            global shapes_lst
            shapes_lst.append(random.choice([plus_shape(), O_shape(), I_shape(), J_shape(), L_shape(), S_shape(), Z_shape()]))
            shape_num += 1
            del_line()
            score += 1


shapes_lst = [random.choice([plus_shape(), O_shape(), I_shape(), L_shape(), S_shape(), Z_shape()]), random.choice([plus_shape(), O_shape(), I_shape(), L_shape(), S_shape(), Z_shape()])]

while run:
    while not alive and run:
        win.fill((200, 200, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # massage here
        message("You Lost! Your Score=" + str(score) + " Press R-Replay Q-Quit", (255, 0, 0))
        if score > High_score:
            High_score = score
            High_score_writer_file = open(path, 'w', newline='')
            High_score_writer = csv.writer(High_score_writer_file)
            High_score_writer.writerow([score])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    alive = True
                    score = 0
                    level = 0
                    lines = 0
                    clear_board()
                    # set up new game here
                elif event.key == pygame.K_q:
                    run = False
    while alive and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.blit(image, (0, 0))
        score_display = myFont.render(str(score), 1, black)
        lines_display = myFont.render(str(lines), 1, black)
        level_display = myFont.render(str(score // 100), 1, black)
        high_score_display = myFont.render(str(int(High_score)), 1, black)
        win.blit(score_display, (230, 202))
        win.blit(lines_display, (230, 252))
        win.blit(level_display, (230, 299))
        win.blit(high_score_display, (205, 445))
        shapes_lst[shape_num + 1].next()
        shapes_lst[shape_num].draw()
        display()
        display_next()
        time_elapsed_since_last_action += clock.tick(30)
        if time_elapsed_since_last_action > time_delay():
            shapes_lst[shape_num].move_down()
            time_elapsed_since_last_action = 0
        if score != 0:
            game_over()
        clock.tick(500)
        pygame.display.update()
    alive = False

pygame.quit()
