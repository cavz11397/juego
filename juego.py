import pygame
import sys
import random
import os
import time  

# Inicializar Pygame
pygame.init()

# Definir constantes
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
GRID_MARGIN = 1

# Colores
GRID_COLOR = (0, 0, 0)
RECTANGLE_COLOR = (107, 107, 107)
BUTTON_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Resultado
TP=0
TN=0
FP=0
FN=0

accuracy = 0
precision = 0
recall = 0
f1Score = 0

# Crear la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Juego de Cuadros')

# Directorio donde se encuentran las imágenes
image_directory_fresh = 'images/freshoranges'
image_directory_rotten = 'images/rottenoranges'

# Definir las ubicaciones de las imágenes específicas
image_location_fresh = 'images/bien.png'
image_location_rotten = 'images/mal.png'
image_location_question = 'images/question.jpg'

# Obtener una lista de archivos en el directorio
image_files_fresh = [os.path.join(image_directory_fresh, filename) for filename in os.listdir(image_directory_fresh) if (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'))]
image_files_rotten = [os.path.join(image_directory_rotten, filename) for filename in os.listdir(image_directory_rotten) if (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'))]

# Asegurarse de que haya al menos una imagen en el directorio
if not (image_files_fresh or image_files_rotten):
    print(f"No se encontraron imágenes en los siguientes directorios: {image_directory_fresh}, {image_files_rotten}")
    pygame.quit()
    sys.exit()

def start_game_button():
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = font.render("Cargar imagen", True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() / 2, button_rect.centery - button_text.get_height() / 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_rect.collidepoint(x, y):
                    return
                
start_game_button()

def get_grid_size():
    grid_input = ""
    font = pygame.font.Font(None, 36)
    instruction_text = font.render("Ingresa el tamaño de la matriz cuadrada de recuadros", True, (0, 0, 0))
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, 200))

    input_rect = pygame.Rect(300, 250, 100, 50)
    active = False

    while True:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            GRID_SIZE = int(grid_input)
                            return GRID_SIZE
                        except ValueError:
                            grid_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        grid_input = grid_input[:-1]
                    else:
                        grid_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False

        color = (0, 0, 0) if active else (100, 100, 100)
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = font.render(grid_input, True, (0, 0, 0))
        screen.blit(instruction_text, instruction_rect)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()


# Pedir al usuario que ingrese GRID_SIZE
# GRID_SIZE = get_grid_size()
GRID_SIZE = 6

# Elegir aleatoriamente entre naranjas frescas y podridas
def choice():
    global background_path, fresh, background
    if random.choice([True, False]):
        background_path = random.choice(image_files_fresh)
        fresh = True
    else:
        background_path = random.choice(image_files_rotten)
        fresh = False
        
    # Cargar una imagen de fondo de forma aleatoria
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
choice()

def make_grid():
    global grid_height, grid_width, grid, selected_count, showing_buttons, revealed_count, total_squares, required_percentage
    # Calcular el tamaño de cada cuadro
    grid_width = (WIDTH - (GRID_SIZE + 1) * GRID_MARGIN) // GRID_SIZE
    grid_height = (HEIGHT - (GRID_SIZE + 1) * GRID_MARGIN) // GRID_SIZE

    # Crear la cuadrícula de cuadros
    grid = [[True for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    selected_count = 0
    showing_buttons = False
    # Definir una variable para llevar el conteo de cuadros destapados
    revealed_count = 0
    # Calcular el total de cuadros
    total_squares = GRID_SIZE * GRID_SIZE
    # Calcular el porcentaje requerido de cuadros destapados
    required_percentage = 0.6

make_grid()

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (grid_width + GRID_MARGIN) + GRID_MARGIN
            y = row * (grid_height + GRID_MARGIN) + GRID_MARGIN
            pygame.draw.rect(screen, GRID_COLOR, (x, y, grid_width, grid_height), 2)
            if grid[row][col]:
                cuadro_image = pygame.image.load(image_location_question)
                cuadro_image = pygame.transform.scale(cuadro_image, (grid_width, grid_height))
                screen.blit(cuadro_image, (x, y))


# Función para mostrar los botones
def show_buttons():
    button1_rect = pygame.Rect(100, 500, 200, 50)
    button2_rect = pygame.Rect(500, 500, 200, 50)

    pygame.draw.rect(screen, BUTTON_COLOR, button1_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, button2_rect)

    font = pygame.font.Font(None, 36)
    button1_text = font.render("fresca", True, BUTTON_TEXT_COLOR)
    button2_text = font.render("podrida", True, BUTTON_TEXT_COLOR)

    screen.blit(button1_text, (button1_rect.centerx - button1_text.get_width() / 2, button1_rect.centery - button1_text.get_height() / 2))
    screen.blit(button2_text, (button2_rect.centerx - button2_text.get_width() / 2, button2_rect.centery - button2_text.get_height() / 2))

# mostrar reinicio
def show_reset():
    font = pygame.font.Font(None, 36)
    button_reiniciar_rect = pygame.Rect(10, 10, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_reiniciar_rect)
    button_reiniciar_text = font.render("Reiniciar", True, BUTTON_TEXT_COLOR)
    screen.blit(button_reiniciar_text, (button_reiniciar_rect.centerx - button_reiniciar_text.get_width() / 2, button_reiniciar_rect.centery - button_reiniciar_text.get_height() / 2))

# Dibuja un botón de reinicio

def reiniciar_juego():
    choice()
    make_grid()
    initialize()

# Bucle principal del juego
def initialize():
    global showGrid, running, lastButtons, show_thanks
    showGrid = True
    running = True
    lastButtons = False
    show_thanks = False

def rotten_oranges():
    global background, lastButtons
    background = pygame.image.load(image_location_rotten)
    lastButtons = True

def fresh_oranges():
    global background, lastButtons
    background = pygame.image.load(image_location_fresh)
    lastButtons = True

def export_variables_to_txt():
    with open("resultado.txt", "w") as file:
        file.write(f"frescaCorrecta={TP}\n")
        file.write(f"frescaIncorrecta={TN}\n")
        file.write(f"podridaCorrecta={FP}\n")
        file.write(f"podridaIncorrecta={FN}\n")
        file.write(f"Accuracy={accuracy}\n")
        file.write(f"Precision={precision}\n")
        file.write(f"Recall={recall}\n")
        file.write(f"f1-score={f1Score}\n")

def show_export_button():
    font = pygame.font.Font(None, 36)
    button_export_rect = pygame.Rect(220, 10, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_export_rect)
    button_export_text = font.render("Resultado", True, BUTTON_TEXT_COLOR)
    screen.blit(button_export_text, (button_export_rect.centerx - button_export_text.get_width() / 2, button_export_rect.centery - button_export_text.get_height() / 2))
    
    return button_export_rect

initialize()
button1_rect = pygame.Rect(100, 500, 200, 50)  # Define button1_rect
button2_rect = pygame.Rect(500, 500, 200, 50)  # Define button2_rect
button_reiniciar_rect = pygame.Rect(10, 10, 200, 50)  # Define button_reiniciar_rect
button_export_rect = pygame.Rect(220, 10, 200, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - GRID_MARGIN) // (grid_width + GRID_MARGIN)
            row = (y - GRID_MARGIN) // (grid_height + GRID_MARGIN)
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col]:
                grid[row][col] = False
                selected_count += 1
                revealed_count += 1
                if selected_count >= required_percentage * total_squares:
                    # Si todos los cuadros están seleccionados, muestra los botones
                    showing_buttons = True

    # Dibujar la imagen de fondo
    if background is not None:
        screen.blit(background, (0, 0))

# Dibujar la cuadrícula de cuadros
    if showGrid :
        draw_grid()

    if showing_buttons:
        # Mostrar los botones solo cuando se haya alcanzado el porcentaje requerido de cuadros destapados
        if revealed_count >= required_percentage * total_squares:
            show_buttons()
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if button1_rect.collidepoint(x, y):
                    if fresh:
                        fresh_oranges()
                        TP += 1
                    else:
                        rotten_oranges()
                        TN += 1
                    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                    showing_buttons = False
                elif button2_rect.collidepoint(x, y):
                    if fresh:
                        rotten_oranges()
                        FN += 1
                    else:
                        fresh_oranges()
                        FP += 1
                    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                    showing_buttons = False
        if selected_count == total_squares:
            showGrid = False

    if show_thanks:
        font = pygame.font.Font(None, 36)
        thanks_text = font.render("¡Muchas gracias por jugar!", True, (0, 0, 0))
        thanks_rect = thanks_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(thanks_text, thanks_rect)
        
        # Verifica si han pasado 2 segundos desde que se mostró el mensaje
        if time.time() - thanks_start_time >= 2:
            pygame.quit()
            sys.exit()

    if lastButtons:
        show_reset()
        show_export_button()
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if button_reiniciar_rect.collidepoint(x, y):
                reiniciar_juego()
            elif button_export_rect.collidepoint(x, y):
                accuracy =  (TP+TN)/(TP+TN+FP+FN)
                precision = TP / (TP + FP)
                recall = TP / (TP + FN)
                f1Score = 2 * ((recall * precision)/(recall + precision)) # Verificar si se hace clic en el botón de exportar
                export_variables_to_txt()  # Llamar a la función de exportación
                show_thanks = True
                thanks_start_time = time.time()  


    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
