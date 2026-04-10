import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
FPS = 60

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 10

# Colors for skins
SKIN_COLORS = {
    "default": WHITE,
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128)
}

class Paddle:
    def __init__(self, x, y, skin="default"):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.skin = skin
        self.color = SKIN_COLORS.get(skin, WHITE)

    def move(self, dy):
        if self.rect.top + dy >= 0 and self.rect.bottom + dy <= HEIGHT:
            self.rect.y += dy

    def set_skin(self, skin):
        if skin in SKIN_COLORS:
            self.skin = skin
            self.color = SKIN_COLORS[skin]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-5, 5])
        self.dy = random.choice([-5, 5])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1
        
    def reset(self):
        self.rect.x = WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        self.dx = random.choice([-5, 5])
        self.dy = random.choice([-5, 5])

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, self.rect)

class BattlePass:
    def __init__(self):
        self.available_skins = list(SKIN_COLORS.keys())
        self.left_paddle_skin = "default"
        self.right_paddle_skin = "default"
        self.current_selection = "left"

    def cycle_left_skin(self):
        current_index = self.available_skins.index(self.left_paddle_skin)
        self.left_paddle_skin = self.available_skins[(current_index + 1) % len(self.available_skins)]

    def cycle_right_skin(self):
        current_index = self.available_skins.index(self.right_paddle_skin)
        self.right_paddle_skin = self.available_skins[(current_index + 1) % len(self.available_skins)]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong - Control Left with WASD, Right with ARROWS")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.paddle_left = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, "default")
        self.paddle_right = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, "default")
        self.ball = Ball()
        self.battle_pass = BattlePass()
        
        # Try to load sound, but don't crash if it fails
        try:
            self.hit_sound = pygame.mixer.Sound("kurt_cobain_moan.wav")
        except:
            self.hit_sound = None
            print("Warning: kurt_cobain_moan.wav not found. Game will run without sound.")
        
        self.left_score = 0
        self.right_score = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Change left paddle skin
                    self.battle_pass.cycle_left_skin()
                    self.paddle_left.set_skin(self.battle_pass.left_paddle_skin)
                if event.key == pygame.K_2:  # Change right paddle skin
                    self.battle_pass.cycle_right_skin()
                    self.paddle_right.set_skin(self.battle_pass.right_paddle_skin)

        keys = pygame.key.get_pressed()
        # Left paddle - WASD
        if keys[pygame.K_w]:
            self.paddle_left.move(-7)
        if keys[pygame.K_s]:
            self.paddle_left.move(7)
        
        # Right paddle - Arrow keys
        if keys[pygame.K_UP]:
            self.paddle_right.move(-7)
        if keys[pygame.K_DOWN]:
            self.paddle_right.move(7)
        
        return True

    def check_collision(self):
        if self.ball.rect.colliderect(self.paddle_left.rect):
            if self.hit_sound:
                self.hit_sound.play()
            self.ball.dx = abs(self.ball.dx)
            self.ball.rect.x = self.paddle_left.rect.right
            
        if self.ball.rect.colliderect(self.paddle_right.rect):
            if self.hit_sound:
                self.hit_sound.play()
            self.ball.dx = -abs(self.ball.dx)
            self.ball.rect.x = self.paddle_right.rect.left - self.ball.rect.width

    def update_score(self):
        if self.ball.rect.x < 0:
            self.right_score += 1
            self.ball.reset()
        elif self.ball.rect.x > WIDTH:
            self.left_score += 1
            self.ball.reset()

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw center line
        for y in range(0, HEIGHT, 20):
            pygame.draw.line(self.screen, GRAY, (WIDTH // 2, y), (WIDTH // 2, y + 10), 2)
        
        # Draw paddles and ball
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        left_text = self.font.render(str(self.left_score), True, WHITE)
        right_text = self.font.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_text, (WIDTH // 4, 20))
        self.screen.blit(right_text, (3 * WIDTH // 4, 20))
        
        # Draw skin info
        skin_info = self.small_font.render(f"Left Skin: {self.battle_pass.left_paddle_skin} (Press 1) | Right Skin: {self.battle_pass.right_paddle_skin} (Press 2)", True, GRAY)
        self.screen.blit(skin_info, (10, HEIGHT - 30))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.ball.move()
            self.check_collision()
            self.update_score()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()