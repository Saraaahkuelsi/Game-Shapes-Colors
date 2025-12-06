import pygame
import random
import math

pygame.init()
pygame.mixer.init()
sound_success = pygame.mixer.Sound("success-videogame-sfx-423626.mp3")

# ---- Fenêtre ----
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shapes & Colors")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
button_font = pygame.font.SysFont(None, 40)

# ---- Couleurs et formes ----
colors = [
    (0, 255, 0),    # vert
    (0, 0, 255),    # bleu
    (255, 255, 0),  # jaune
    (255, 0, 255),  # magenta
    (0, 255, 255) ,# cyan
    (255,0,0)  #  red
]
shape_types = ["circle", "square", "triangle", "joker"]
UI_HEIGHT = 120  # Zone interface en haut

# ---- Fonctions pour dessiner ----
def draw_triangle(surface, color, x, y, size):
    points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
    pygame.draw.polygon(surface, color, points)

def draw_star(surface, color, x, y, size):
    points = [
        (x, y - size),
        (x + size*0.2245, y - size*0.309),
        (x + size, y - size*0.309),
        (x + size*0.363, y + size*0.118),
        (x + size*0.5878, y + size*0.809),
        (x, y + size*0.382),
        (x - size*0.5878, y + size*0.809),
        (x - size*0.363, y + size*0.118),
        (x - size, y - size*0.309),
        (x - size*0.2245, y - size*0.309)
    ]
    pygame.draw.polygon(surface, color, points)

# ---- Animation du titre centré dans un carré ----
def draw_animated_title(surface, frame_count, rect_x, rect_y, rect_size):
    line1 = "Shapes"
    line2 = "&"
    line3 = "Colors"
    big_font = pygame.font.SysFont(None, 60, bold=True)

    # Couleur par lettre
    def get_color(i):
        return colors[i % len(colors)]

    # Pré-rendu des surfaces
    line_surfaces = [
        big_font.render(line1, True, (0,0,0)),
        big_font.render(line2, True, (0,0,0)),
        big_font.render(line3, True, (0,0,0))
    ]

    # Hauteur totale pour centrer verticalement
    total_height = sum([surf.get_height() for surf in line_surfaces]) + 20  # espace entre lignes
    start_y = rect_y + (rect_size - total_height)//2

    for line_index, line in enumerate([line1, line2, line3]):
        total_width = sum([big_font.render(c, True, (0,0,0)).get_width() for c in line])
        start_x = rect_x + (rect_size - total_width)//2  # centré horizontalement

        x = start_x
        y_offset = start_y + line_index * (line_surfaces[line_index].get_height() + 10)
        for i, letter in enumerate(line):
            color = get_color(i)
            letter_surface = big_font.render(letter, True, color)
            surface.blit(letter_surface, (x, y_offset + int(math.sin(frame_count*0.1 + i) * 5)))
            x += letter_surface.get_width()

