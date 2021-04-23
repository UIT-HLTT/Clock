import math
import pygame
import time
import pygame.gfxdraw
from Image import IMG

pygame.init()
pygame.font.init()


# constant
GREY = (15, 15, 15)
GREY_2 = (20, 20, 20)
GREY_3 = (40, 40, 40)
GREY_4 = (25, 25, 25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH_CIRCLE = 13
SCREEN_HEIGHT = SCREEN_WIDTH = 300
FPS = 20
PI = math.pi

# pos of box
x1_pause = 115; x2_pause = 139
y1_pause = 240; y2_pause = 264
x1_reset = 160; x2_reset = 184
y1_reset = 240; y2_reset = 264

x1_minute = 92; x2_minute = 136
y1_minute = 125; y2_minute = 154
x1_second = 162; x2_second = 206
y1_second = 125; y2_second = 154

x1_clock = 1; x2_clock = 42
y1_clock = 4; y2_clock = 21
x1_countdown = 44; x2_countdown = 142
y1_countdown = 4; y2_countdown = 21
x1_countup = 144; x2_countup = 228
y1_countup = 4; y2_countup = 21

x_circle = 149; y_circle = 139
r0 = 76
start_angle = PI/2
stop_angle = PI/2 - PI/180

# crete window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CountdownClock')
pygame.display.set_icon(pygame.image.load('icon.png'))
fpsClock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)


# variables
running = True
type_app = 1 # 1: clock, 2: countdown, 3: countup
counting = False
pause = True
number_input = ""
type_input = None # 1: minute, 2: second
status = 2 # 1: Play, 2: Pause, 3: Reset
total_second = 359
second_run = 1
minute = 0
second = 0

# contruction
font_text = pygame.font.Font(r'data\Segoe_UI.ttf', 14)
font_num = pygame.font.Font(r'data\Segoe_UI_Bold.ttf', 38)
font_time = pygame.font.Font(r'data/Segoe_UI.ttf', 15)
font_ver = pygame.font.Font(r'data\Segoe_UI_Italic.ttf', 13)
bg_1 = IMG(screen, r'data\bg_1.png', 0, 0)
bg_2 = IMG(screen, r'data\bg_2.png', 0, 0)
pause_img = IMG(screen, r'data\pause.png', x1_pause, y1_pause)
play_img = IMG(screen, r'data\play.png', x1_pause, y1_pause)
reset_img = IMG(screen, r'data\reset.png', x1_reset, y1_reset)

# input number
def input_number(event):
    global number_input, type_input

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if type_input == 1:
                type_input = 2
            else:
                type_input = None
        elif event.key == pygame.K_BACKSPACE:
            number_input = number_input[:-1]
        elif 47 < event.key < 58 and int(number_input) <= 9:
            number_input += event.unicode
    
def render_text(display_surface, font, text, color, x, y):
    number_surf = font.render(text, True, color)
    display_surface.blit(number_surf, number_surf.get_rect(center = (x, y)))

def mouse_cursor(mouse_x_, mouse_y_):
    if x1_clock < mouse_x < x2_clock and y1_clock < mouse_y < y2_clock and type_app != 1 or \
       x1_countdown < mouse_x < x2_countdown and y1_countdown < mouse_y < y2_countdown and type_app != 2 or \
       x1_countup < mouse_x < x2_countup and y1_countup < mouse_y < y2_countup and type_app != 3:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    elif x1_minute < mouse_x < x2_minute and y1_minute < mouse_y < y2_minute and counting == False or \
         x1_second < mouse_x < x2_second and y1_second < mouse_y < y2_second and counting == False or \
         x1_reset < mouse_x < x2_reset and y1_reset < mouse_y < y2_reset and (minute + second) != 0 or \
         x1_pause < mouse_x < x2_pause and y1_pause < mouse_y < y2_pause and (minute + second) != 0:
        if type_app == 2 or type_app == 3:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

def menu_bar():
    if type_app == 1:
        pygame.draw.rect(screen, GREY_4, (0, 1, 43, 22), 1)
        pygame.draw.rect(screen, GREY_3, (0, 2, 42, 22))
        render_text(screen, font_text, 'Clock', BLACK, 21, 9)
        render_text(screen,  font_text, 'Countdown', BLACK, 93, 11)
        render_text(screen, font_text, 'Countup', BLACK, 187, 11)
    elif type_app == 2:
        pygame.draw.rect(screen, GREY_4, (43, 1, 100, 22), 1)
        pygame.draw.rect(screen, GREY_3, (44, 2, 98, 22))
        render_text(screen, font_text, 'Clock', BLACK, 21, 11)
        render_text(screen,  font_text, 'Countdown', BLACK, 93, 9)
        render_text(screen, font_text, 'Countup', BLACK, 187, 11)
    elif type_app == 3:
        pygame.draw.rect(screen, GREY_4, (143, 1, 86, 22), 1)
        pygame.draw.rect(screen, GREY_3, (144, 2, 84, 22))
        render_text(screen, font_text, 'Clock', BLACK, 21, 11)
        render_text(screen,  font_text, 'Countdown', BLACK, 93, 11)
        render_text(screen, font_text, 'Countup', BLACK, 187, 9)
        

