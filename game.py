import pgzrun
import math
import random


# Game configuration
WIDTH = 800
HEIGHT = 600
TITLE = "CRYSTAL ALIEN"

game_state = "menu"
sounds_on = True


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 48
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.health = 3
        self.anim = "idle"
        self.frame = 0
        self.timer = 0

    def update(self, dt, platforms):
        self.vy += 0.8
        self.x += self.vx
        self.y += self.vy

        if self.y > HEIGHT + 50:
            self.health -= 1
            self.x = 50
            self.y = 300
            self.vy = 0
            
            if sounds_on:
                try:
                    sounds.hurt.play()
                except Exception:
                    pass
                    
            if self.health <= 0:
                global game_state
                game_state = "gameover"

        # Platform colitions
        self.on_ground = False
        for p in platforms:
            if Rect(self.x, self.y, self.w, self.h).colliderect(p):
                if self.vy > 0 and self.y < p.top:
                    self.y = p.top - self.h
                    self.vy = 0
                    self.on_ground = True

        
        if not self.on_ground:
            new_anim = "jump"
        elif abs(self.vx) > 0:
            new_anim = "walk"
        else:
            new_anim = "idle"

        if new_anim != self.anim:
            self.anim = new_anim
            self.frame = 0

        # Change animation frames
        self.timer += dt
        if self.timer > 0.15:
            self.timer = 0
            frames = {"idle": 2, "walk": 1, "jump": 2}
            self.frame = (self.frame + 1) % frames[self.anim]

    def draw(self):
        sprite = Actor(f"player_{self.anim}_right_{self.frame}")
        sprite.bottomleft = (self.x, self.y + self.h)
        sprite.draw()


class Slime:
    def __init__(self, x, y, left, right):
        self.x = x
        self.y = y
        self.left = left
        self.right = right
        self.speed = 1.5
        self.frame = 0
        self.timer = 0

    def update(self, dt):
        self.x += self.speed
        if self.x <= self.left or self.x >= self.right:
            self.speed *= -1

        self.timer += dt
        if self.timer > 0.2:
            self.timer = 0
            self.frame = (self.frame + 1) % 4

    def draw(self):
        sprite = Actor(f"slime_move_right_{self.frame}")
        sprite.bottomleft = (self.x, self.y + 25)
        sprite.draw()


class Bat:
    def __init__(self, x, y):
        self.x = x
        self.start_y = y
        self.y = y
        self.time = 0
        self.frame = 0

    def update(self, dt):
        self.time += dt
        self.y = self.start_y + math.sin(self.time * 2) * 40
        self.frame = int(self.time * 10) % 4

    def draw(self):
        sprite = Actor(f"bat_fly_{self.frame}")
        sprite.center = (self.x + 15, self.y + 10)
        sprite.draw()


# Coordinates for player-enemies-crystals position in game
player = Player(50, 300)
platforms = [
    Rect(0, 550, 800, 50),
    Rect(100, 450, 150, 20),
    Rect(300, 350, 150, 20),
    Rect(500, 250, 250, 20)
]
enemies = [
    Slime(200, 525, 150, 400),
    Bat(400, 200),
    Slime(520, 225, 500, 650)
]
crystals = [
    {"x": 160, "y": 350, "got": False},
    {"x": 360, "y": 250, "got": False},
    {"x": 560, "y": 150, "got": False}
]

goal = Rect(680, 150, 40, 50)
score = 0
mouse_pos = (0, 0)


