import pgzrun
import random
import math
from pygame import Rect

# --- 1. Constantes e Configuração da Tela ---
WIDTH = 800
HEIGHT = 600
TITLE = "Capybara Go!"

GRAVITY = 800
JUMP_STRENGTH = 450
GROUND_Y = 550

# --- 2. Variáveis Globais de Estado ---
game_state = 'menu'
music_on = True
# --- AQUI ESTÁ A MUDANÇA (Score) ---
score = 0

# --- 3. Definição dos Botões (Rects) ---
start_button = Rect((WIDTH/2 - 100, 200), (200, 50))
sound_button = Rect((WIDTH/2 - 100, 270), (200, 50))
exit_button = Rect((WIDTH/2 - 100, 340), (200, 50))

# --- 4. Definição das Classes ---

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
        # Use os nomes das imagens da sua capivara
        player_animations = {
            'idle': ['capy_idle_1', 'capy_idle_2'], 
            'walk_right': ['capy_walk_right_1', 'capy_walk_right_2', 'capy_walk_right_3'],
            'walk_left': ['capy_walk_left_1', 'capy_walk_left_2', 'capy_walk_left_3']
        }
        
        super().__init__(player_animations, x, y)
        self.actor.bottom = y
        self.speed = 200
        self.velocity_y = 0
        self.is_on_ground = True

    def update(self, dt):
        # 1. Aplica gravidade
        self.velocity_y += GRAVITY * dt
        # 2. Atualiza a posição Y
        self.actor.y += self.velocity_y * dt
        
        # 3. Checagem de Chão
        if self.actor.bottom >= GROUND_Y:
            self.actor.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_on_ground = True
        
        # 4. Lógica do Pulo
        if (keyboard.up or keyboard.space) and self.is_on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.is_on_ground = False
            # Opcional: sounds.jump.play()
        
        # Lógica de movimento (esquerda/direita)
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

# --- AQUI ESTÁ A MUDANÇA (Classe Enemy renomeada) ---
class MrBones(Character):
    def __init__(self, x, y):
        # Use os nomes das imagens do seu esqueleto
        enemy_animations = {
            'idle': ['skeleton_idle_1'],
            'walk_right': ['skeleton_walk_right_1', 'skeleton_walk_right_2'],
            'walk_left': ['skeleton_walk_left_1', 'skeleton_walk_left_2']
        }
        
        super().__init__(enemy_animations, x, y)
        self.actor.bottom = y
        self.speed = 100
        self.direction = 1
        self.current_animation = 'walk_right'
        self.velocity_y = 0
        self.is_on_ground = True

    def update(self, dt):
        # Gravidade para o Mr. Bones
        self.velocity_y += GRAVITY * dt
        self.actor.y += self.velocity_y * dt
        
        if self.actor.bottom >= GROUND_Y:
            self.actor.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_on_ground = True
            
        # Lógica de patrulha (só se move se estiver no chão)
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

# --- 5. Criação dos Objetos (Instâncias) ---

player = Player(WIDTH/2, GROUND_Y)

# --- AQUI ESTÁ A MUDANÇA (Inimigos agora são skeletons) ---
skeletons = []
for _ in range(3): 
    skeletons.append(MrBones(random.randint(0, WIDTH), GROUND_Y))

# --- AQUI ESTÁ A MUDANÇA (Criação das Estrelas) ---
stars = []
for _ in range(10): # Cria 10 estrelas
    # Garante que as estrelas não apareçam no chão ou muito alto
    star_x = random.randint(50, WIDTH - 50)
    star_y = random.randint(100, GROUND_Y - 50)
    stars.append(Actor('star', (star_x, star_y))) # 'star.png' deve estar em /images/

# --- 6. Funções Principais do Pygame Zero ---

def draw():
    global score # Pega a variável global
    screen.clear()
    
    if game_state == 'menu':
        screen.fill('darkblue')
        screen.draw.text('Capybara Go!', center=(WIDTH/2, 100), fontsize=60)
        # ... (código dos botões do menu) ...
        screen.draw.filled_rect(start_button, 'green')
        screen.draw.text('Começar o Jogo', center=start_button.center, fontsize=30)
        screen.draw.filled_rect(sound_button, 'orange')
        sound_text = 'Música e Sons Ligados' if music_on else 'Música e Sons Desligados' 
        screen.draw.text(sound_text, center=sound_button.center, fontsize=25)
        screen.draw.filled_rect(exit_button, 'red')
        screen.draw.text('Sair', center=exit_button.center, fontsize=30)
    
    elif game_state == 'playing':
        screen.fill('darkgreen')
        # Desenha o chão
        screen.draw.filled_rect(Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y), 'brown')
        
        # --- AQUI ESTÁ A MUDANÇA (Desenha estrelas e score) ---
        for star in stars:
            star.draw()
            
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="yellow")
        
        player.draw()
        for skeleton in skeletons: # Modificado de 'enemies' para 'skeletons'
            skeleton.draw()
    
    # --- AQUI ESTÁ A MUDANÇA (Estado de Vitória) ---
    elif game_state == 'win':
        screen.fill('blue')
        screen.draw.text('VOCÊ VENCEU!', center=(WIDTH/2, HEIGHT/2 - 40), fontsize=80)
        screen.draw.text(f'Score Final: {score}', center=(WIDTH/2, HEIGHT/2 + 40), fontsize=60)

    elif game_state == 'game_over':
        screen.fill('black')
        screen.draw.text('FIM DE JOGO', center=(WIDTH/2, HEIGHT/2), fontsize=80)

def update(dt):
    global game_state, score, music_on # Pega as variáveis globais
    
    if music_on and not music.is_playing():
        music.play('background.mp3')
    elif not music_on:
        music.stop()

    if game_state == 'playing':
        player.update(dt) 
        for skeleton in skeletons: # Modificado de 'enemies' para 'skeletons'
            skeleton.update(dt)

        # --- AQUI ESTÁ A MUDANÇA (Lógica de Coletar Estrelas) ---
        collected_stars = []
        for star in stars:
            if player.actor.colliderect(star):
                collected_stars.append(star)
                score += 10 # Adiciona 10 pontos por estrela
                try:
                    sounds.collect.play() # 'collect.wav' deve estar em /sounds/
                except:
                    print("Arquivo de som 'collect' não encontrado")
        
        # Remove as estrelas que foram coletadas
        for star in collected_stars:
            stars.remove(star)
            
        # --- AQUI ESTÁ A MUDANÇA (Checa condição de vitória) ---
        if not stars: # Se a lista de estrelas está vazia
            game_state = 'win'

        # Checagem de colisão com o Mr. Bones
        for skeleton in skeletons:
            if player.actor.colliderect(skeleton.actor):
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
    
    # --- AQUI ESTÁ A MUDANÇA (Permite reiniciar após vencer ou perder) ---
    # Se o jogo acabou ou você venceu, qualquer clique volta ao menu
    if game_state == 'game_over' or game_state == 'win':
        # (Futuramente, você precisará de uma função para resetar o jogo)
        # game_state = 'menu' 
        # Por enquanto, apenas fechar o jogo é mais simples:
        quit()


# --- 7. Início do Jogo ---
try:
    music.play('background.mp3') 
    music.set_volume(0.3)
except:
    print("Arquivo de música 'background.mp3' não encontrado na pasta /music/")

pgzrun.go()