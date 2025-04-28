import threading
import pygame
import socket
import sys
import random
import queue
import time

name = "test"
posx = 300
posy = 200
screen_size = screen_width, screen_height = 600, 400
rect1_speed = 10
game_active = False
game_over = False


def GameThread(screen, event_queue):
    global rect1_speed
    global screen_size
    global posx
    global posy
    global game_active
    global game_over
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)

    fps = pygame.time.Clock()

    rect1 = pygame.Rect(0, 0, 25, 25)

    rect_width = 20
    rect_height = 20
    rect_speed = 2
    moving_rects = []
    spawn_interval = 5000
    spawn_interval_increment = 100
    last_spawn_time = pygame.time.get_ticks()

    score = 0
    font = pygame.font.Font(None, 40)
    score_color = (0, 0, 0)

    

    def create_moving_rect():
        x = random.randint(0, screen_width - rect_width)
        y = -rect_height
        return pygame.Rect(x, y, rect_width, rect_height)

    def reset_game():
        nonlocal moving_rects, rect_speed, spawn_interval, score, last_spawn_time
        global rect1_speed
        moving_rects = []
        rect_speed = 2
        spawn_interval = 5000
        score = 0
        rect1_speed = 15
        reset_player_position()
        last_spawn_time = pygame.time.get_ticks()

    def reset_player_position():
        global posx, posy
        posx = 300
        posy = 200

    colorRect = (shapeColor)

    while True:
        # Process events from the queue (non-blocking)
        try:
            events = event_queue.get_nowait()  # Get all events at once
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.KEYDOWN:
                #     if not game_active and not game_over:
                #         if event.key == pygame.K_SPACE:
                #             game_active = True
                #             reset_game()
                #     elif game_over:
                #         if event.key == pygame.K_r:
                #             game_over = False
        except queue.Empty:
            pass  # No events in the queue

        screen.fill(background)

        if game_active:
            rect1.center = (posx, posy)
            pygame.draw.rect(screen, colorRect, rect1)

            current_time = pygame.time.get_ticks()
            if current_time - last_spawn_time >= spawn_interval:
                moving_rects.append(create_moving_rect())
                last_spawn_time = current_time

            for i, moving_rect in enumerate(moving_rects[:]):
                moving_rect.y += rect_speed

                if moving_rect.y > screen_height:
                    game_active = False
                    game_over = True
                    break
                collision = rect1.colliderect(moving_rect)
                if collision:
                    moving_rects.pop(i)
                    if spawn_interval > spawn_interval_increment:
                        spawn_interval -= spawn_interval_increment
                    rect_speed += 0.1
                    rect1_speed += 0.2
                    score += 1
                else:
                    pygame.draw.rect(screen, colorRect, moving_rect, 6, 1)

            score_text = font.render(f"Score: {score}", True, score_color)
            screen.blit(score_text, (10, 10))

        elif game_over:
            game_over_text = font.render(f"Game Over! Final Score: {score}", True, (255, 0, 0))
            restart_text = font.render("Press R to Restart", True, (0, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))
            screen.blit(restart_text, (screen_width // 2 - 120, screen_height // 2))
        else:
            if moving_rects != []:
                reset_game()
            start_text = font.render("Press SPACE to Start", True, (0, 0, 0))
            screen.blit(start_text, (screen_width // 2 - 120, screen_height // 2))

        pygame.display.update()
        fps.tick(60)

    pygame.quit()


def ServerThread():
    global posy
    global posx
    global rect1_speed
    global screen_size
    global game_active
    global game_over

    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    print("printing host")
    s.close()
    print(host)
    port = 5432

    server_socket = socket.socket()
    server_socket.bind((host, port))
    print("Server enabled...")
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    rect1_size = 25
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        for command in data:
            print("from connected user: " + str(command))
            if command == 'w':
                if posy > 0 + rect1_speed + (rect1_size / 2):
                    posy -= rect1_speed
                else:
                    posy = 0 + (rect1_size / 2)
            if command == 's':
                if posy < screen_height - rect1_speed - (rect1_size / 2):
                    posy += rect1_speed
                else:
                    posy = screen_height - (rect1_size / 2)
            if command == 'a':
                if posx > 0 + rect1_speed + (rect1_size / 2):
                    posx -= rect1_speed
                else:
                    posx = 0 + (rect1_size / 2)
            if command == 'd':
                if posx < screen_width - rect1_speed - (rect1_size / 2):
                    posx += rect1_speed
                else:
                    posx = screen_width - (rect1_size / 2)
            if command == ' ':
                game_active = True
            if command == 'r':
                game_over = False
    conn.close()  # close the connection


if __name__ == "__main__":  # main thread
    pygame.init()
    screen_size = (600, 400)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')

    event_queue = queue.Queue()  # Create a queue for events

    t1 = threading.Thread(target=GameThread, args=(screen, event_queue))
    t2 = threading.Thread(target=ServerThread, args=[])

    t1.start()
    t2.start()

    running = True
    while running:
        events = pygame.event.get()  # Get events in the main thread
        event_queue.put(events)  # Put events into the queue
        for event in events: # handle quit event in main thread
            if event.type == pygame.QUIT:
                running = False

        time.sleep(0.01) # Add a small sleep to main thread

    pygame.quit()
    sys.exit()
