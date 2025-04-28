import threading
import pygame
import socket
import sys
import random

name = "test"
posx = 300
posy = 200
screen_size = screen_width, screen_height = 600, 400
rect1_speed = 10

def GameThread(screen):
    global rect1_speed
    global screen_size
    global posx
    global posy
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)

    fps = pygame.time.Clock()

    rect1 = pygame.Rect(0, 0, 25, 25)

    #falling object variables
    rect_width = 20
    rect_height = 20
    rect_speed = 2
    moving_rects = []
    spawn_interval = 5000 #in milliseconds
    spawn_interval_increment = 100
    last_spawn_time = pygame.time.get_ticks()

    #score variables
    score = 0
    font = pygame.font.Font(None, 40)
    score_color = (0, 0, 0)

    def create_moving_rect():
        #creates a single moving rectangle
        x = random.randint(0, screen_width - rect_width)
        y = -rect_height
        return pygame.Rect(x, y, rect_width, rect_height)

    def reset_moving_rect(rect):
        #resets a moving rectangle
        rect.x = random.randint(0, screen_width - rect_width)
        rect.y = -rect_height

    colorRect = (shapeColor)
    colorRect2 = (shapeColorOver)

    while True:
        screen.fill(background)
        rect1.center = (posx, posy)

        pygame.draw.rect(screen, colorRect, rect1)

        #spawn in moving rects
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= spawn_interval:
            moving_rects.append(create_moving_rect())
            last_spawn_time = current_time

        for i, moving_rect in enumerate(moving_rects):
            moving_rect.y += rect_speed

            # CONDITION FOR WHEN AN OBJECT REACHES THE BOTTOM
            # YOU CAN EDIT THIS TO CHANGE TO END THE GAME
            if moving_rect.y > screen_height:
                moving_rects.pop(i)
            collision = rect1.colliderect(moving_rect)
            if collision:
                moving_rects.pop(i) #removes object when touched

                #speeds up spawn rate until it is nearly above 0
                if(spawn_interval > spawn_interval_increment):
                    spawn_interval -= spawn_interval_increment

                rect_speed += 0.1
                rect1_speed += 0.2
                score += 1
                #moving_rects.append(create_moving_rect()) #create a new object
            else:
                pygame.draw.rect(screen, colorRect, moving_rect, 6, 1)

        #display score
        score_text = font.render(f"Score: {score}", True, score_color)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        fps.tick(60)

    pygame.quit()


def ServerThread():
    global posy
    global posx
    global rect1_speed
    global screen_size
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    print("printing host")
    s.close()
    print(host)
    port = 5432  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    rect1_size = 25
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        for command in data:
            print("from connected user: " + str(command))
            if(command == 'w'):
                if(posy > 0 + rect1_speed + (rect1_size/2)):
                    posy -= rect1_speed
                else:
                    posy = 0 + (rect1_size/2)
            if(command == 's'):
                if(posy < screen_height - rect1_speed - (rect1_size/2)):
                    posy += rect1_speed
                else:
                    posy = screen_height - (rect1_size/2)
            if(command == 'a'):
                if(posx > 0 + rect1_speed + (rect1_size/2)):
                    posx -= rect1_speed
                else:
                    posx = 0 + (rect1_size/2)
            if(command == 'd'):
                if(posx < screen_width - rect1_speed - (rect1_size/2)):
                    posx += rect1_speed
                else:
                    posx = screen_width - (rect1_size/2)
    conn.close()  # close the connection

if __name__ == "__main__": #main thread
    pygame.init()
    screen_size = (600, 400)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')

    t1 = threading.Thread(target=GameThread, args=(screen, ))
    t2 = threading.Thread(target=ServerThread, args=[])

    t1.start()
    t2.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()