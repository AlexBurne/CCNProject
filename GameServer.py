import threading
import pygame
import socket
import sys
import random

name = "test"
posx = 300
posy = 200

def GameThread():
    pygame.init()
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)
    
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 600, 400
    rect1 = pygame.Rect(0, 0, 25, 25)

    rect_width = 20
    rect_height = 20
    rect_speed = 2
    num_rects = 3
    moving_rects = []

    def create_moving_rect():
        #creates a single moving rectangle
        x = random.randint(0, screen_width - rect_width)
        y = -rect_height
        return pygame.Rect(x, y, rect_width, rect_height)
    
    def reset_moving_rect(rect):
        #resets a moving rectangle
        rect.x = random.randint(0, screen_width - rect_width)
        rect.y = -rect_height

    for _ in range(num_rects):
        moving_rects.append(create_moving_rect())

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')
    
    colorRect = (shapeColor)
    colorRect2 = (shapeColorOver)
    global posx 
    global posy 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background)
        rect1.center = (posx, posy)
        
        pygame.draw.rect(screen, colorRect, rect1)
        
        for moving_rect in moving_rects:
            moving_rect.y += rect_speed
            if moving_rect.y > screen_height:
                reset_moving_rect(moving_rect)
            collision = rect1.colliderect(moving_rect)
            if collision:
                pygame.draw.rect(screen, colorRect2, moving_rect, 6, 1)
            else:
                pygame.draw.rect(screen, colorRect, moving_rect, 6, 1) 

        pygame.display.update()
        fps.tick(60)


    pygame.quit()


def ServerThread():
    global posy
    global posx
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    print("printing host")
    s.close()
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        for command in data:
            print("from connected user: " + str(command))
            if(command == 'w'):
                posy -= 10
            if(command == 's'):
                posy += 10
            if(command == 'a'):
                posx -= 10
            if(command == 'd'):
                posx += 10
    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
#t1.daemon = True
t2 = threading.Thread(target=ServerThread, args=[])
#t2.daemon = True
t1.start()
t2.start()