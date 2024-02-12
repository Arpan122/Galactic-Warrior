import pygame
import random
import pyperclip
from pygame import mixer
import time
from button import Button
from cryptography.fernet import Fernet

pygame.init()

# Screen variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF, 16)
pygame.display.set_caption('Galactic Warrior')
pygame.display.set_icon(pygame.image.load("assets/img/player/fighter2.png").convert_alpha())
last_time = time.time()

bg = pygame.image.load('assets/img/bg.png').convert_alpha()

# Game Variables
score = 0
with open('assets/key.key', 'rb') as file:
    key = file.read()
fer = Fernet(key)
with open("assets/high_score.txt", "r") as file:
    high_score = file.read()
    high_score = fer.decrypt(high_score.encode()).decode()
settings = False
SCROLL_THRESH = 400
scroll = [0, 0]
scroll_spd = [0, 0]
menu = True
credit = False
info = False
updates = False
choose_ship = False
game = 1
player = None
mouseClicked = False
level_difficulty = 0
DIFICULTY_ADDER = 15
target_difficulty = 50
level = 1
level_done = False
fort_health = 5000
fort_max = 5000
run_i = 0
spawn_delay = 1.5
# Upgrade Levels
spd_lvl = 1
ammo_lvl = 1
reload_lvl = 1
delay_lvl = 1
upgrade_page = 1
info_page = 1

# Music
fx_group = [
    mixer.Sound("assets/music/boom1.wav"),
    mixer.Sound("assets/music/laser.wav"),
    mixer.Sound("assets/music/laser1.wav"),
    mixer.Sound("assets/music/thruster-short.wav")
]
mixer.init()
mixer.music.load("assets/music/background.wav")
mixer.music.play(-1, 0.0)
mixer.music.set_volume(.8)

player1 = pygame.image.load('assets/img/player/blueships1.png').convert_alpha()
player2 = pygame.image.load('assets/img/player/fighter2.png').convert_alpha()
player3 = pygame.image.load('assets/img/player/freighter.png').convert_alpha()
player1 = pygame.transform.scale(player1, (100, 100))
player2 = pygame.transform.scale(player2, (100, 100))
player3 = pygame.transform.scale(player3, (75, 150))

enemies_list = [
    pygame.image.load('assets/img/enemies/scout.png').convert_alpha(),
    pygame.image.load('assets/img/enemies/bomber.png').convert_alpha(),
    pygame.image.load('assets/img/enemies/battleship.png').convert_alpha(),
    pygame.image.load('assets/img/enemies/cruiser.png').convert_alpha(),
    pygame.image.load('assets/img/enemies/mothership.png').convert_alpha()
]

bullets = [pygame.image.load('assets/img/bullets/laser_blue.png').convert_alpha(),
           pygame.image.load('assets/img/bullets/cannon.png').convert_alpha(),
           pygame.image.load('assets/img/bullets/rocket.png').convert_alpha()]

font70 = pygame.font.SysFont('Futura', 70)
font30 = pygame.font.SysFont('Futura', 30)
font20 = pygame.font.SysFont('Futura', 25)

# Button Images
# Page 1
cannon_img = pygame.image.load('assets/img/buttons/cannon_btn.png').convert_alpha()
rocket_img = pygame.image.load('assets/img/buttons/rockets.png').convert_alpha()
ship_spd_img = pygame.image.load('assets/img/buttons/Ship_spd_btn.png').convert_alpha()
ammo_img = pygame.image.load('assets/img/buttons/Ammo_btn.png').convert_alpha()
reload_img = pygame.image.load('assets/img/buttons/Reload_btn.png').convert_alpha()
delay_img = pygame.image.load('assets/img/buttons/delay_btn.png').convert_alpha()
# Page 2
repair_img = pygame.image.load('assets/img/buttons/repair_btn.png').convert_alpha()
double_laser_img = pygame.image.load('assets/img/buttons/double_laser.png').convert_alpha()
triple_laser_img = pygame.image.load('assets/img/buttons/triple_laser.png').convert_alpha()
fort_increase = pygame.image.load('assets/img/buttons/health.png').convert_alpha()
ship_max_increase = pygame.image.load('assets/img/buttons/ship_health.png').convert_alpha()
ship_rep_img = pygame.image.load('assets/img/buttons/ship_rep.png').convert_alpha()
# Utility
back_img = pygame.image.load('assets/img/buttons/back_btn.png').convert_alpha()
upgrade_img = pygame.image.load('assets/img/buttons/upgrade_btn.png').convert_alpha()
pg_img = pygame.image.load('assets/img/buttons/page_btn.png').convert_alpha()
pgbk_img = pygame.transform.flip(pg_img, True, False)
play_img = pygame.image.load('assets/img/buttons/play_btn.png').convert_alpha()
info_img = pygame.image.load('assets/img/buttons/info_btn.png').convert_alpha()
credits_img = pygame.image.load('assets/img/buttons/credits_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/img/buttons/restart_btn.png').convert_alpha()
settings_img = pygame.image.load('assets/img/buttons/options.png').convert_alpha()
quit_img = pygame.image.load("assets/img/buttons/exit_btn.png").convert_alpha()

# Buttons
# Page 1
cannon_btn = Button(100, 125, cannon_img, 0.5)
rockets_btn = Button(100, 200, rocket_img, 0.5)
ship_spd_btn = Button(100, 275, ship_spd_img, 0.5)
ammo_btn = Button(100, 350, ammo_img, 0.5)
reload_btn = Button(100, 350 + 75, reload_img, 0.5)
delay_btn = Button(100, 350 + 150, delay_img, 0.5)
# Page 2
repair_btn = Button(100, 125, repair_img, 0.5)
double_laser_btn = Button(100, 200, double_laser_img, 0.5)
triple_laser_btn = Button(100, 200, triple_laser_img, 0.5)
fort_max_btn = Button(100, 275, fort_increase, 0.5)
ship_max_btn = Button(100, 350, ship_max_increase, 0.5)
ship_rep_btn = Button(100, 350 + 75, ship_rep_img, 0.5)
# Utility
upgrade_btn = Button(740, 540, upgrade_img, 0.5)
page_btn = Button(25, 550, pg_img, 0.70)
page_back_btn = Button(25, 550, pgbk_img, 0.70)
page_btn2 = Button(85, 550, pg_img, 0.5)
page_back_btn2 = Button(15, 550, pgbk_img, 0.5)
back_btn = Button(740, 540, back_img, 0.5)
play_btn = Button(100, 225, play_img, 0.75)
credits_btn = Button(100, 350, credits_img, .75)
info_btn = Button(100, 475, info_img, 0.75)
restart_btn = Button(300, 200, restart_img, .75)
settings_btn = Button(740, 10, settings_img, .5)
quit_btn = Button(300, 325, quit_img, .75)


