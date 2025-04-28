import pygame
import socket
import time
import sys

def client_program():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))  # Just needed to receive events
    pygame.display.set_caption('Client Input Window')

    print("Trying to connect to server")
    host = "192.168.0.224"
    port = 5432

    client_socket = socket.socket()
    client_socket.connect((host, port))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            running = False
        if keys[pygame.K_a]:
            client_socket.send('a'.encode())
           # time.sleep(0.1)
        if keys[pygame.K_d]:
            client_socket.send('d'.encode())
           # time.sleep(0.1)
        if keys[pygame.K_w]:
            client_socket.send('w'.encode())
           # time.sleep(0.1)
        if keys[pygame.K_s]:
            client_socket.send('s'.encode())
           # time.sleep(0.1)
       # clock.tick(60)
    
        time.sleep(0.2)  # Small delay to reduce CPU usage

    client_socket.close()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    client_program()