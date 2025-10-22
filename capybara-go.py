import pgzrun
import random
import math
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Capybara Go!"

WORLD_WIDTH = 3200  
camera_x = 0       

GRAVITY = 800
JUMP_STRENGTH = 500
GROUND_Y = 550

game_state = 'menu'
music_on = True

score = 0

start_button = Rect((WIDTH/2 - 100, 200), (200, 50))
sound_button = Rect((WIDTH/2 - 100, 270), (200, 50))
exit_button = Rect((WIDTH/2 - 100, 340), (200, 50))

platforms = [
    Rect((200, 450), (150, 20)),
    Rect((400, 380), (100, 20)),
    Rect((600, 300), (200, 20)),
    Rect((900, 400), (100, 20)),
    Rect((1050, 350), (150, 20)),
    Rect((1300, 450), (200, 20)),
    Rect((1600, 400), (100, 20)),
    Rect((1800, 320), (150, 20)),
    Rect((2050, 250), (100, 20)),
    Rect((2400, 450), (150, 20)), 
    Rect((2600, 350), (100, 20)),
    Rect((2850, 400), (200, 20)),
]


class Character:
    def __init__(self, animations, x, y):
        self.animations = animations
        self.actor = Actor(self.animations['idle'][0], (x, y))
        
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.current_animation = 'idle'
        
        self.actor.x = x 

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            current_anim_list = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(current_anim_list)
            self.actor.image = current_anim_list[self.current_frame]

    def draw(self):
        self.actor.draw()

class Player(Character):
    def __init__(self, x, y):
        player_animations = {
            'idle': ['capy_idle_1', 'capy_idle_2'], 
            'walk_right': ['capy_walk_right_1', 'capy_walk_right_2', 'capy_walk_right_3', 'capy_walk_right_4', 'capy_walk_right_3', 'capy_walk_right_2'],
            'walk_left': ['capy_walk_left_1', 'capy_walk_left_2', 'capy_walk_left_3', 'capy_walk_left_4', 'capy_walk_left_3', 'capy_walk_left_2']
        }
        
        super().__init__(player_animations, x, y)
        self.actor.bottom = y
        self.speed = 200
        self.velocity_y = 0
        self.is_on_ground = True

    def update(self, dt):
        self.velocity_y += GRAVITY * dt
        self.actor.y += self.velocity_y * dt
        
        self.is_on_ground = False

        if self.actor.bottom >= GROUND_Y:
            self.actor.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_on_ground = True

        for platform in platforms:
            if self.actor.colliderect(platform) and self.velocity_y >= 0:
                if self.actor.bottom <= platform.top + (self.velocity_y * dt): 
                    self.actor.bottom = platform.top
                    self.velocity_y = 0
                    self.is_on_ground = True
        
        if (keyboard.up or keyboard.space) and self.is_on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.is_on_ground = False
            if music_on: # <--- CORREÇÃO 1
                try:
                    sounds.jump.play()
                except:
                    pass
        
        is_moving = False
        if keyboard.left:
            self.actor.x -= self.speed * dt
            self.current_animation = 'walk_left'
            is_moving = True
        elif keyboard.right:
            self.actor.x += self.speed * dt
            self.current_animation = 'walk_right'
            is_moving = True
        
        if self.is_on_ground and not is_moving:
            self.current_animation = 'idle'
            
        if self.actor.left < 0: 
            self.actor.left = 0
        if self.actor.right > WORLD_WIDTH: 
            self.actor.right = WORLD_WIDTH
            
        self.update_animation(dt)

class Enemy(Character):
    def __init__(self, x, y, patrol_range=100): 
        enemy_animations = {
            'idle': ['mrbones_idle_1', 'mrbones_idle_2'],
            'walk_right': ['mrbones_walk_right_1', 'mrbones_walk_right_2', 'mrbones_walk_right_3', 'mrbones_walk_right_4', 'mrbones_walk_right_3', 'mrbones_walk_right_2'],
            'walk_left': ['mrbones_walk_left_1', 'mrbones_walk_left_2', 'mrbones_walk_left_3', 'mrbones_walk_left_4', 'mrbones_walk_left_3', 'mrbones_walk_left_2']
        }
        
        super().__init__(enemy_animations, x, y)
        self.actor.bottom = y
        self.speed = 100
        self.direction = 1
        self.current_animation = 'walk_right'
        self.velocity_y = 0
        self.is_on_ground = True
        
        self.patrol_min_x = x - patrol_range
        self.patrol_max_x = x + patrol_range

    def update(self, dt):
        self.velocity_y += GRAVITY * dt
        self.actor.y += self.velocity_y * dt
        
        self.is_on_ground = False
        
        if self.actor.bottom >= GROUND_Y:
            self.actor.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_on_ground = True
            
        for platform in platforms:
            if self.actor.colliderect(platform) and self.velocity_y >= 0:
                if self.actor.bottom <= platform.top + (self.velocity_y * dt):
                    self.actor.bottom = platform.top
                    self.velocity_y = 0
                    self.is_on_ground = True
            
        if self.is_on_ground:
            self.actor.x += self.speed * dt * self.direction
            
            if self.actor.right > min(self.patrol_max_x, WORLD_WIDTH):
                self.actor.right = min(self.patrol_max_x, WORLD_WIDTH)
                self.direction = -1
                self.current_animation = 'walk_left'
            elif self.actor.left < max(self.patrol_min_x, 0):
                self.actor.left = max(self.patrol_min_x, 0)
                self.direction = 1
                self.current_animation = 'walk_right'
        
        self.update_animation(dt)

