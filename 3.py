from pygame import *
from random import randint

# підвантажуємо окремо функції для роботи зі шрифтом
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

# фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# нам потрбні такі картинки:
img_back = "galaxy.jpg"  # фон гри
img_bullet = "bullet.png"  # куля
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # ворог
score = 0  # збито кораблів
goal = 10  # стільки кораблів потрбіно збити для перемоги
lost = 0  # пропущено кораблів
max_lost = 3  # програли, якщо пропустили стільки
life = 3

# батьківський клас для інших спрайтів
class GameSprite(sprite.Sprite):
   # конструктор класу
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       # виклкикаємо конструктор класу (Sprite):
       sprite.Sprite.__init__(self)

       # кожен спрайт має зберігати властивість image
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed

       # кожен спрайт повинен зберігати властивість rect - прямокутник, який він вписаний
       self.rect = self.image.get_rect()

       self.rect.x = player_x
       self.rect.y = player_y

   # метод, що відмальовує героя на екрані
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


# клас головного героя
class Player(GameSprite):
   # метод для керування спрайтами стрілками клавіатури
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed

   # метод "постріл" (використвою місце гравця, щоб ствоорити там кулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

# клас спрайту-ворога
class Enemy(GameSprite):
   # рух ворога
   def update(self):
       self.rect.y += self.speed
       global lost
       # зникає якщо дійде до краю екрану
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1


# клас спрайту-кулі
class Bullet(GameSprite):
   # рух ворога
   def update(self):
       self.rect.y += self.speed
       # зникає якщо дійде до краю екрану
       if self.rect.y < 0:
           self.kill()


# створюємо ігрове вікно
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
# створюємо групи спрайтів
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
bullets = sprite.Group()
# змінна "гра закінчилася": як тільки там True, в основному циклі перестають працювати спрайти
finish = False
# основний цикл гри:
run = True  # рапор скидається кнопкою закриття вікна
while run:
   # подія натискання на кнопку Закрити
   for e in event.get():
       if e.type == QUIT:
           run = False
       # подія натискання на пробіл - спрайт стріляє
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
   # сама гра: дії спрайтів, перевірка правил гри, перемальовка
   if not finish:
       # оновлюємо фон
       window.blit(background, (0, 0))

       # виробляємо рухи спрайтів
       ship.update()
       monsters.update()
       bullets.update()

       # оновлюємо їх у новому місці при кожній ітерації циклу
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       # перевірка зіткнення кулі та монстрів (і монстр, і куля при дотику зникають)
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           # цей цикл повториться стільки разів, скільки монстрів підбито
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)

       # можливий програш: пропустили забагато або герой зіткнувся з ворогом
       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
           finish = True  # програли, ставимо тло і більше не керуємо спрайтами.
           window.blit(lose, (200, 200))

       # перевірка виграшу: скільки очок набрали?
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))

       # пишемо текст на екрані
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))

       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))

       display.update()
   # бонус: автоматичний перезапуск гри
   else:
       finish = False
       score = 0
       lost = 0
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()

       time.delay(3000)
       for i in range(1, 6):
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)

   time.delay(50)