# Draw text
def text(txt, font, text_col, x, y):
    img = font.render(txt, True, text_col)
    screen.blit(img, (x, y))

def wait(current_time, wait_time):
    ct = current_time
    if pygame.time.get_ticks() - ct >= wait_time * 1000:
        return True
    else:
        return False


class Particle_group:
    def __init__(self):
        self.particle_group = list()
    def update(self):
        if self.particle_group:
            for p in self.particle_group:
                p[0][1] += (p[2][1] * dt) - scroll_spd[1]
                p[0][0] += p[2][0] * dt - scroll_spd[0]
                p[1] -= 0.2 * dt
                self.del_particles(p)
                pygame.draw.circle(screen, pygame.Color("Orange"), p[0], p[1])
    def add_particles(self, pos_x: int, pos_y: int, direction: list):
        radius = 10
        particle_circle = [[pos_x, pos_y], radius, direction]
        self.particle_group.append(particle_circle)
    def del_particles(self, p):
        if p[1] <= 0 or (p[0][0] >= SCREEN_WIDTH or p[0][0] <= 0 or p[0][1] <= 0 or p[0][1] >= SCREEN_HEIGHT):
            self.particle_group.remove(p)


# Player class
class Player:
    def __init__(self, x, y, type="fighter"):
        self.type = type
        if self.type == "fighter":
            self.img = player1
            self.lasers = 2
            self.cannon_able = False
            self.cannon_status = "Not unlocked"
            self.rockets = 0
            self.spd = 5
            self.max_ammo = 40
            self.ammo = self.max_ammo
            self.reload = .2
            self.max_health = 500
            self.health = self.max_health
            self.cannon_reload = 5
        elif self.type == "fighter-type2":
            self.img = player2
            self.lasers = 1
            self.cannon_able = True
            self.cannon_status = "Ready"
            self.rockets = 0
            self.spd = 4
            self.max_ammo = 50
            self.ammo = self.max_ammo
            self.reload = .4
            self.max_health = 750
            self.health = self.max_health
            self.cannon_reload = 5
        elif type == "heavy-boi":
            self.img = player3
            self.lasers = 1
            self.cannon_able = True
            self.cannon_status = "Ready"
            self.rockets = 12
            self.spd = 3
            self.max_ammo = 70
            self.ammo = self.max_ammo
            self.reload = .5
            self.max_health = 1250
            self.health = self.max_health
            self.cannon_reload = 3
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.px = self.rect.centerx
        self.py = y
        self.dx = 0
        self.dy = 0
        self.last_rld = pygame.time.get_ticks()
        self.laser = False
        self.cannon = False
        self.rocket_r = False
        self.cannon = False
        self.cannon_time = None
        self.money = 0

    def show_health(self):
        health_bar = HealthBar(self.rect.x, self.rect.bottom + 10, self.img.get_width(), 7, self.health, self.max_health)
        health_bar.update(self.health)

    def update(self):
        global game
        self.move()
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0
            game = -1

        if self.ammo < self.max_ammo and wait(self.last_rld, self.reload):
            self.ammo += 1
            self.last_rld = pygame.time.get_ticks()
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo

    def shoot(self, key):
        if key == 'c':
            fx_group[2].play()
            bullet = Bullet(self.rect.centerx, self.rect.top, "cannon")
            cannon_group.add(bullet)
        elif key == 'l':
            fx_group[1].play()
            if self.lasers == 1:
                bullet = Bullet(self.rect.centerx, self.rect.centery - 10)
                laser_group.add(bullet)
            elif self.lasers == 2:
                bullet = Bullet(self.rect.left + 17, self.rect.centery)
                bullet2 = Bullet(self.rect.right - 17, self.rect.centery)
                laser_group.add(bullet, bullet2)
            elif self.lasers == 3:
                if self.type == 'fighter':
                    bullet = Bullet(self.rect.left, self.rect.centery)
                    bullet2 = Bullet(self.rect.right, self.rect.centery)
                else:
                    bullet = Bullet(self.rect.left + 17, self.rect.centery)
                    bullet2 = Bullet(self.rect.right - 17, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                laser_group.add(bullet, bullet2, bullet3)
        elif key == 'r':
            fx_group[3].play()
            rocket = Bullet(self.rect.centerx, self.rect.centery, "rocket")
            rocket_group.add(rocket)

    def move(self):
        global scroll, scroll_spd
        self.dx = 0
        self.dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.laser == False:
            self.laser = True
            if self.lasers == 1 and self.ammo >= 2:
                self.ammo -= 2
                self.shoot('l')
            elif self.lasers == 2 and self.ammo >= 3:
                self.ammo -= 3
                self.shoot('l')
            elif self.lasers == 3 and self.ammo >= 4:
                self.ammo -= 4
                self.shoot('l')
        elif key[pygame.K_SPACE] == False:
            self.laser = False

        if key[pygame.K_c] and self.cannon == False and self.cannon_able:
            self.cannon = True
            self.cannon_time = pygame.time.get_ticks()
            self.shoot('c')

        if self.cannon == True and self.cannon_able:
            self.cannon_status = "Reloading"
            print(self.cannon_time, self.cannon_reload, pygame.time.get_ticks())
            if wait(self.cannon_time, self.cannon_reload):
                self.cannon_status = "Ready"
                self.cannon = False

        if key[pygame.K_r] and self.rocket_r == False and self.rockets > 0:
            self.rockets -= 1
            self.shoot('r')
            self.rocket_r = True
        elif key[pygame.K_r] == False:
            self.rocket_r = False

        if key[pygame.K_d]:
            self.dx = self.spd * dt
        elif key[pygame.K_a]:
            self.dx = self.spd * dt * -1
        if key[pygame.K_w]:
            self.dy = self.spd * dt * -1
        if key[pygame.K_s]:
            self.dy = self.spd * dt

        self.px += self.dx
        self.py += self.dy
        if self.px < SCROLL_THRESH:
            self.rect.centerx += self.dx
            scroll_spd[0] = 0
        elif self.px > SCREEN_WIDTH * 2 - SCROLL_THRESH:
            self.rect.centerx = self.px - SCREEN_WIDTH
            scroll_spd[0] = 0
        else:
            self.rect.centerx = SCROLL_THRESH
            scroll_spd[0] = self.dx

        if scroll[1] >= 0 and key[pygame.K_s]:
            scroll_spd[1] = 0
        elif scroll[1] <= -600 and key[pygame.K_w]:
            scroll_spd[1] = 0
        else:
            scroll_spd[1] = self.dy

        if self.rect.right >= 800:
            self.rect.right = 800
        elif self.rect.left <= 0:
            self.rect.left = 0

        if self.px >= 1600 - self.rect.width//2:
            self.px = 1600 - self.rect.width//2
        elif self.px <= 0 + self.rect.width//2:
            self.px = 0 + self.rect.width//2
        if self.py <= -300:
            self.py = -300
        elif self.py >= 300:
            self.py = 300

    def draw(self):
        screen.blit(self.img, self.rect)
        self.show_health()


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type="laser"):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if self.type == "laser":
            self.image = pygame.image.load("assets/img/bullets/laser_blue.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(65 * 0.75), int(121 * 0.75)))
        elif self.type == "cannon":
            self.image = pygame.image.load("assets/img/bullets/cannon.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 100))
        elif self.type == "rocket":
            self.image = pygame.image.load("assets/img/bullets/rocket.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(50 * 0.5), int(100 * 0.65)))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.px = x + scroll[0]
        self.py = y + scroll[1]
        self.speed = 9

    def update(self):
        global scroll, scroll_spd
        self.py -= (self.speed * dt)
        self.rect.bottom = self.py - scroll[1]
        self.rect.centerx = self.px - scroll[0]

        if self.rect.y <= -1300 + scroll[1]:
            self.kill()
        if self.type == "rocket":
            particles.add_particles(self.rect.centerx, self.rect.centery + 30, [random.randint(-15, 15)/10, 1])
        if self.rect.x <= SCREEN_WIDTH and self.rect.right >= 0 and self.rect.bottom >= 0 and self.rect.y <= SCREEN_HEIGHT:
            screen.blit(self.image, self.rect)


# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, px, py, type="scout"):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if self.type == "scout":
            self.img = pygame.image.load('assets/img/enemies/scout.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, (50, 100))
            self.health = 75
            self.max_health = 75
            self.spd = 3
        elif self.type == "heavy-cruiser":
            self.img = pygame.image.load('assets/img/enemies/cruiser.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, (175, 125 * 1.75))
            self.health = 500
            self.max_health = 500
            self.spd = 1.5
        elif self.type == "bomber":
            self.img = pygame.image.load('assets/img/enemies/bomber.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, (60, 85))
            self.health = 120
            self.max_health = 120
            self.spd = 2.4
        elif self.type == "battleship":
            self.img = pygame.image.load('assets/img/enemies/battleship.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, (125, 125))
            self.health = 300
            self.max_health = 300
            self.spd = 1.8
        elif self.type == 'mothership':
            self.img = pygame.image.load('assets/img/enemies/mothership.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, (400, 400))
            self.health = 800
            self.max_health = 800
            self.spd = 1.2

        self.image = pygame.transform.rotate(self.img, 180)
        self.px = px
        self.py = py
        self.tx = px
        self.rect = self.img.get_rect()
        self.rect.centerx = px - scroll[0]
        self.rect.centery = py - scroll[1]
        self.killed = False
        self.parDone = 0
        self.time = None
        self.px += self.rect.width//2

    def update(self):
        global score
        if self.health <= 0:
            self.killed = True
        if not self.killed:
            self.move()
            self.rect.centerx = self.px - scroll[0]
            self.rect.centery = self.py - scroll[1]
            
            if self.rect.x <= SCREEN_WIDTH and self.rect.right >= 0 and self.rect.bottom >= 0 and self.rect.y <= SCREEN_HEIGHT:
                self.show_bar()
                screen.blit(self.image, self.rect)
            if pygame.sprite.spritecollide(self, laser_group, True):
                self.health -= 35
            if pygame.sprite.spritecollide(self, cannon_group, True):
                self.health -= 100
            if pygame.sprite.spritecollide(self, rocket_group, True):
                self.health -= 200
            if self.rect.colliderect(player.rect):
                player.health -= self.max_health // 10
                self.health -= 10
        elif self.killed:
            score += self.max_health
            player.money += self.max_health
            fx_group[0].play()
            self.kill()

    def move(self):
        global scroll_spd, fort_health
        self.py += self.spd * dt

        if self.rect.top >= 600 - scroll[1]:
            fort_health -= self.health
            self.kill()

    def show_bar(self):
        health_bar = HealthBar(self.rect.left, self.rect.top - 10, self.image.get_width(), 5, self.health,
                               self.max_health)
        health_bar.update(self.health)


# Health Bar
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health, maxHealth):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = maxHealth

    def update(self, health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width * ratio, self.height))


# Minimap class
class Minimap(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_group):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.enemy_grp = enemy_group
        self.rect = pygame.Rect(0, 0, 160 // 2, 120 // 2)
        self.rect.centerx = 50

    def update(self):
        self.p_circle = [player.px // 10 + 10, player.py // 10 + 525]
        self.rect.centery = self.p_circle[1]
        if self.p_circle[0] >= 10 + int(160 * (1 / 4)) and self.p_circle[0] <= 10 + int(160 * (3 / 4)):
            self.rect.centerx = self.p_circle[0]

        if self.rect.x < 10:
            self.rect.x = 10
        elif self.rect.right > 170:
            self.rect.right = 170

        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, 164, 124), border_radius=2)
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, 160, 120), border_radius=2)  # Background

        pygame.draw.rect(screen, (150, 150, 150), self.rect, 3)  # Screen pos
        r = 0
        for enemy in self.enemy_grp:
            if enemy.type == "scout":
                r = 5
            elif enemy.type == "heavy-cruiser":
                r = 8
            elif enemy.type == "bomber":
                r = 6
            elif enemy.type == "battleship":
                r = 10
            elif enemy.type == 'mothership':
                r = 15

            pygame.draw.circle(screen, (255, 0, 0),
                                   (((enemy.px // 10) + 12.5), (enemy.py // 12) + 530 - r), r)
        #Player location on minimap
        pygame.draw.circle(screen, (0, 0, 255), self.p_circle, 5)


# Slider
class Slider:
    def __init__(self, x, y, width, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.slider_selected = False
        self.slider_width = self.width
        self.body = pygame.Rect(self.x, self.y, self.width, 15)
        self.slider_circle = pygame.Rect(self.body.right - (30 // 2),
                                         self.body.centery - (30 // 2), 30,
                                         30)
        self.rect = pygame.Rect(self.x, self.y - 7.5, width, 30)

    def update(self):
        pygame.draw.rect(screen, (150, 150, 150), self.body, border_radius=10)
        pygame.draw.ellipse(screen, (90, 90, 90), self.slider_circle)
        pygame.draw.ellipse(screen, (10, 10, 10), self.slider_circle, 3)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and mouseClicked != True:
            if pygame.mouse.get_pressed()[0] == 1:
                self.slider_selected = True

        if self.slider_selected:
            self.slider_circle.centerx = mouse_pos[0]
            if pygame.mouse.get_pressed()[0] == 0:
                self.slider_selected = False

        if self.slider_circle.centerx < self.body.left:
            self.slider_circle.centerx = self.body.left
        elif self.slider_circle.centerx > self.body.right:
            self.slider_circle.centerx = self.body.right


# Credits screen
def credits():
    global credit
    font70 = pygame.font.SysFont('Futura', 70)
    font20 = pygame.font.SysFont('Futura', 25)
    coral = pygame.Color("Coral")
    screen.blit(bg, (0, 0))
    back_btn.update(screen, mouseClicked)
    if back_btn.action:
        credit = False
    text("CREDITS", font70, coral, 300, 50)
    text("Blue type 1 fighter and freighter", font20, coral, 10, 110)
    text("If any issues in copyright or bugs, please DM me on discord at God_Avatar68(#4746)", font20, coral, 10,
         260)
    text("Click the links to copy them to the clipboard", font20, coral, 10,
         290)
    text("By MillionthVector (millionthvector.blogspot.com/p/free-sprites.html)", font20, coral, 10, 130)
    text("Enemy images by Skorpio (opengameart.org/content/space-ship-construction-kit)", font20, coral, 10,
        170)
    text("Laser and cannon images by Rawdanitsu (opengameart.org/content/lasers-and-beams)", font20, coral, 10,
        200)
    text("Background music by ZakharValaha (pixabay.com/music/ambient-drone-space-main-9706)", font20, coral, 10,
        230)

    t1 = pygame.Rect(10, 130, 780, 20)
    t2 = pygame.Rect(10, 170, 780, 20)
    t3 = pygame.Rect(10, 200, 780, 20)
    t4 = pygame.Rect(10, 230, 780, 20)
    mouse_pos = pygame.mouse.get_pos()
    if t1.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if pygame.mouse.get_pressed()[0] == 1 and mouseClicked != True:
            pyperclip.copy("http://millionthvector.blogspot.com/p/free-sprites.html")
    elif t2.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if pygame.mouse.get_pressed()[0] == 1 and mouseClicked != True:
            pyperclip.copy("https://opengameart.org/content/space-ship-construction-kit")
    elif t3.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if pygame.mouse.get_pressed()[0] == 1 and mouseClicked != True:
            pyperclip.copy("https://opengameart.org/content/lasers-and-beams")
    elif t4.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if pygame.mouse.get_pressed()[0] == 1 and mouseClicked != True:
            pyperclip.copy("https://pixabay.com/music/ambient-drone-space-main-9706/")
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Information screen
def info_screen():
    global info_page, info
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    text("INFORMATION", font70, pygame.Color('Coral'), 250, 50)
    back_btn.update(screen, mouseClicked)
    if back_btn.action:
        info = False
    if info_page > 1:
        page_back_btn2.update(screen, mouseClicked)
        if page_back_btn2.action:
            info_page -= 1
    if info_page < 5:
        page_btn2.update(screen, mouseClicked)
        if page_btn2.action:
            info_page += 1

    if info_page == 1:
        text("The aim of the game is to stop the astrodian empire from destoying your fortress.", font20,
             pygame.Color("Coral"), 50, 195)
        text("Use your weapons to destory the astrodian forces.", font20,
             pygame.Color("Coral"), 50, 225)
        text("Use your radar in the bottom left to find the enemy ships.", font20,
             pygame.Color("Coral"), 50, 255)
        text("W, S, A, D keys to move forward, backward, left and right respectively", font20,
             pygame.Color("Coral"), 50, 285)
        text("Space Bar to fire laser", font20,
             pygame.Color("Coral"), 50, 315)
        text("C to fire the cannon.", font20,
             pygame.Color("Coral"), 50, 345)
        text("R to fire rockets.", font20,
             pygame.Color("Coral"), 50, 375)
        text("You can upgrade your ship for unlocking cannons, increasing health and much more.", font20,
             pygame.Color("Coral"), 50, 405)
    elif info_page == 2:
        text("You can choose between 3 ships:", font30, pygame.Color('Coral'), 100, 150)

        screen.blit(player1, (100 - 15, 220))
        screen.blit(player2, (370 - 15, 220))
        screen.blit(player3, (640 - 15, 220 - 20))

        text("The type-1 fighter can", font20, pygame.Color('Coral'), 60 - 15, 345)
        text("shoot 2 lasers and is fast ", font20, pygame.Color('Coral'), 50 - 15, 370)
        text("but has no cannons or", font20, pygame.Color('Coral'), 60 - 15, 395)
        text("rockets", font20, pygame.Color('Coral'), 115 - 15, 395 + 25)

        text("The type-2 fighter shoots", font20, pygame.Color('Coral'), 320 - 15, 345)
        text("1 laser and is slower but", font20, pygame.Color('Coral'), 320 - 15, 370)
        text("but has a cannon", font20, pygame.Color('Coral'), 350 - 15, 395)
        text("and more health", font20, pygame.Color('Coral'), 355 - 15, 395 + 25)

        text("The freighter has alot", font20, pygame.Color('Coral'), 590 - 15, 445 - 70)
        text("of health and has a", font20, pygame.Color('Coral'), 605 - 15, 470 - 70)
        text("cannon and 12 rockets", font20, pygame.Color('Coral'), 590 - 15, 495 - 70)
        text("but is very slow", font20, pygame.Color('Coral'), 615 - 15, 520 - 70)
    elif info_page == 3:
        text("There are many enemies:", font30, pygame.Color('Coral'), 100, 150)
        list_of_enemies = [enemies_list[0],
                           enemies_list[1],
                           enemies_list[2]
                           ]
        say = [["SCOUT", "It's fast but has 75"],
               ["BOMBER", "Slower than the scout but has 120 health"],
               ["BATTLESHIP", "Much slower than a bomber but has 300 health. Appears at wave 10"]]
        for i, j in enumerate(list_of_enemies):
            img = pygame.transform.scale(j, (100, 100))
            screen.blit(img, (50, (i * 135) + 170))
        for j, i in enumerate(say):
            text(i[0], font30, pygame.Color("Coral"), 175, (j * 135) + 195)
            text(i[1], font20, pygame.Color("Coral"), 175, (j * 135) + 225)
    elif info_page == 4:
        list_of_enemies = [enemies_list[-2],
                           enemies_list[-1]
                           ]
        say = [["CRUISER", "It has 500 health and is very, very slow. Appears at wave 20"],
               ["MOTHERSHIP", "It has 800 health and is EXTREMELY slow. Appears at wave 30"]]

        for i, j in enumerate(list_of_enemies):
            img = pygame.transform.scale(j, (100, 100))
            screen.blit(img, (50, (i * 150) + 170))
        for j, i in enumerate(say):
            text(i[0], font30, pygame.Color("Coral"), 175, (j * 150) + 195)
            text(i[1], font20, pygame.Color("Coral"), 175, (j * 150) + 225)
    elif info_page == 5:
        say = [["LASER", "Your normal attack. You can have 1, 2 or even 3 shooting at the same time."],
               ["CANNON", "Powerful plasma cannon doing 100 damage"],
               ["MISSILE", "Good ol' missiles. They deal 200 damage."]]
        for i, j in enumerate(bullets):
            img = pygame.transform.scale(j, (50, 100))
            screen.blit(img, (50, (i * 135) + 170))
        for j, i in enumerate(say):
            text(i[0], font30, pygame.Color("Coral"), 175, (j * 135) + 195)
            text(i[1], font20, pygame.Color("Coral"), 175, (j * 135) + 225)
        text("Deals 35 damage.", font20, pygame.Color("Coral"), 175, 245)


# Choose your ship
def choose():
    global player, game, menu, reset, choose_ship
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    rect_list = [
        [pygame.Rect(75, 200, 150, 200), 1],
        [pygame.Rect(325, 200, 150, 200), 2],
        [pygame.Rect(575, 200, 150, 200), 3]
    ]
    text("CHOOSE YOUR SHIP", font70, pygame.Color('Coral'), 150, 50)
    for i in rect_list:
        pygame.draw.rect(screen, pygame.Color("Grey"), i[0])
        pygame.draw.rect(screen, pygame.Color("Black"), [i[0].x - 4, i[0].y - 4, i[0].width + 4, i[0].height + 4], 4)
        screen.blit(player1, (100, 240))
        screen.blit(player2, (350, 240))
        screen.blit(player3, (587.5 + 25, 220))
        text("Type-1 fighter", font30, pygame.Color(0, 0, 0), 80, 350)
        text("Type-2 fighter", font30, pygame.Color(0, 0, 0), 330, 350)
        text("Freighter", font30, pygame.Color(0, 0, 0), 605, 375)
        if i[0].collidepoint(mouse_pos) and mouseClicked == False:
            if i[1] == 1 and pygame.mouse.get_pressed()[0] == 1:
                player = Player(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
                game = 1
                menu = False
                reset = False
            elif i[1] == 2 and pygame.mouse.get_pressed()[0] == 1:
                player = Player(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, "fighter-type2")
                game = 1
                menu = False
                reset = False
            elif i[1] == 3 and pygame.mouse.get_pressed()[0] == 1:
                player = Player(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, "heavy-boi")
                game = 1
                menu = False
                reset = False
    back_btn.update(screen, mouseClicked)
    if back_btn.action:
        choose_ship = False


# Main Menu
def main_menu():
    global menu, game, info, credit, choose_ship, mouseClicked
    screen.fill((0, 0, 0))
    player_dummy = player2
    enemy_dummy = enemies_list[0]
    enemy_dummy = pygame.transform.flip(enemy_dummy, False, True)
    enemy_dummy = pygame.transform.scale(enemy_dummy, (75, 125))
    bullet = bullets[0]
    bullet = pygame.transform.scale(bullet, (int(65 * 0.75), int(121 * 0.75)))
    screen.blit(bg, (0, 0))
    screen.blit(player_dummy, (600, 425))
    screen.blit(enemy_dummy, (610, 175))
    screen.blit(bullet, (625, 325))
    text("GALACTIC WARRIOR", font70, pygame.Color('Coral'), 150, 50)
    play_btn.update(screen, mouseClicked)
    credits_btn.update(screen, mouseClicked)
    info_btn.update(screen, mouseClicked)
    if play_btn.action and mouseClicked == False:
        choose_ship = True
    elif credits_btn.action and mouseClicked == False:
        credit = True
    elif info_btn.action and mouseClicked == False:
        info = True


# Settings
def options():
    global settings
    screen.blit(bg, (0, 0))
    text("OPTIONS", font70, pygame.Color("Coral"), 300, 50)
    sfx_bar.update()
    music_bar.update()
    text("SFX VOLUME", font30, pygame.Color("Coral"), sfx_bar.x - 150, sfx_bar.y)
    text("MUSIC VOLUME", font30, pygame.Color("Coral"), music_bar.x - 175, music_bar.y)
    rect1 = pygame.Rect(sfx_bar.body.right + 50, sfx_bar.rect.y - 16, 50, 50)
    rect2 = pygame.Rect(music_bar.body.right + 50, music_bar.rect.y - 16, 50, 50)
    fx_ratio = (sfx_bar.slider_circle.centerx - sfx_bar.body.x) / sfx_bar.body.width
    bg_ratio = (music_bar.slider_circle.centerx - music_bar.body.x) / music_bar.body.width
    for fx in fx_group:
        fx.set_volume(fx_ratio)
    mixer.music.set_volume(bg_ratio * 0.3)
    pygame.draw.rect(screen, pygame.Color('Red'), rect1, 3)
    pygame.draw.rect(screen, pygame.Color('Red'), rect2, 3)
    fx_length = str(int(fx_ratio * 100))
    bg_length = str(int(bg_ratio * 100))
    fxl = [int(i) for i in fx_length]
    bgl = [int(j) for j in bg_length]
    if len(fxl) == 3:
        text(str(int(fx_ratio * 100)), font30, pygame.Color("Coral"), sfx_bar.body.right + 58, sfx_bar.rect.y)
    elif len(fxl) == 2:
        text(str(int(fx_ratio * 100)), font30, pygame.Color("Coral"), sfx_bar.body.right + 65, sfx_bar.rect.y)
    elif len(fxl) == 1:
        text(str(int(fx_ratio * 100)), font30, pygame.Color("Coral"), sfx_bar.body.right + 70, sfx_bar.rect.y)

    if len(bgl) == 3:
        text(str(int(bg_ratio * 100)), font30, pygame.Color("Coral"), music_bar.body.right + 58, music_bar.rect.y)
    if len(bgl) == 2:
        text(str(int(bg_ratio * 100)), font30, pygame.Color("Coral"), music_bar.body.right + 65, music_bar.rect.y)
    if len(bgl) == 1:
        text(str(int(bg_ratio * 100)), font30, pygame.Color("Coral"), music_bar.body.right + 70, music_bar.rect.y)
    back_btn.update(screen, mouseClicked)
    if back_btn.action:
        settings = False


# Upgrades screen
def upgrade():
    global updates, spawn_delay, spd_lvl, reload_lvl, delay_lvl, ammo_lvl, upgrade_page, fort_health, fort_max
    bg = pygame.image.load('assets/img/bg.png').convert_alpha()
    screen.blit(bg, (0, 0))

    font = pygame.font.SysFont("Futura", 50)
    font2 = pygame.font.SysFont("Futura", 25)

    coral_clr = pygame.Color("Coral")

    text("UPGRADES", font, coral_clr, 300, 50)
    text(f"Your have: {player.money}", font2, coral_clr, 550, 75)

    back_btn.update(screen, mouseClicked)
    if back_btn.action and mouseClicked == False:
        updates = False

    if upgrade_page == 1:
        text("Cost: 600", font2, coral_clr, 220, 125)
        text("Info: Unlocks Cannon (press c)", font2, coral_clr, 220, 105 + (75 // 2))

        text("Cost: 450", font2, coral_clr, 220, 200)
        text("Info: Gives you 3 rockets (max: 12 rockets)", font2, coral_clr, 220, 180 + (75 // 2))
        text(f"Rockets: {player.rockets}", font2, coral_clr, 220, 200 + (75 // 2))

        text("Cost: 400", font2, coral_clr, 220, 275)
        text("Info: Increases your speed (max level: 4)", font2, coral_clr, 220, 255 + (75 // 2))
        text(f"Level: {spd_lvl}, Your current speed: {player.spd}", font2, coral_clr, 220, 272 + (75 // 2))

        text("Cost: 500", font2, coral_clr, 220, 350)
        text("Info: Gives your more total ammo (max level: 10)", font2, coral_clr, 220, 330 + (75 // 2))
        text(f"Level: {ammo_lvl}, Current Ammo: {player.ammo}", font2, coral_clr, 220, 330 + 17 + (75 // 2))

        text("Cost: 450", font2, coral_clr, 220, 350 + 75)
        text("Info: Reloads faster (max level: 8)", font2, coral_clr, 220, 330 + 75 + (75 // 2))
        text(f"Level: {reload_lvl}, Laser Reload Spd: {player.reload:.3f} secs., Cannon Reload Spd: {player.cannon_reload:.1f} secs.", font2, coral_clr, 220, 330 + 75 + 17 + (75 // 2))

        text("Cost: 1000", font2, coral_clr, 220, 350 + 150)
        text("Info: Increases delay in spawning enemies (max level: 5)", font2, coral_clr, 220, 330 + 150 + (75 // 2))
        text(f"Level: {delay_lvl}, Delay: {spawn_delay:.2f} secs.", font2, coral_clr, 220, 330 + 150 + 17 + (75 // 2))

        cannon_btn.update(screen, mouseClicked)
        rockets_btn.update(screen, mouseClicked)
        ship_spd_btn.update(screen, mouseClicked)
        ammo_btn.update(screen, mouseClicked)
        reload_btn.update(screen, mouseClicked)
        delay_btn.update(screen, mouseClicked)
        page_btn.update(screen, mouseClicked)

        if cannon_btn.action and player.money >= 600 and player.cannon_able == False:
            player.money -= 600
            player.cannon_able = True
            player.cannon_status = "Ready"
        elif rockets_btn.action and player.money >= 900 and player.rockets <= 9:
            player.money -= 450
            player.rockets += 3
        elif ship_spd_btn.action and player.money >= 400 and spd_lvl < 4:
            player.money -= 400
            player.spd += .75
            spd_lvl += 1
        elif ammo_btn.action and player.money >= 500 and ammo_lvl < 10:
            player.max_ammo += 35
            player.money -= 500
            ammo_lvl += 1
        elif reload_btn.action and player.money >= 450 and reload_lvl < 8:
            player.reload -= 0.015
            if (player.type == "heavy-boi"):
                player.cannon_reload -= 0.1
            else:
                player.cannon_reload -= 0.2
            player.money -= 450
            reload_lvl += 1
        elif delay_btn.action and player.money >= 1000 and delay_lvl < 5:
            player.money -= 1000
            spawn_delay += 0.25
            delay_lvl += 1
        elif page_btn.action:
            upgrade_page += 1

        if player.cannon_able:
            cannon_btn.image = pygame.transform.scale(pygame.image.load("assets/img/buttons/maxed_img.png"), (100, 50))
        if player.rockets == 30:
            rockets_btn.image = pygame.transform.scale(pygame.image.load("assets/img/buttons/maxed_img.png"), (100, 50))
        if spd_lvl == 4:
            ship_spd_btn.image = pygame.transform.scale(pygame.image.load("assets/img/buttons/maxed_img.png"), (100, 50))
        if ammo_lvl == 10:
            ammo_btn.image = pygame.transform.scale(pygame.image.load("assets/img/buttons/maxed_img.png"), (100, 50))
        if reload_lvl == 8:
            reload_btn.image = pygame.transform.scale(pygame.image.load("assets/img/buttons/maxed_img.png"), (100, 50))
        if delay_lvl == 5:
            delay_btn.image = pygame.transform.scale(pygame.image.load("assets/img/buttons/maxed_img.png"), (100, 50))

    elif upgrade_page == 2:
        text("Cost: 500", font2, coral_clr, 220, 125)
        text("Info: Repairs the fort", font2, coral_clr, 220, 105 + (75 // 2))
        text(f"Fort Health: {fort_health}", font2, coral_clr, 220, 125 + (75 // 2))

        text(f"Number of lasers: {player.lasers}", font2, coral_clr, 220, 200 + (75 // 2))

        text("Cost: 700", font2, coral_clr, 220, 275)
        text("Info: Increases the max fort health", font2, coral_clr, 220, 255 + (75 // 2))
        text(f"Max fort health: {fort_max}", font2, coral_clr, 220, 255 + 17 + (75 // 2))

        text("Cost: 650", font2, coral_clr, 220, 350)
        text("Info: Increases max player health", font2, coral_clr, 220, 330 + (75 // 2))
        text(f"Max player health: {player.max_health}", font2, coral_clr, 220, 330 + 17 + (75 // 2))

        text("Cost: 700", font2, coral_clr, 220, 350 + 75)
        text("Info: Repairs player's health to full", font2, coral_clr, 220, 330 + 75 + (75 // 2))
        text(f"Player health: {player.health}", font2, coral_clr, 220, 330 + 75 + 17 + (75 // 2))

        if player.lasers == 1:
            text("Cost: 400", font2, coral_clr, 220, 200)
            text("Info: Shoot 2 lasers instead of 1", font2, coral_clr, 220, 180 + (75 // 2))
            double_laser_btn.update(screen, mouseClicked)
            if double_laser_btn.action and player.money >= 400:
                player.money -= 400
                player.lasers = 2
        elif player.lasers == 2:
            text("Cost: 700", font2, coral_clr, 220, 200)
            text("Info: Shoot 3 lasers instead of 2", font2, coral_clr, 220, 180 + (75 // 2))
            triple_laser_btn.update(screen, mouseClicked)
            if triple_laser_btn.action and player.money >= 700:
                player.money -= 700
                player.lasers = 3
        else:
            text("Cost: Maxed out", font2, coral_clr, 220, 200)
            text("Info: You've maxed this out", font2, coral_clr, 220, 180 + (75 // 2))
            triple_laser_btn.image = pygame.transform.scale(pygame.image.load("assets/img/buttons/maxed_img.png"), (100, 50))
            triple_laser_btn.update(screen, mouseClicked)


        repair_btn.update(screen, mouseClicked)
        page_back_btn.update(screen, mouseClicked)
        fort_max_btn.update(screen, mouseClicked)
        ship_max_btn.update(screen, mouseClicked)
        ship_rep_btn.update(screen, mouseClicked)

        if repair_btn.action and player.money >= 500:
            fort_health += 500
            player.money -= 500
        elif fort_max_btn.action and player.money >= 700:
            fort_max += 500
            player.money -= 700
        elif ship_max_btn.action and player.money >= 650:
            player.max_health += 25
            player.money -= 650
        elif ship_rep_btn.action and player.money >= 700:
            player.money -= 700
            player.health = player.max_health
        elif page_back_btn.action:
            upgrade_page -= 1


# To draw background
def background(bg):
    global scroll, scroll_spd
    global upgrade_btn
    global updates
    global settings
    screen.fill((22, 49, 69))
    bgf = bg
    for i in range(2):
        for j in range(2):
            screen.blit(bgf, (i * bgf.get_width() - scroll[0], -j * bgf.get_height() - scroll[1]))
    
    enemy_group.update()
    text(f"FPS: {int(clock.get_fps())}", font30, pygame.Color("Grey"), 710, 75)
    upgrade_btn.update(screen, mouseClicked)
    settings_btn.update(screen, mouseClicked)
    if upgrade_btn.action:
        updates = True
    elif settings_btn.action:
        settings = True


# HUD
def hud():
    font30 = pygame.font.SysFont("Futura", 25)
    coral_clr = pygame.Color("Coral")

    text(f"Rockets: {player.rockets}", font30, coral_clr, 15, 15)
    text(f"Cannon Status: {player.cannon_status}", font30, coral_clr, 115, 15)
    text(f"Ammo: {int(player.ammo)}/{player.max_ammo}", font30, coral_clr, 15, 35)
    text(f"Money: {player.money}", font30, coral_clr, 15, 55)
    text(f"Fort Health: {fort_health}/{fort_max}", font30, coral_clr, 15, 75)
    text(f"Wave: {level}", font30, coral_clr, 15, 95)
    text(f"Score: {score}", font30, coral_clr, 15, 115)
    text(f"High Score: {high_score}", font30, coral_clr, 15, 135)


# Scrolling
def scrollevr():
    global scroll
    global scroll_spd
    scroll[0] += scroll_spd[0]
    scroll[1] += scroll_spd[1]
    if scroll[0] > 800:
        scroll[0] = 800
    elif scroll[0] < 0:
        scroll[0] = 0
    if scroll[1] < -600:
        scroll[1] = -600
    elif scroll[1] > 0:
        scroll[1] = 0


# Sprite groups
laser_group = pygame.sprite.Group()
cannon_group = pygame.sprite.Group()
rocket_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Minimap
minimap = Minimap(10, 465, enemy_group)

particles = Particle_group()

# Sliders
sfx_bar = Slider(250, 200, 300, 25)
music_bar = Slider(250, 300, 300, 25)

lt = pygame.time.get_ticks()

mixer.music.set_volume(0.4)

# Main game loop
while True:
    # Set max fps
    clock.tick(360)

    # Getting Delta time
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    if menu == False:
        if game == 1:
            if updates != True and settings != True:
                # Call background function
                background(bg)

                fx_ratio = (sfx_bar.slider_circle.centerx - sfx_bar.body.x) / sfx_bar.body.width
                bg_ratio = (music_bar.slider_circle.centerx - music_bar.body.x) / music_bar.body.width
                for fx in fx_group:
                    fx.set_volume(fx_ratio)
                mixer.music.set_volume(bg_ratio * 0.4)

                # Update minimap
                minimap.update()

                # Player
                player.draw()
                player.update()

                # Update enemy groups

                # Wave Generator
                if level_difficulty < target_difficulty and level_done == False and wait(lt, spawn_delay):
                    lt = pygame.time.get_ticks()
                    enemy_num = random.randint(1, 5)
                    if enemy_num == 1:
                        enemy = Enemy(random.randint(75, 1525), -750)
                    elif enemy_num == 2:
                        enemy = Enemy(random.randint(75, 1525), -750, "bomber")
                    elif enemy_num == 3 and level >= 10:
                        enemy = Enemy(random.randint(75, 1525), -750, "battleship")
                    elif enemy_num == 4 and level >= 20:
                        enemy = Enemy(random.randint(75, 1525), -750, "heavy-cruiser")
                    elif enemy_num == 5 and level >= 30:
                        enemy = Enemy(random.randint(75, 1525), -750, "mothership")
                    else:
                        enemy_num2 = random.randint(1, 2)
                        if enemy_num2 == 1:
                            enemy = Enemy(random.randint(75, 1525), -750)
                        else:
                            enemy = Enemy(random.randint(75, 1525), -750, "bomber")

                    level_difficulty += enemy.health
                    enemy_group.add(enemy)
                elif level_difficulty >= target_difficulty and len(enemy_group) == 0:
                    level_done = True
                if level_done:
                    enemy_group.empty()
                    target_difficulty += DIFICULTY_ADDER
                    level_difficulty = 0
                    level += 1
                    level_done = False

                # Bullets
                laser_group.update()
                cannon_group.update()
                rocket_group.update()
                particles.update()

                # Display info (HUD)
                hud()

                # For scrolling
                scrollevr()
            elif updates:
                upgrade()
            elif settings:
                options()
            if fort_health > fort_max:
                fort_health = fort_max
            elif fort_health <= 0:
                fort_health = 0
                game = -1
        elif game == -1:
            screen.blit(bg, (0, 0))
            text('GAME OVER', pygame.font.SysFont('Futura', 80), pygame.Color('Coral'), 225, 100)
            if int(score) > int(high_score):
                score = str(score)
                with open("assets/high_score.txt", "w") as f:
                    f.write(str(fer.encrypt(score.encode()).decode()))
            restart_btn.update(screen, mouseClicked)
            quit_btn.update(screen, mouseClicked)
            if restart_btn.action:
                reset = True
            elif quit_btn.action:
                raise SystemExit
            if reset:
                with open("assets/high_score.txt", "r") as file:
                    high_score = file.read()
                    high_score = fer.decrypt(high_score.encode()).decode()
                scroll = [0, 0]
                score = 0
                level_difficulty = 0
                level = 1
                target_difficulty = 100
                run_i = 0
                spawn_delay = 1500
                spd_lvl = 1
                ammo_lvl = 1
                reload_lvl = 1
                delay_lvl = 1
                upgrade_page = 1
                info_page = 1
                enemy_group.empty()
                laser_group.empty()
                cannon_group.empty()
                rocket_group.empty()
                menu = True
                choose_ship = True
    elif menu:
        if info:
            info_screen()
        elif credit:
            credits()
        elif choose_ship:
            choose()
        else:
            main_menu()

    if pygame.mouse.get_pressed()[0] == 1:
        mouseClicked = True
    elif pygame.mouse.get_pressed()[0] == 0:
        mouseClicked = False

    # Detect events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
    # Updates
    pygame.display.update()
