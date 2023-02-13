from time import sleep
import pygame
import sys
import socket
import threading

p1velo = 0
p1score = 0
p2velo = 0
p2score = 0
done = False
timeout = 0
server_created = False
client = None

def listen_input(client):
    global p1velo
    while True:
        p1velo = int(client.recv(1024).decode())


def main():
    global server_created, p1score, p2score, done, timeout, client, p1velo, p2velo
    if not server_created:
        server = socket.socket()
        server.bind(("localhost", 10110))
        server.listen(1)
        print("Waiting for another player.")
        client, address = server.accept()
        c_input = threading.Thread(target=listen_input, args=(client, ))
        c_input.start()
        print(address, "connected to the server. Game is starting..")
        server_created = True
    pygame.init()
    pygame.display.set_caption("Pong Sockets | Host")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
    font = pygame.font.SysFont('arial', 50)
    newfont = pygame.font.SysFont('arial', 30)

    score1_screen_obj = font.render(str(p1score), True, (255, 255, 255), (0, 0, 0))
    score1_rect_obj = score1_screen_obj.get_rect()
    score1_rect_obj.center = (800/2 - 30, 40)

    score2_screen_obj = font.render(str(p2score), True, (255, 255, 255), (0, 0, 0))
    score2_rect_obj = score2_screen_obj.get_rect()
    score2_rect_obj.center = (800/2 + 30, 40)

    sball_y = 1
    sball_x = 1

    ball = pygame.Rect(800/2 - 7, 800/2 - 110, 15, 15)

    player1 = pygame.Rect(800 - 9, 800/2 - 130, 7, 60)
    
    player2 = pygame.Rect(0, 800/2 - 130, 7, 60)
   
    while True:
        if p1score >= 5:
            winner = "Left"
            winner_screen_obj = newfont.render(str(winner + " Won! You can close the game to restart."), True, (255, 255, 255), (0, 0, 0))
            winner_rect_obj = winner_screen_obj.get_rect()
            winner_rect_obj.center = (800/2, 300)
            timeout += 1
            sball_y = 0
            sball_x = 0
            done = True
        elif p2score >= 5:
            winner = "Right"
            winner_screen_obj = newfont.render(str(winner + " Won! You can close the game to restart."), True, (255, 255, 255), (0, 0, 0))
            winner_rect_obj = winner_screen_obj.get_rect()
            winner_rect_obj.center = (800/2, 300)
            timeout += 1
            sball_y = 0
            sball_x = 0
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    p2velo -= 1
                    client.send(bytes(str(p2velo), "utf-8"))
                if event.key == pygame.K_s:
                    p2velo += 1
                    client.send(bytes(str(p2velo), "utf-8"))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    p2velo = 0
                    client.send(bytes(str(p2velo), "utf-8"))
                if event.key == pygame.K_s:
                    p2velo = 0
                    client.send(bytes(str(p2velo), "utf-8"))
                    

        ball.x += sball_x
        ball.y += sball_y
        player1.y += p1velo
        player2.y += p2velo

        if ball.top <= 0 or ball.bottom >= 600:
            sball_y *= -1
        if ball.left <= 0:
            p2score += 1
            main()
        if ball.right >= 800:
            p1score += 1
            main()
        if ball.colliderect(player1):
            sball_x *= -1
            # sball_x += round(random.uniform(-0.1, 0.1), 2)
            # print(sball_x)
        if ball.colliderect(player2):
            sball_x *= -1
            # sball_x += round(random.uniform(-0.1, 0.1), 2)
            # print(sball_x)

            

        screen.fill((0,0,0))
        screen.blit(score1_screen_obj, score1_rect_obj)
        screen.blit(score2_screen_obj, score2_rect_obj)
        if done == True:
            screen.blit(winner_screen_obj, winner_rect_obj)
        pygame.draw.rect(screen, (255, 255, 255), player1)
        pygame.draw.rect(screen, (255, 255, 255), player2)
        if not done:
            pygame.draw.ellipse(screen, (255, 255, 255), ball)
            pygame.draw.aaline(screen, (255, 255, 255), (800/2, 0), (800/2, 800))

        pygame.display.flip()
        clock.tick(320)


if __name__ == "__main__":
    main()