def draw_button(x, y, w, h, text):
    button_rect = Rect(x, y, w, h)
    color = "yellow" if button_rect.collidepoint(mouse_pos) else "white"
    screen.draw.filled_rect(button_rect, color)
    screen.draw.text(
        text,
        center=(x + w // 2, y + h // 2),
        fontsize=25,
        color="black"
    )


def draw():
    screen.clear()
    
    if game_state == "menu":
        screen.fill((20, 20, 50))
        screen.draw.text(
            "CRYSTAL ALIEN",
            center=(400, 150),
            fontsize=60,
            color="gold",
            shadow=(2, 2)
        )
        draw_button(275, 300, 250, 50, "START GAME")
        
        sound_text = f"MUSIC/SOUNDS: {'ON' if sounds_on else 'OFF'}"
        draw_button(275, 370, 250, 50, sound_text)
        draw_button(275, 440, 250, 50, "EXIT")

    elif game_state == "playing":
        screen.fill((135, 206, 235))

        for p in platforms:
            for i in range(0, p.width, 32):
                screen.blit("platform_tile", (p.x + i, p.y))

        for c in crystals:
            if not c["got"]:
                screen.blit("crystal", (c["x"], c["y"]))

        screen.blit("goal_flag", (goal.x, goal.y))

        for e in enemies:
            e.draw()
            
        player.draw()

        screen.draw.text(
            f"Score: {score}",
            (10, 10),
            fontsize=30,
            color="white",
            shadow=(1, 1)
        )
        
        for i in range(player.health):
            screen.blit("heart", (10 + i * 35, 45))

    elif game_state in ["gameover", "victory"]:
        screen.fill("black")
        msg = "GAME OVER" if game_state == "gameover" else "VICTORY!"
        msg_color = "red" if game_state == "gameover" else "gold"
        screen.draw.text(
            msg,
            center=(400, 250),
            fontsize=70,
            color=msg_color
        )


def update(dt):
    global game_state, score
    
    if game_state != "playing":
        return

    #  Game controls
    if keyboard.right:
        player.vx = 4
    elif keyboard.left:
        player.vx = -4
    else:
        player.vx = 0

    if keyboard.up and player.on_ground:
        player.vy = -12
        if sounds_on:
            try:
                sounds.jump.play()
            except Exception:
                pass

    player.update(dt, platforms)
    for e in enemies:
        e.update(dt)

    # Collect Crystals
    player_rect = Rect(player.x, player.y, player.w, player.h)
    
    for c in crystals:
        crystal_rect = Rect(c["x"], c["y"], 20, 20)
        if not c["got"] and player_rect.colliderect(crystal_rect):
            c["got"] = True
            score += 10
            if sounds_on:
                try:
                    sounds.coin.play()
                except Exception:
                    pass

    # Enemy colission
    for e in enemies:
        ew, eh = (35, 25) if isinstance(e, Slime) else (30, 20)
        enemy_rect = Rect(e.x, e.y, ew, eh)
        
        if player_rect.colliderect(enemy_rect):
            player.health -= 1
            player.x = 50
            player.y = 300
            player.vy = 0
            
            if sounds_on:
                try:
                    sounds.hurt.play()
                except Exception:
                    pass
                    
            if player.health <= 0:
                game_state = "gameover"

    # Victory condition
    all_crystals = all(c["got"] for c in crystals)
    if all_crystals and player_rect.colliderect(goal):
        game_state = "victory"


def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos


def on_mouse_down(pos):
    global game_state, sounds_on, score
    
    if game_state == "menu":
        if Rect(275, 300, 250, 50).collidepoint(pos):
            game_state = "playing"
            player.health = 3
            score = 0
            player.x = 50
            player.y = 300
            player.vy = 0
            
            for c in crystals:
                c["got"] = False
                
            if sounds_on:
                try:
                    music.play("bg_music")
                except Exception:
                    pass
                    
        elif Rect(275, 370, 250, 50).collidepoint(pos):
            sounds_on = not sounds_on
            if not sounds_on:
                try:
                    music.stop()
                except Exception:
                    pass
                    
        elif Rect(275, 440, 250, 50).collidepoint(pos):
            exit()
            
    elif game_state in ["gameover", "victory"]:
        game_state = "menu"
        try:
            music.stop()
        except Exception:
            pass


pgzrun.go()