player = Player(WIDTH/2, GROUND_Y)

mrbones = []
mrbones.append(Enemy(500, GROUND_Y, patrol_range=300))
mrbones.append(Enemy(1000, GROUND_Y, patrol_range=250))
mrbones.append(Enemy(1400, 450)) 
mrbones.append(Enemy(1900, 320))

stars = []

for _ in range(5):
    star_x = random.randint(50, WORLD_WIDTH - 50)
    stars.append(Actor('star', (star_x, GROUND_Y - 30)))

for p in platforms:
    star_x = p.centerx
    star_y = p.top - 30
    stars.append(Actor('star', (star_x, star_y)))


def draw():
    global score, camera_x
    screen.clear()
    
    if game_state == 'menu':
        screen.fill('darkblue')
        screen.draw.text('Capybara Go!', center=(WIDTH/2, 100), fontsize=60)
        screen.draw.filled_rect(start_button, 'green')
        screen.draw.text('Comecar o Jogo', center=start_button.center, fontsize=30)
        screen.draw.filled_rect(sound_button, 'orange')
        sound_text = 'Musica e Sons Ligados' if music_on else 'Musica e Sons Desligados' 
        screen.draw.text(sound_text, center=sound_button.center, fontsize=25)
        screen.draw.filled_rect(exit_button, 'red')
        screen.draw.text('Sair', center=exit_button.center, fontsize=30)
    
    elif game_state == 'playing':
        screen.fill('darkgreen')
        
        screen.draw.filled_rect(Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y), 'brown')
        
        for p in platforms:
            screen_rect = Rect((p.x - camera_x, p.y), (p.width, p.height))
            screen.draw.filled_rect(screen_rect, 'saddlebrown')

        player_world_x = player.actor.x
        enemies_world_x = [e.actor.x for e in mrbones]
        stars_world_x = [s.x for s in stars]

        player.actor.x = player_world_x - camera_x
        for i, e in enumerate(mrbones):
            e.actor.x = enemies_world_x[i] - camera_x
        for i, s in enumerate(stars):
            s.x = stars_world_x[i] - camera_x
            
        for star in stars:
            star.draw()
            
        player.draw()
        for enemy in mrbones:  
            enemy.draw()

        player.actor.x = player_world_x
        for i, e in enumerate(mrbones):
            e.actor.x = enemies_world_x[i]
        for i, s in enumerate(stars):
            s.x = stars_world_x[i]
            
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="yellow")

    elif game_state == 'win':
        screen.fill('blue')
        screen.draw.text('VOCE VENCEU!', center=(WIDTH/2, HEIGHT/2 - 40), fontsize=80)
        screen.draw.text(f'Score Final: {score}', center=(WIDTH/2, HEIGHT/2 + 40), fontsize=60)

    elif game_state == 'game_over':
        screen.fill('black')
        screen.draw.text('FIM DE JOGO', center=(WIDTH/2, HEIGHT/2 - 40), fontsize=80)
        screen.draw.text('Mr. Bones te pegou!', center=(WIDTH/2, HEIGHT/2 + 40), fontsize=50)

def update(dt):
    global game_state, score, music_on, camera_x
    
    if music_on and not music.is_playing('background.mp3'):
        music.play('background.mp3')
    elif not music_on:
        music.stop()

    if game_state == 'playing':

        player.update(dt)
        for enemy in mrbones:
            enemy.update(dt)

        target_camera_x = player.actor.x - WIDTH / 2
        
        camera_x = max(0, min(target_camera_x, WORLD_WIDTH - WIDTH))

        collected_stars = []
        for star in stars:
            if player.actor.colliderect(star):
                collected_stars.append(star)
                score += 10 
                if music_on: # <--- CORREÇÃO 2
                    try:
                        sounds.collect.play() 
                    except:
                        print("Arquivo de som 'collect' não encontrado")
        
        for star in collected_stars:
            stars.remove(star)
            
        if not stars:
            game_state = 'win'
            music.stop()
            if music_on:
                try:
                    sounds.win.play()
                except:
                    print("Arquivo de som 'win' não encontrado na pasta /sounds/")
            music_on = False 

        for enemy in mrbones:
            if player.actor.colliderect(enemy.actor):
                print("Crash! Mr. Bones te capturou!")
                music.stop()
                if music_on:
                    try:
                        sounds.game_over.play() 
                    except:
                        print("Arquivo de som 'game_over' não encontrado na pasta /sounds/")
                game_state = 'game_over'
                music_on = False
                break

def on_mouse_down(pos):
    global game_state, music_on
    
    if game_state == 'menu':
        if start_button.collidepoint(pos):
            game_state = 'playing' 
        elif sound_button.collidepoint(pos):
            music_on = not music_on
        elif exit_button.collidepoint(pos):
            quit()

    if game_state == 'game_over' or game_state == 'win':
        quit()

try: 
    music.set_volume(0.3)
except:
    print("Arquivo de música 'background.mp3' não encontrado na pasta /music/")

pgzrun.go()