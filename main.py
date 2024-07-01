import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

TILE_SIZE = 40
TILE_COUNT = 27
BOARD_SIZE = TILE_SIZE * TILE_COUNT

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

# Load assets

## Load font
game_font = pygame.font.Font("Fonts/Minecraft.ttf", 32)
game_font_color = pygame.Color("navajowhite4")

## Load sounds
crunch_sfx = pygame.mixer.Sound("Sounds/crunch.wav")


class PlayerSnakeNode:
    def __init__(self, prev, next, x_direction, y_direction, x, y, sprite):
        self.prev: PlayerSnakeNode = prev
        self.next: PlayerSnakeNode = next
        self.x_direction: int = x_direction
        self.y_direction: int = y_direction
        self.sprite: pygame.Surface = sprite
        self.rect: pygame.Rect = self.sprite.get_rect(
            topleft=(x, y), width=40, height=40
        )


class Apple:
    def __init__(self):
        random_number_1 = random.randint(0, BOARD_SIZE)
        random_number_2 = random.randint(0, BOARD_SIZE)
        random_number_1 -= random_number_1 % TILE_SIZE
        random_number_2 -= random_number_2 % TILE_SIZE
        self.sprite: pygame.Surface = pygame.image.load("Graphics/apple.png")
        self.rect: pygame.Rect = self.sprite.get_rect(
            topleft=(random_number_1, random_number_2), width=40, height=40
        )

    def change_position(self):
        random_number_1 = random.randint(0, BOARD_SIZE)
        random_number_2 = random.randint(0, BOARD_SIZE)
        random_number_1 -= random_number_1 % TILE_SIZE
        random_number_2 -= random_number_2 % TILE_SIZE

        self.rect.x = random_number_1
        self.rect.y = random_number_2


# Initialize player snake
score = 0
head = PlayerSnakeNode(
    None, None, 1, 0, 2 * TILE_SIZE, 0, pygame.image.load("Graphics/head_right.png")
)
tail = PlayerSnakeNode(
    None, None, 1, 0, TILE_SIZE, 0, pygame.image.load("Graphics/tail_left.png")
)
extra = PlayerSnakeNode(
    tail, head, 1, 0, TILE_SIZE, 0, pygame.image.load("Graphics/body_horizontal.png")
)

tail.next = extra
head.prev = extra

# Make an apple and place it in a random spot
apple = Apple()


# Functions to alter the snek
def insert_node():
    global tail
    new = PlayerSnakeNode(
        None,
        tail,
        tail.x_direction,
        tail.y_direction,
        tail.rect.x,
        tail.rect.y,
        tail.sprite,
    )
    new.sprite = tail.sprite
    tail.prev = new
    tail = new


def swap_head_tail():
    global head
    global tail

    current = head
    while current != None:
        temp = current.prev
        current.x_direction = current.x_direction * -1
        current.y_direction = current.y_direction * -1
        current.prev = current.next
        current.next = temp
        current = current.next

    swap_temp = head
    head = tail
    tail = swap_temp

    current = tail
    while current != head:
        current.x_direction = current.next.x_direction
        current.y_direction = current.next.y_direction
        current = current.next


