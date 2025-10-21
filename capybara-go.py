import pgzrun
import random
import math
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Capybara Go!"

GRAVITY = 800
JUMP_STRENGTH = 450
GROUND_Y = 550

game_state = 'menu'
music_on = True

score = 0

start_button = Rect((WIDTH/2 - 100, 200), (200, 50))
sound_button = Rect((WIDTH/2 - 100, 270), (200, 50))
exit_button = Rect((WIDTH/2 - 100, 340), (200, 50))


class Character:
    def __init__(self, animations, x, y):
        self.animations = animations
        self.actor = Actor(self.animations['idle'][0], (x, y))
        
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.current_animation = 'idle'

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
            'walk_right': ['capy_walk_right_1', 'capy_walk_right_2', 'capy_walk_right_3', 'capy_walk_right_4'],
            'walk_left': ['capy_walk_left_1', 'capy_walk_left_2', 'capy_walk_left_3', 'capy_walk_left_4']
        }
        
        super().__init__(player_animations, x, y)
        self.actor.bottom = y
        self.speed = 200
        self.velocity_y = 0
        self.is_on_ground = True

    def update(self, dt):
        self.velocity_y += GRAVITY * dt
        self.actor.y += self.velocity_y * dt

        if self.actor.bottom >= GROUND_Y:
            self.actor.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_on_ground = True
        
        if (keyboard.up or keyboard.space) and self.is_on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.is_on_ground = False
            sounds.jump.play()
        
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
            
        if self.actor.left < 0: self.actor.left = 0
        if self.actor.right > WIDTH: self.actor.right = WIDTH
            
        self.update_animation(dt)

class Enemy(Character):
    def __init__(self, x, y):
        enemy_animations = {
            'idle': ['mrbones_idle_1', 'mrbones_idle_2'],
            'walk_right': ['mrbones_walk_right_1', 'mrbones_walk_right_2', 'mrbones_walk_right_3', 'mrbones_walk_right_4'],
            'walk_left': ['mrbones_walk_left_1', 'mrbones_walk_left_2', 'mrbones_walk_left_3', 'mrbones_walk_left_4']
        }
        
        super().__init__(enemy_animations, x, y)
        self.actor.bottom = y
        self.speed = 100
        self.direction = 1
        self.current_animation = 'walk_right'
        self.velocity_y = 0
        self.is_on_ground = True

    def update(self, dt):
        self.velocity_y += GRAVITY * dt
        self.actor.y += self.velocity_y * dt
        
        if self.actor.bottom >= GROUND_Y:
            self.actor.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_on_ground = True
            
        if self.is_on_ground:
            self.actor.x += self.speed * dt * self.direction
            
            if self.actor.right > WIDTH:
                self.actor.right = WIDTH
                self.direction = -1
                self.current_animation = 'walk_left'
            elif self.actor.left < 0:
                self.actor.left = 0
                self.direction = 1
                self.current_animation = 'walk_right'
        
        self.update_animation(dt)
mrbones = []

player = Player(WIDTH/2, GROUND_Y)
for _ in range(3): 
    mrbones.append(Enemy(random.randint(0, WIDTH), GROUND_Y))

stars = []
for _ in range(10):
    star_x = random.randint(50, WIDTH - 50)
    star_y = random.randint(100, GROUND_Y - 50)
    stars.append(Actor('star', (star_x, star_y)))


def draw():
    global score
    screen.clear()
    
    if game_state == 'menu':
        screen.fill('darkblue')
        screen.draw.text('Capybara Go!', center=(WIDTH/2, 100), fontsize=60)
        screen.draw.filled_rect(start_button, 'green')
        screen.draw.text('Começar o Jogo', center=start_button.center, fontsize=30)
        screen.draw.filled_rect(sound_button, 'orange')
        sound_text = 'Música e Sons Ligados' if music_on else 'Música e Sons Desligados' 
        screen.draw.text(sound_text, center=sound_button.center, fontsize=25)
        screen.draw.filled_rect(exit_button, 'red')
        screen.draw.text('Sair', center=exit_button.center, fontsize=30)
    
    elif game_state == 'playing':
        screen.fill('darkgreen')
        screen.draw.filled_rect(Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y), 'brown')
        for star in stars:
            star.draw()
            
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="yellow")
        
        player.draw()
        for mrbones in mrbones:  
            mrbones.draw()

    elif game_state == 'win':
        screen.fill('blue')
        screen.draw.text('VOCÊ VENCEU!', center=(WIDTH/2, HEIGHT/2 - 40), fontsize=80)
        screen.draw.text(f'Score Final: {score}', center=(WIDTH/2, HEIGHT/2 + 40), fontsize=60)

    elif game_state == 'game_over':
        screen.fill('black')
        screen.draw.text('FIM DE JOGO', center=(WIDTH/2, HEIGHT/2), fontsize=80)

def update(dt):
    global game_state, score, music_on 
    
    if music_on and not music.is_playing():
        music.play('background.mp3')
    elif not music_on:
        music.stop()

    if game_state == 'playing':
        player.update(dt) 
        for mrbones in mrbones:
            mrbones.update(dt)

        collected_stars = []
        for star in stars:
            if player.actor.colliderect(star):
                collected_stars.append(star)
                score += 10 
                try:
                    sounds.collect.play() 
                except:
                    print("Arquivo de som 'collect' não encontrado")
        
        for star in collected_stars:
            stars.remove(star)
            
        if not stars:
            game_state = 'win'

        for'mrbones in'mrboness:
            if player.actor.colliderect'mrbones.actor):
                print("Crash! Mr. Bones te capturou!")
                if music_on:
                    try:
                        sounds.dano.play()
                    except:
                        print("Arquivo de som 'dano' não encontrado")
                game_state = 'game_over'

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
    music.play('background.mp3') 
    music.set_volume(0.3)
except:
    print("Arquivo de música 'background.mp3' não encontrado na pasta /music/")

pgzrun.go()