import pygame
import socket
import time
import sys

def client_program():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))  # Just needed to receive events
    pygame.display.set_caption('Client Input Window')

    print("Trying to connect to server")
    host = "192.168.0.227"
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    keys_held = {
        pygame.K_a: False,
        pygame.K_d: False,
        pygame.K_w: False,
        pygame.K_s: False
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key in keys_held:
                    keys_held[event.key] = True
            if event.type == pygame.KEYUP:
                if event.key in keys_held:
                    keys_held[event.key] = False

        if keys_held[pygame.K_a]:
            client_socket.send('a'.encode())
        if keys_held[pygame.K_d]:
            client_socket.send('d'.encode())
        if keys_held[pygame.K_w]:
            client_socket.send('w'.encode())
        if keys_held[pygame.K_s]:
            client_socket.send('s'.encode())

        time.sleep(0.05)  # Small delay to reduce CPU usage

    client_socket.close()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    client_program()