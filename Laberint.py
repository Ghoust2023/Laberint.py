from pygame import *

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self,player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        if self.rect.x <= win_width - 73 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = p.rect.left
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = p.rect.right  
        if self.rect.y <= win_heigth - 83 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = p.rect.bottom
        
    def fire(self):
        bullet = Bullet('molnia.png', self.rect.centerx, self.rect.top, 30, 35, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = 'лево'
    
    def update(self):
        if self.rect.x <= 687:
            self.side = "право"
        if self.rect.x >= win_width-80:
            self.side = 'лево'
        if self.side == 'лево':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_2(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = 'лево'
    
    def update(self):
        if self.rect.x <= 605:
            self.side = "право"
        if self.rect.x >= win_width-80:
            self.side = 'лево'
        if self.side == 'лево':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

win_width = 1000
win_heigth = 700
window = display.set_mode((win_width, win_heigth))
display.set_caption('PACMAN')
back = (250, 50, 50)

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

w1 = GameSprite('platform1.png',116, 180, 300, 50)
w2 = GameSprite('platform2.png',370, 100, 50, 400)
w3 = GameSprite('platform2.png',560, 370, 50, 335)
w4 = GameSprite('platform2.png',180, 370, 50, 335)
w5 = GameSprite('platform2.png',370, 605, 50, 100)
w6 = GameSprite('platform2.png',637, 0, 50, 255)

barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)

packman = Player('Phone.png',5, win_heigth - 90, 60, 80, 0, 0)
monster = Enemy('cyborg.png', win_width - 100, 180, 80, 80, 5)
monster2 = Enemy_2('cyborg.png', win_width - 100, 420, 80, 80, 5)
final_sprite = GameSprite('pac-1.png', win_width - 100, win_heigth - 100, 80, 80)

monsters.add(monster)
monsters.add(monster2)

finish = True

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -7
            elif e.key == K_RIGHT:
                packman.x_speed = 7
            elif e.key == K_UP:
                packman.y_speed = -7
            elif e.key == K_DOWN:
                packman.y_speed = 7
            elif e.key == K_SPACE:
                packman.fire()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    if finish:
        window.fill(back)
        final_sprite.reset()
        packman.reset()
        packman.update()
        bullets.update()
        bullets.draw(window)
        barriers.draw(window)

        sprite.groupcollide(bullets, barriers, True, False)

        if not(sprite.groupcollide(monsters, bullets, True, True)):
            monsters.draw(window)
            monsters.update()

        if sprite.spritecollide(packman, monsters, True):
            finish = False
            img = image.load('game-over_1.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_heigth)), (0, 0))
        
        if sprite.collide_rect(packman, final_sprite):
            finish = False
            img = image.load('you_win.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_heigth)), (0, 0))

    time.delay(30)
    display.update()