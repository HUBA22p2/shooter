from pygame import*
from random import randint
import time as t
init()
# розміри вікна
W = 500
H = 700

window = display.set_mode((W, H))
display.set_caption("shooter")# надання назви вікна
display.set_icon(image.load("rocket.png"))# завантаження об'єкта
# піднесення об'єкта під розміри вікна
back = transform.scale(image.load('galaxy.jpg'), (W, H))
# clock = time.Clock()
# змінні для підрахунку пропущених, вбитих, життя
lost = 0
killed = 0
score = 0
life = 5

"""         ЗВУКИ       """
mixer.init()
mixer.music.load('space.ogg')# фонова музика
mixer.music.set_volume(0.3)# гучність музики
fire = mixer.Sound('fire.ogg')# звук для пострілу
mixer.music.play()# запуск фонової музики

"""         ШРИФТИ       """
font.init()
font1 = font.SysFont('Arial', 30, bold=True)
font2 = font.SysFont('Arial', 60, bold=True)

""""        КЛАСИ       """
class GameSprite(sprite.Sprite):# основний клас 
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()# відмалювання картинки
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):# клас для гравця
    def update(self):# метод управління гравця  
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - 80)
            lost += 1

class Asteroid(Enemy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - 80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# створення об'єктів            
player = Player("rocket.png",W/2,H-100,80, 100, 6)
# створення групи спрайтів
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):# створюємо ворогів і додаємо в групу
    monster = Enemy('ufo.png', randint(0, W-80), randint(-50, 0), 80, 50, randint(1, 3))
    monsters.add(monster)

for i in range(1):
    asteroid = Asteroid('asteroid.png', randint(0, W-80), randint(-50, 0), 80, 50, randint(1, 3))
    asteroids.add(asteroid)

game = True
finish = False
num_fire = 0
rel_time = False
color_life = (0, 255, 0)
while game:# ігровий цикл
    time.delay(10)# затримка
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 15 and rel_time is False:
                    num_fire += 1
                    player.fire()
                    fire.play()
                if num_fire > 15 and rel_time is False:
                    rel_time = True
                    last_time = t.time()


                
    if not finish:
        window.blit(back, (0, 0))# малювання фону
        player.reset()# малювання гравця
        player.update()# рух гравця

        monsters.draw(window)# малювання монстрів
        monsters.update()

        asteroids.draw(window)# малювання астероїдів
        asteroids.update()    

        bullets.draw(window)
        bullets.update()

        if rel_time:
            new_time = t.time()
            if new_time - last_time < 1:
                reload_txt = font1.render('Перезарядка...', True, (255, 0, 0))
                window.blit(reload_txt, (W/2-100, H-100))
            else:
                rel_time = False
                num_fire = 0


        lost_txt = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))# текст пропущено
        window.blit(lost_txt, (10, 10))# виводить текст
        killed_txt = font1.render('Збито: ' + str(killed), 1, (255, 255, 255))
        window.blit(killed_txt, (10, 45))
        life_txt = font2.render(str(life), 1, color_life)
        window.blit(life_txt, (450, 5))

        if life == 2:
            color_life = (212, 174, 38)
        if life == 1:
            color_life = (255, 0, 0)

        if sprite.spritecollide(player, monsters, True):
            life -= 1
            monster = Enemy('ufo.png', randint(0, W-80), -50, 80, 50, randint(1, 3))
            monsters.add(monster)

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for col in collides:
            killed += 1
            monster = Enemy('ufo.png', randint(0, W-80), -50, 80, 50, randint(1, 3))
            monsters.add(monster)
            
        if killed >= 100:
            finish = True
            win = font2.render('Ти виграв!!!', True, (0, 255, 0))
            window.blit(win, (W/2-180, H/2-50))
        if life <= 0:
            finish = True
            lose = font2.render('Ти програв!!!', True, (255, 0, 0))
            window.blit(lose, (W/2-180, H/2-50))
        if lost >= 10:
            finish = True
            lose = font2.render('Ти програв!!!', True, (255, 0, 0))
            window.blit(lose, (W/2-180, H/2-50))

        if sprite.spritecollide(player, asteroids, True):
            life -= 5
            asteroid = Asteroid("asteroid.png", randint(0, W - 80), randint(-50, 0), 80, 50, randint(1, 3))
            asteroids.add(asteroid)

    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_r]:
            life = 5
            killed = 0
            lost = 0
            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for i in range(5):
                monster = Enemy('ufo.png', randint(0, W-80), -50, 80, 50, randint(1, 3))
                monsters.add(monster)
            finish = False




    display.update()# оновлення екрану