# loop program
while running:
    if type_app == 1:
        bg_1.render()
    else:
        bg_2.render()
    ver = font_ver.render('2.0', True, BLACK)
    screen.blit(ver, (4, 280))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if x1_clock < mouse_x < x2_clock and y1_clock < mouse_y < y2_clock and type_app != 1:
                    type_app = 1
                    status = 3
                elif x1_countdown < mouse_x < x2_countdown and y1_countdown < mouse_y < y2_countdown and type_app != 2:
                    type_app = 2
                    status = 3
                elif x1_countup < mouse_x < x2_countup and y1_countup < mouse_y < y2_countup and type_app != 3:
                    type_app = 3
                    status = 3
                
                # clock
                if type_app == 1:
                    pass
                # countdown, countup
                else:
                    if counting == False:
                        if x1_minute < mouse_x < x2_minute and y1_minute < mouse_y < y2_minute:
                            type_input = 1
                        elif x1_second < mouse_x < x2_second and y1_second < mouse_y < y2_second:
                            type_input = 2

                    if (minute + second) != 0:
                        if x1_pause < mouse_x < x2_pause and y1_pause < mouse_y < y2_pause:
                                if pause == True:
                                    status = 1
                                elif pause == False:
                                    status = 2

                    if x1_reset < mouse_x < x2_reset and y1_reset < mouse_y < y2_reset:
                        status = 3


        # countdown
        if type_app == 2 or type_app == 3:
            if type_input == 1:
                number_input = str(minute)
                input_number(event)
                if number_input:
                    minute = int(number_input)
                else:
                    minute = 0
            elif type_input == 2:
                number_input = str(second)
                input_number(event)
                if number_input:
                    second = int(number_input)
                else:
                    second = 0

            if status == 1:
                if event.type == pygame.USEREVENT:
                    if type_app == 2:
                        total_second -= 1
                    second_run += 1
    
    # clock
    if type_app == 1:
        pygame.draw.arc(screen, GREY, [62, 74, 176, 176], start_angle, stop_angle, 13)

        hour_c = time.strftime("%H")
        minute_c = time.strftime("%M")

        symbol = font_num.render(':', True, BLACK)
        screen.blit(symbol, (143, 130))
        render_text(screen, font_num, str(hour_c), BLACK, 114, 158)
        render_text(screen, font_num, str(minute_c), BLACK, 184, 158)


    # countdown, countup
    else:
        reset_img.render()
        if status == 1:
            if counting == False and pause == True:
                total_second = minute*60 + second
            counting = True
            pause = False
            type_input = None
        elif status == 2:
            pause = True
        elif status == 3:
            counting = False
            pause = True
            number_input = ""
            type_input = None
            status = 2
            total_second = 359
            second_run = 1
            minute = 0
            second = 0
            start_angle = PI/2
            stop_angle = PI/2 - PI/180

        symbol = font_num.render(':', True, BLACK)
        screen.blit(symbol, (143, 112))
        render_text(screen, font_num, str(minute), BLACK, 114, 140)
        render_text(screen, font_num, str(second), BLACK, 184, 140)
        if type_input == 1:
            render_text(screen, font_num, str(minute), GREY_2, 114, 140)
        elif type_input == 2:
            render_text(screen, font_num, str(second), GREY_2, 184, 140)

        if pause:
            play_img.render()
        else:
            pause_img.render()

    # countdown
    if type_app == 2:
        r0 = 76
        stop_angle = PI/2 - second_run*2*PI/(total_second + second_run)
        pygame.draw.arc(screen, GREY, [62, 52, 176, 176], start_angle, stop_angle, 13)

        if counting:
            minute = total_second // 60
            second = total_second % 60
            if total_second == 0:
                status = 3
    # countup
    elif type_app == 3:
        r0 = 76
        stop_angle = -90 + second_run*360//total_second
        for i in range(WIDTH_CIRCLE):
            pygame.gfxdraw.arc(screen, x_circle, y_circle, r0 + i, -90, stop_angle, GREY)

        if counting:
            minute = second_run // 60
            second = second_run % 60
            if second_run == total_second:
                status = 3

            time_countup = str(total_second//60) + ' : ' + str(total_second%60)
        else:
            time_countup = '0 : 0'
        render_text(screen, font_time, time_countup, BLACK, 25, 34)


    mouse_cursor(mouse_x, mouse_y)
    menu_bar()

    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()