# ---- Écran de fin ----
def end_screen(score):
    restart_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
    running_end = True
    while running_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_end = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    running_end = False
                    start_game()

        screen.fill((20, 20, 60))
        rect_width, rect_height = 400, 150
        rect_x = WIDTH//2 - rect_width//2
        rect_y = HEIGHT//2 - rect_height//2
        s = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 180))
        screen.blit(s, (rect_x, rect_y))

        big_font = pygame.font.SysFont(None, 60)
        end_text = big_font.render("Bravo !", True, (0, 0, 0))
        screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, rect_y + 20))
        score_text = font.render(f"Ton score est : {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, rect_y + 100))

        pygame.draw.rect(screen, (200, 200, 200), restart_rect)
        restart_text = button_font.render("Restart", True, (0, 0, 0))
        screen.blit(restart_text,(restart_rect.x + (restart_rect.width - restart_text.get_width())//2,
                                  restart_rect.y + (restart_rect.height - restart_text.get_height())//2))

        pygame.display.flip()
        clock.tick(60)

# ---- Jeu ----
def start_game():
    initial_speed = 2
    shapes = []
    for i in range(30):
        shape_type = random.choice(["circle", "square", "triangle"])
        shape_color = random.choice(colors)
        shapes.append({
            "type": shape_type,
            "x": random.randint(50, WIDTH-50),
            "y": random.randint(-300, -UI_HEIGHT),
            "speed": initial_speed,
            "size": 30,
            "color": shape_color
        })
    joker = {"type":"joker","x":random.randint(50,WIDTH-50),"y":random.randint(-300,-UI_HEIGHT),
             "speed": initial_speed,"size":30,"color":(255,0,0)}
    shapes.append(joker)

    game_duration=150000
    start_time=pygame.time.get_ticks()
    score = 0
    mode = random.choice(["shape", "color"])
    target_shape = random.choice(["circle", "square", "triangle"]) if mode=="shape" else None
    target_color = random.choice(colors) if mode=="color" else None
    change_time = 12000
    last_change = pygame.time.get_ticks()

    running_game = True
    while running_game:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or current_time - start_time >= game_duration:
                running_game = False
                end_screen(score)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if mouse_y < UI_HEIGHT: continue
                for shape in shapes:
                    x, y, size = shape["x"], shape["y"], shape["size"]
                    valid = False
                    if shape["type"]=="circle":
                        if ((mouse_x-x)**2 + (mouse_y-y)**2)**0.5 <= size:
                            valid = True
                    else:
                        if x-size <= mouse_x <= x+size and y-size <= mouse_y <= y+size:
                            valid = True
                    if valid:
                        if shape["type"]=="joker":
                            sound_success.play()
                            score += 5
                            shape["y"] = random.randint(-300, -UI_HEIGHT)
                            shape["x"] = random.randint(50, WIDTH-50)
                        elif (mode=="shape" and shape["type"]==target_shape) or (mode=="color" and shape["color"]==target_color):
                            sound_success.play()
                            score += 2
                            shape["y"] = random.randint(-300, -UI_HEIGHT)
                            shape["x"] = random.randint(50, WIDTH-50)
                            if shape["type"] != "joker":
                                shape["color"] = random.choice(colors)

        if current_time - last_change > change_time:
            last_change = current_time
            mode = "shape" if mode=="color" else "color"
            target_shape = random.choice(["circle","square","triangle"]) if mode=="shape" else None
            target_color = random.choice(colors) if mode=="color" else None

        # Fond
        screen.fill((20,20,60))
        pygame.draw.rect(screen,(10,10,40),(0,0,WIDTH,UI_HEIGHT))

        # Update + draw shapes
        for shape in shapes:
            shape["y"] += shape["speed"]
            if shape["y"] - shape["size"] > HEIGHT:
                shape["y"] = random.randint(-300,-UI_HEIGHT)
                shape["x"] = random.randint(50,WIDTH-50)
                if shape["type"] != "joker":
                    shape["color"] = random.choice(colors)
            x,y,size,color = shape["x"],shape["y"],shape["size"],shape["color"]
            if shape["type"]=="circle":
                pygame.draw.circle(screen,color,(x,int(y)),size)
            elif shape["type"]=="square":
                pygame.draw.rect(screen,color,(x-size,int(y)-size,size*2,size*2))
            elif shape["type"]=="triangle":
                draw_triangle(screen,color,x,int(y),size)
            elif shape["type"]=="joker":
                draw_star(screen,color,x,int(y),size)

        # Score et temps
        score_text = font.render(f"Score : {score}", True, (255,255,255))
        screen.blit(score_text,(20,20))
        time_left = max(0, (game_duration - (current_time - start_time)) // 1000)
        time_text = font.render(f"Temps : {time_left}s", True, (255,255,255))
        screen.blit(time_text,(WIDTH//2 - 50,20))

        # Consigne
        icon_x = WIDTH - 50
        icon_y = 40
        size_icon = 30
        if mode=="shape":
            text = font.render("Forme :",True,(255,255,255))
            screen.blit(text,(WIDTH-200,20))
            if target_shape=="circle":
                pygame.draw.circle(screen,(255,255,255),(icon_x,icon_y),size_icon)
            elif target_shape=="square":
                pygame.draw.rect(screen,(255,255,255),(icon_x-size_icon,icon_y-size_icon,size_icon*2,size_icon*2))
            elif target_shape=="triangle":
                points=[(icon_x,icon_y-size_icon),(icon_x-size_icon,icon_y+size_icon),(icon_x+size_icon,icon_y+size_icon)]
                pygame.draw.polygon(screen,(255,255,255),points)
        else:
            text = font.render("Couleur :",True,(255,255,255))
            screen.blit(text,(WIDTH-200,20))
            pygame.draw.rect(screen,target_color,(icon_x-size_icon,icon_y-size_icon,size_icon*2,size_icon*2))

        pygame.display.flip()
        clock.tick(60)

# ---- Écran d'intro ----
def intro_screen():
    NUM_SHAPES = 50
    intro_shapes = []
    frame_count = 0
    for _ in range(NUM_SHAPES):
        shape = {
            "type": random.choice(shape_types),
            "x": random.randint(50, WIDTH-50),
            "y": random.randint(-600, -50),
            "size": random.randint(20, 40),
            "color": random.choice(colors),
            "speed": random.uniform(1, 4)
        }
        intro_shapes.append(shape)

    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)
    running = True
    while running:
        screen.fill((30,30,60))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
                    start_game()

        for shape in intro_shapes:
            shape["y"] += shape["speed"]
            if shape["y"]-shape["size"] > HEIGHT:
                shape["y"] = random.randint(-600,-50)
                shape["x"] = random.randint(50,WIDTH-50)
                shape["color"] = random.choice(colors)
                shape["type"] = random.choice(shape_types)
                shape["size"] = random.randint(20,40)
                shape["speed"] = random.uniform(1,4)
            if shape["type"]=="circle":
                pygame.draw.circle(screen, shape["color"], (shape["x"], int(shape["y"])), shape["size"])
            elif shape["type"]=="square":
                pygame.draw.rect(screen, shape["color"], (shape["x"]-shape["size"], int(shape["y"])-shape["size"], shape["size"]*2, shape["size"]*2))
            elif shape["type"]=="triangle":
                draw_triangle(screen, shape["color"], shape["x"], int(shape["y"]), shape["size"])
            elif shape["type"]=="joker":
                draw_star(screen, shape["color"], shape["x"], int(shape["y"]), shape["size"])
        frame_count += 1

        # Carré noir semi-transparent pour le titre
        TITLE_RECT_SIZE = 180
        TITLE_RECT_X = WIDTH//2 - TITLE_RECT_SIZE//2
        TITLE_RECT_Y = 40
        s = pygame.Surface((TITLE_RECT_SIZE, TITLE_RECT_SIZE), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        screen.blit(s, (TITLE_RECT_X, TITLE_RECT_Y))

        # Animation du titre centré dans le carré
        draw_animated_title(screen, frame_count, TITLE_RECT_X, TITLE_RECT_Y, TITLE_RECT_SIZE)

        # Bouton START
        pygame.draw.rect(screen,(200,200,200),button_rect)
        start_text = button_font.render("START",True,(0,0,0))
        screen.blit(start_text,(button_rect.x+(button_rect.width-start_text.get_width())//2,
                                button_rect.y+(button_rect.height-start_text.get_height())//2))

        pygame.display.flip()
        clock.tick(60)

# ---- Lancer l'intro ----
intro_screen()
pygame.quit()
