import random,time,math
import wgtk_wall,wgtk_enemy
WIDTH=1200 #480
HEIGHT=660  #680

begin=False
gameover=False
win=False
background=Actor("wgtk/background",topleft=(0,0))
background2=[]
for i in range(20):
    for j in range(11):
        bg=Actor("wgtk/background2",topleft=(i*60,j*60))
        bg.i=i
        bg.j=j
        background2.append(bg)

walls=[]
for a in range(len(wgtk_wall.walls_pos)):
    print(wgtk_wall.walls_pos[a][0])
    wall=Actor("wgtk/wall",topleft=(wgtk_wall.walls_pos[a][0]*60,wgtk_wall.walls_pos[a][1]*60))
    walls.append(wall)

tank_enemies=[]
for a in range(len(wgtk_enemy.enemies_pos)):
    print(wgtk_enemy.enemies_pos[a][0])
    tank_enemy=Actor("wgtk/tank_enemy",topleft=(wgtk_enemy.enemies_pos[a][0]*60,wgtk_enemy.enemies_pos[a][1]*60))
    tank_enemies.append(tank_enemy)



def update():
    global begin
    if not begin:
        if keyboard.a:
            begin=True
        return
    if win:
        return
    if gameover:
        return



def draw():
    if not begin:
        screen.blit("warplanes_zt",(10,10))
        screen.draw.text("pass a to begin",center=(WIDTH//2,HEIGHT//2),fontsize=45,color="red")
        return
    if gameover:
        #screen.blit("warplanes_gameover",(WIDTH/2,HEIGHT/2))
        screen.draw.text("gameover",center=(WIDTH//2,HEIGHT//2),fontsize=45,color="red")
        return
    background.draw()
    for bg in background2:
        bg.draw()
        screen.draw.text(str(bg.i)+","+str(bg.j),center=(30+60*bg.i,30+60*bg.j),fontsize=20,color="red")
    for wall in walls:
        wall.draw()
    for tank_enemy in tank_enemies:
        tank_enemy.draw()
    draw_live()


def draw_live():
    screen.draw.text("your live:",topleft=(20,20),
                    #fontname="marker_felt",
                    fontsize=25)
    screen.draw.text("remain enemies:",topleft=(20,40),
                    #fontname="marker_felt",
                    fontsize=25)