# Game loop
while True:

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    if head.y_direction != 1:
                        head.x_direction = 0
                        head.y_direction = -1
                    print("up")
                    break
                case pygame.K_a:
                    if head.x_direction != 1:
                        head.x_direction = -1
                        head.y_direction = 0
                    print("left")
                    break
                case pygame.K_s:
                    if head.y_direction != -1:
                        head.x_direction = 0
                        head.y_direction = 1
                    print("down")
                    break
                case pygame.K_d:
                    if head.x_direction != -1:
                        head.x_direction = 1
                        head.y_direction = 0
                    print("right")
                    break
                case pygame.K_f:
                    swap_head_tail()
                    break

    delta_t = clock.tick(8)
    screen.fill(pygame.Color("moccasin"))

    # Draw background
    for row in range(TILE_COUNT):
        if row % 2 == 0:
            for col in range(TILE_COUNT):
                if col % 2 == 0:
                    background_rect = pygame.Rect(
                        col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    pygame.draw.rect(
                        screen, pygame.Color("navajowhite1"), background_rect
                    )
        else:
            for col in range(TILE_COUNT):
                if col % 2 != 0:
                    background_rect = pygame.Rect(
                        col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    pygame.draw.rect(
                        screen, pygame.Color("navajowhite2"), background_rect
                    )

    # Draw controls
    controls_text = "W,A,S,D to move   |   F to reverse"
    controls_surface = game_font.render(controls_text, False, game_font_color)
    controls_text_position = (20, BOARD_SIZE - 20)
    controls_rect = controls_surface.get_rect(bottomleft=controls_text_position)
    screen.blit(controls_surface, controls_rect)

    # Draw score
    score_text = "Score: " + str(score)
    score_surface = game_font.render(score_text, False, game_font_color)
    score_position = (BOARD_SIZE - 20, BOARD_SIZE - 20)
    score_rect = score_surface.get_rect(bottomright=score_position)
    screen.blit(score_surface, score_rect)

    # Blit the apple
    screen.blit(apple.sprite, (apple.rect.x, apple.rect.y))

    # Tail
    match tail.next.x_direction:
        case 1:
            tail.sprite = pygame.image.load("Graphics/tail_left.png")
        case -1:
            tail.sprite = pygame.image.load("Graphics/tail_right.png")
    match tail.next.y_direction:
        case -1:
            tail.sprite = pygame.image.load("Graphics/tail_down.png")
        case 1:
            tail.sprite = pygame.image.load("Graphics/tail_up.png")
    tail.rect.x = tail.next.rect.x
    tail.rect.y = tail.next.rect.y
    tail.x_direction = tail.next.x_direction
    tail.y_direction = tail.next.y_direction

    screen.blit(tail.sprite, (tail.rect.x, tail.rect.y))
    temp = tail.next

    # Body
    while temp != head:
        temp.rect.x = temp.next.rect.x
        temp.rect.y = temp.next.rect.y

        if temp.y_direction == 0:
            temp.sprite = pygame.image.load("Graphics/body_horizontal.png")
        else:
            temp.sprite = pygame.image.load("Graphics/body_vertical.png")

        if (
            temp.prev.x_direction == -1
            and temp.next.y_direction == -1
            or temp.prev.y_direction == 1
            and temp.next.x_direction == 1
        ):
            temp.sprite = pygame.image.load("Graphics/body_topright.png")
        elif (
            temp.prev.x_direction == 1
            and temp.next.y_direction == -1
            or temp.prev.y_direction == 1
            and temp.next.x_direction == -1
        ):
            temp.sprite = pygame.image.load("Graphics/body_topleft.png")
        elif (
            temp.prev.x_direction == -1
            and temp.next.y_direction == 1
            or temp.prev.y_direction == -1
            and temp.next.x_direction == 1
        ):
            temp.sprite = pygame.image.load("Graphics/body_bottomright.png")
        elif (
            temp.prev.x_direction == 1
            and temp.next.y_direction == 1
            or temp.prev.y_direction == -1
            and temp.next.x_direction == -1
        ):
            temp.sprite = pygame.image.load("Graphics/body_bottomleft.png")
        elif temp != head.prev:
            temp.sprite = temp.next.sprite

        temp.x_direction = temp.next.x_direction
        temp.y_direction = temp.next.y_direction
        screen.blit(temp.sprite, (temp.rect.x, temp.rect.y))

        temp = temp.next

    # Head (directions already set in event loop)
    match head.x_direction:
        case 1:
            head.sprite = pygame.image.load("Graphics/head_right.png")
            head.rect.x += TILE_SIZE
        case -1:
            head.sprite = pygame.image.load("Graphics/head_left.png")
            head.rect.x -= TILE_SIZE
    match head.y_direction:
        case -1:
            head.sprite = pygame.image.load("Graphics/head_up.png")
            head.rect.y -= TILE_SIZE
        case 1:
            head.sprite = pygame.image.load("Graphics/head_down.png")
            head.rect.y += TILE_SIZE

    screen.blit(head.sprite, (head.rect.x, head.rect.y))

    # Check head and body/tail collision
    temp = tail
    while temp != head.prev:
        if head.rect.colliderect(temp.rect):
            pygame.display.update()
            pygame.quit()
            sys.exit()
        temp = temp.next

    # Check head and wall collision
    if (
        head.rect.x > BOARD_SIZE
        or head.rect.x < 0
        or head.rect.y > BOARD_SIZE
        or head.rect.y < 0
    ):
        pygame.display.update()
        pygame.quit()
        sys.exit()

    # Check head and apple collision
    if head.rect.colliderect(apple.rect):
        insert_node()
        score += 1
        crunch_sfx.play()
        apple.change_position()

    pygame.display.update()