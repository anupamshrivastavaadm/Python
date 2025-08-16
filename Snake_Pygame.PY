import pygame,sys,random

def game():
    pygame.init()
    w,h=540,900   # 9:16 screen ratio
    sc=pygame.display.set_mode((w,h))
    clk=pygame.time.Clock()
    f=30
    x,y=w//2,h//2;dx,dy=f,0
    snake=[(x,y)]
    food=(random.randrange(0,w,f),random.randrange(0,h,f))
    font=pygame.font.SysFont(None,36)
    score=0
    title=pygame.font.SysFont(None,48)

    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_UP and dy==0:dx,dy=0,-f
                if e.key==pygame.K_DOWN and dy==0:dx,dy=0,f
                if e.key==pygame.K_LEFT and dx==0:dx,dy=-f,0
                if e.key==pygame.K_RIGHT and dx==0:dx,dy=f,0

        x+=dx;y+=dy;snake.append((x,y))
        if (x,y)==food:
            food=(random.randrange(0,w,f),random.randrange(0,h,f))
            score+=1
        else: snake.pop(0)

        # Collision check
        if x<0 or y<0 or x>=w or y>=h or len(snake)!=len(set(snake)): return score

        sc.fill((0,0,0))
        # Draw snake body
        for i in snake[:-1]:
            pygame.draw.rect(sc,(0,200,0),(i[0],i[1],f,f))
        # Draw snake head (different color)
        pygame.draw.rect(sc,(0,255,100),(snake[-1][0],snake[-1][1],f,f))
        # Draw food
        pygame.draw.rect(sc,(200,0,0),(food[0],food[1],f,f))
        # Draw title and score
        sc.blit(title.render("SNAKE GAME",1,(255,255,0)),(w//2-100,10))
        sc.blit(font.render(f"Score: {score}",1,(255,255,255)),(10,50))
        pygame.display.flip();clk.tick(12)

# --- Main loop with restart/quit menu ---
while True:
    score=game()
    sc=pygame.display.set_mode((540,960))
    font=pygame.font.SysFont(None,48)
    sc.fill((0,0,0))
    sc.blit(font.render("GAME OVER!",1,(255,0,0)),(150,400))
    sc.blit(font.render(f"Final Score: {score}",1,(200,200,200)),(130,460))
    sc.blit(font.render("R = Restart",1,(200,200,200)),(150,520))
    sc.blit(font.render("Q = Quit",1,(200,200,200)),(170,580))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_q:pygame.quit();sys.exit()
                if e.key==pygame.K_r:break
        else: continue
        break
