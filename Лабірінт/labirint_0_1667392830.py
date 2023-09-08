from pygame import *



#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.coins = None
        self.collected_coins = 0
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self): 
        # Спершу рух по горизонталі
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
            # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # йдемо вниз
            for p in platforms_touched:
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 25, 25, 15)
        bullets.add(bullet)
    def fire2(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 25, 25, -15)
        bullets.add(bullet)    


#клас спрайту-ворога
class Enemy_h(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 =x1
        self.x2 =x2
        

   #рух ворога
    def update(self):
        if self.rect.x <= self.x1: 
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 =y1
        self.y2 =y2
        

   #рух ворога
    def update(self):
        if self.rect.y <= self.y1: #w1.wall_x + w1.wall_width
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

# клас спрайту-кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #рух ворога
    def update(self):
        self.rect.x += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x > win_width+10:
            self.kill()


font.init()
font1 = font.SysFont('Shtift.ttf', 25)
font2 = font.SysFont('Shrift_play.ttf', 40)
font3 = font.SysFont('Shrift_play.ttf', 25)



class Coin(GameSprite):
    def __init__(self, spr_image, spr_x, spr_y, spr_size_x, spr_size_y):
        GameSprite.__init__(self, spr_image, spr_x, spr_y, spr_size_x, spr_size_y)      
    


#Створюємо віконце
win_width = 700
win_height = 650
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load("forest.jpg"), (win_width, win_height)) # задаємо колір відповідно до колірної схеми RGB
icon = image.load('icons.png')
display.set_icon(icon)

A = image.load('A.png')
D = image.load('D.png')

#Створюємо групу для стін 
barriers = sprite.Group()

bullets = sprite.Group()

monsters = sprite.Group()

coins = sprite.Group()

keys = sprite.Group()


A = GameSprite('A.png',130, 605, 60, 40)
D = GameSprite('D.png',340, 605, 60, 40)
arrows = GameSprite('arrows.png',570, 560, 100, 80)

keys.add(A)
keys.add(D)
keys.add(arrows)


heartse = GameSprite('heart.png', 10, 600, 70, 50) 
coine = GameSprite('coin.png', 0, 520, 90, 60)

coin1 = Coin('coin.png', 10, 265, 60, 40)
coin2 = Coin('coin.png', 450, 30, 60, 40)
coin3 = Coin('coin.png', 80, 300, 60, 40)
coin4 = Coin('coin.png', 600, 317, 60, 40)
coin5 = Coin('coin.png', 385, 30, 60, 40)


coins.add(coin1)
coins.add(coin2)
coins.add(coin3)
coins.add(coin4)
coins.add(coin5)





#Створюємо стіни картинки
w1 = GameSprite('platform.png',0, 90, 10, 400 )
w2 = GameSprite('platform.png', 0, 490, 700, 10)
w3 = GameSprite('platform.png',690, 0, 10, 500)
w4 = GameSprite('platform.png',0, 0, 700, 10 )
w5 = GameSprite('platform.png',150, 80, 450, 10 )
w6 = GameSprite('platform.png',450, -210, 10, 300)
w7 = GameSprite('platform.png',80, -200, 10, 300)
w8 = GameSprite('platform.png',-5, 250, 80, 10)
w9 = GameSprite('platform.png',80,170, 525, 10)
w10 = GameSprite('platform.png',70,250, 10, 160)
w11 = GameSprite('platform.png',80,350, 70, 10)
w12 = GameSprite('platform.png',145,170, 10, 190)
w13 = GameSprite('platform.png',220,250, 500, 10)
w14 = GameSprite('platform.png',550,400, 500, 10)
w15 = GameSprite('platform.png',220,250, 10, 110)
w16 = GameSprite('platform.png',290,250, 10, 160)
w17 = GameSprite('platform.png',375,330, 10, 170)
w18 = GameSprite('platform.png',550,250, 10, 50)
w19 = GameSprite('platform.png',550,360, 10, 50)
w20 = GameSprite('platform.png',455,250, 10, 160)
w21 = GameSprite('platform.png',180,435, 10, 60)
w22 = GameSprite('fone.png',0,500, 800, 500)
w23 = GameSprite('platform.png',550,400, 10, 90)


#додаємо стіни до групи
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)
barriers.add(w12)
barriers.add(w13)
barriers.add(w14)
barriers.add(w15)
barriers.add(w16)
barriers.add(w17)
barriers.add(w18)
barriers.add(w19)
barriers.add(w20)
barriers.add(w21)
barriers.add(w22)
barriers.add(w23)

#створюємо спрайти
packman = Player('hero.png', 5, win_height - 620, 60, 60, 0, 0)
final_sprite = GameSprite('pokemon.png', win_width - 85, win_height - 240, 80, 80)

monster = Enemy_v('monster.png', win_width - 470, 370, 60, 60,5, 250,450)
monster2 = Enemy_h('monster2.png', win_width - 120, 280, 100, 100,5, 470, win_width-85)
monster3 = Enemy_v('monster3.png', win_width - 610, 100, 60, 60, 3, 0, 100)
monster4 = Enemy_v('monster4.png', win_width - 90, 100, 80, 80, 6, 0, 150)
monster5 = Enemy_v('monster5.png', win_width - 625, 370, 80, 80, 6, 360, 420)

monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

#змінна, що відповідає за те, як закінчилася гра
finish = False
#ігровий цикл
run = True



mixer.init()
mixer.music.load('back.mp3')
mixer.music.set_volume(0.08)
mixer.music.play(loops=-1)

bullet = mixer.Sound('bullet.ogg')
bullet.set_volume(0.2)
losers = mixer.Sound('failed.ogg')
winer = mixer.Sound('win.ogg')
coinse = mixer.Sound('money.ogg')
coinse.set_volume(1.0)



coins_amount_1 = 0
hearts = 3

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP :
                packman.y_speed = -5
            elif e.key == K_DOWN :
                packman.y_speed = 5
            elif e.key == K_d:
                packman.fire() 
                bullet.play()   
            elif e.key == K_a:
                packman.fire2() 
                bullet.play()       
 
        elif e.type == KEYUP:
            if e.key == K_LEFT :
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if not finish:
        window.blit(back, (0, 0))
        #малюємо об'єкти
        barriers.draw(window)
        monsters.update()
        monsters.draw(window)
        packman.reset()
        coins.draw(window)
        final_sprite.reset()
        heartse.reset()
        coine.reset()
        keys.draw(window)
        
        
        #включаємо рух
        packman.update()
        bullets.update()

        bullets.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(bullets, barriers, True, False)

        if coins_amount_1 >= 5:
            barriers.remove(w23)
    

        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(packman, monsters, False):
            hearts -= 1
            packman = Player('hero.png', 5, win_height - 620, 60, 60, 0, 0)

            if coins_amount_1 == 1:
                coins_amount_1 -=1
                coin1 = Coin('coin.png', 10, 265, 60, 40)
                coin2 = Coin('coin.png', 450, 30, 60, 40)
                coin3 = Coin('coin.png', 80, 300, 60, 40)
                coin4 = Coin('coin.png', 600, 317, 60, 40)
                coin5 = Coin('coin.png', 385, 30, 60, 40)

                coins.add(coin1)
                coins.add(coin2)
                coins.add(coin3)
                coins.add(coin4)
                coins.add(coin5)

            if coins_amount_1 == 2:
                coins_amount_1 -=2
                coin1 = Coin('coin.png', 10, 265, 60, 40)
                coin2 = Coin('coin.png', 450, 30, 60, 40)
                coin3 = Coin('coin.png', 80, 300, 60, 40)
                coin4 = Coin('coin.png', 600, 317, 60, 40)
                coin5 = Coin('coin.png', 385, 30, 60, 40)

                coins.add(coin1)
                coins.add(coin2)
                coins.add(coin3)
                coins.add(coin4)
                coins.add(coin5)

            if coins_amount_1 == 3:
                coins_amount_1 -=3
                coin1 = Coin('coin.png', 10, 265, 60, 40)
                coin2 = Coin('coin.png', 450, 30, 60, 40)
                coin3 = Coin('coin.png', 80, 300, 60, 40)
                coin4 = Coin('coin.png', 600, 317, 60, 40)
                coin5 = Coin('coin.png', 385, 30, 60, 40)

                coins.add(coin1)
                coins.add(coin2)
                coins.add(coin3)
                coins.add(coin4)
                coins.add(coin5)    

            if coins_amount_1 == 4:
                coins_amount_1 -=4
                coin1 = Coin('coin.png', 10, 265, 60, 40)
                coin2 = Coin('coin.png', 450, 30, 60, 40)
                coin3 = Coin('coin.png', 80, 300, 60, 40)
                coin4 = Coin('coin.png', 600, 317, 60, 40)
                coin5 = Coin('coin.png', 385, 30, 60, 40)

                coins.add(coin1)
                coins.add(coin2)
                coins.add(coin3)
                coins.add(coin4)
                coins.add(coin5)

              

        if hearts == 0:
            finish = True
            img = image.load('loser.png')
            window.blit(transform.scale(img, (win_width - 150, win_height - 150)), (100, 0))
            losers.play()
            mixer.music.pause()
            

        if sprite.spritecollide(packman, coins, True):
            coins_amount_1 += 1
            coinse.play()
        
        coin_text = font1.render(f' {coins_amount_1}/5', True, (0,0, 0))
        window.blit(coin_text, (50, 560))  
        

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('win.jpg')
            window.blit(transform.scale(img, (win_width - 150 , win_height - 150)), (100, 0))
            winer.play()
            mixer.music.pause()
            display.update()

        setting_text = font1.render(f' - стріляти вліво                 - стріляти вправо',False,(255,255,255))   
        window.blit(setting_text, (200, 620)) 

        hp_text = font1.render(f"x {hearts}", True, (0, 0, 0))
        window.blit(hp_text, (55, 630))

        
        task_text = font2.render(f'Задача:',True,(0,0,0))
        window.blit(task_text,(280,500))

        task2_text = font3.render(f'Зібрати всі монете, після чого буде відкрита стіна',True,(0,0,0))
        window.blit(task2_text,(120,540))

        task3_text = font3.render(f'ОСТЕРІГАЙСЯ ВОРОГІВ!',True,(0,0,0))
        window.blit(task3_text,(230,575))
        #цикл спрацьовує кожну 0.05 секунд
        time.delay(20)
        display.update()


