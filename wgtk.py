import random,time,math
import wgtk_self,wgtk_wall,wgtk_enemy
WIDTH=1200 #480
HEIGHT=660  #680
begin=False
gameover=False
win=False
#background=Actor("wgtk/background",topleft=(0,0))
background2=[]
for i in range(20):
    for j in range(11):
        bg=Actor("wgtk/background2",topleft=(i*60,j*60))
        bg.i=i
        bg.j=j
        background2.append(bg)
tank_self=Actor("wgtk/tank_self",topleft=(wgtk_self.self_pos[0]*60,wgtk_self.self_pos[1]*60))
tank_self_tang=Actor("wgtk/tank_self_tang",center=(tank_self.x,tank_self.y))
tank_self.live=4
tank_self.speed=2

bullets=[]
tank_enemies=[]
boom_imgs=[]
tracks=[]


walls=[]
for a in range(len(wgtk_wall.walls_pos)):
    #print(wgtk_wall.walls_pos[a][0])
    wall=Actor("wgtk/wall",topleft=(wgtk_wall.walls_pos[a][0]*60,wgtk_wall.walls_pos[a][1]*60))
    walls.append(wall)


tank_enemies=[]
for a in range(len(wgtk_enemy.enemies_pos)):
    #print(wgtk_enemy.enemies_pos[a][0])
    tank_enemy=Actor("wgtk/tank_enemy",topleft=(wgtk_enemy.enemies_pos[a][0]*60,wgtk_enemy.enemies_pos[a][1]*60))
    track=Actor("wgtk/track",center=((tank_enemy.x+tank_self.x)/2,(tank_enemy.y+tank_self.y)/2))
    track.angle=track.angle_to(tank_self)
    tracks.append(track)
    tank_enemy.a=track
    tank_enemy.r=20
    tank_enemy.m_d=wgtk_enemy.m_d
    tank_enemy.speed=30
    tank_enemy.m=1
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
    update_tank_self()
    update_bullets()
    update_tank_enemy()
    updata_boom_img()
        



def draw():
    if not begin:
        screen.blit("wgtk/begin",(10,10))
        screen.draw.text("pass 'A' to begin",center=(WIDTH//2,HEIGHT//2),fontsize=60,color="yellow")
        return
    #background.draw()
    for bg in background2:
        bg.draw()
        #screen.draw.text(str(bg.i)+","+str(bg.j),center=(30+60*bg.i,30+60*bg.j),fontsize=20,color="red")
    tank_self.draw()
    tank_self_tang.draw()
    #screen.fill((255, 255, 255))
    for tank_enemy in tank_enemies:
        tank_enemy.draw()
        #tank_enemy.a.draw()
    for bullet in bullets:
        bullet.draw()
    for boom_img in boom_imgs:
        boom_img.draw()
    for wall in walls:
        wall.draw()
    draw_live()
    if gameover:
        #screen.blit("warplanes_gameover",(WIDTH/2,HEIGHT/2))
        screen.draw.text("gameover",center=(WIDTH//2,HEIGHT//2),fontsize=50,color="red")
        return
    if win:
        screen.draw.text("you win",center=(WIDTH//2,HEIGHT//2),fontsize=60,color="yellow")
        return


def draw_live():
    screen.draw.text("your live:"+str(tank_self.live),topleft=(20,20),
                    #fontname="marker_felt",
                    fontsize=25)
    screen.draw.text("remain enemies:"+str(len(tank_enemies)),topleft=(20,40),
                    #fontname="marker_felt",
                    fontsize=25)

def on_mouse_move(pos):
    tank_self_tang.angle = tank_self.angle_to(pos)


def on_mouse_down(button,pos):
    #print("Mouse button", button, "clicked")
    if button == mouse.LEFT:
        #print("+++++++++++++++++++")
        clock.schedule_unique(shoot_self,0.15)
    if button == mouse.RIGHT:
        #print(tank_self.pos)
        '''
        for tank_enemy in tank_enemies:
            tank_enemy.angle = tank_enemy.angle_to(tank_self.pos)
            r2=tank_enemy.a.collidelist(walls)
            if r2!=-1:
                print("dis1="+str(tank_enemy.distance_to(walls[r2])))
                print("dis2="+str(tank_enemy.distance_to(tank_self)))
                print("ang1="+str(tank_enemy.angle_to(walls[r2])))
                print("ang2="+str(tank_enemy.angle_to(tank_self)))
        '''



def update_tank_self():
    move_tank_self()
    r=tank_self.collidelist(bullets)
    if r!=-1:
        create_boom_img(tank_self.x,tank_self.y)
        islive()
        bullets.remove(bullets[r])
def islive():
    global gameover
    tank_self.live-=1;
    if tank_self.live<=0:
        gameover=True
        time.sleep(0.5)


def move_tank_self():
    #global bullet_n
    #global bulletself
    old_x=tank_self.x
    old_y=tank_self.y


    if keyboard.right or keyboard.d:
        tank_self.x+=tank_self.speed
    r=tank_self.collidelist(walls)
    if r!=-1:
        tank_self.x=old_x
        tank_self.y=old_y
    else:
        old_x=tank_self.x
        old_y=tank_self.y


    if keyboard.left or keyboard.a:
        tank_self.x-=tank_self.speed
    r=tank_self.collidelist(walls)
    if r!=-1:
        tank_self.x=old_x
        tank_self.y=old_y
    else:
        old_x=tank_self.x
        old_y=tank_self.y

    if keyboard.down or keyboard.s:
        tank_self.y+=tank_self.speed
    r=tank_self.collidelist(walls)
    if r!=-1:
        tank_self.x=old_x
        tank_self.y=old_y
    else:
        old_x=tank_self.x
        old_y=tank_self.y

    if keyboard.up or keyboard.w:
        tank_self.y-=tank_self.speed
    r=tank_self.collidelist(walls)
    if r!=-1:
        tank_self.x=old_x
        tank_self.y=old_y
    #if keyboard.space:
    #    clock.schedule_unique(shoot_self,0.1)
    if tank_self.left<0:
        tank_self.left=0
    if tank_self.right>WIDTH:
        tank_self.right=WIDTH
    if tank_self.top<0:
        tank_self.top=0
    if tank_self.bottom>HEIGHT:
        tank_self.bottom=HEIGHT
    tank_self_tang.center=(tank_self.x,tank_self.y)




def move_tank_enemy_move(a_enemy,angle):
    theta=math.radians(angle)
    old_x=a_enemy.x
    old_y=a_enemy.y
    a_enemy.x+=a_enemy.speed*math.cos(theta)
    a_enemy.y-=a_enemy.speed*math.sin(theta)
    r=a_enemy.collidelist(walls)
    if r!=-1:
        a_enemy.x=old_x
        a_enemy.y=old_y

    if a_enemy.left<0:
        a_enemy.left=0
    if a_enemy.right>WIDTH:
        a_enemy.right=WIDTH
    if a_enemy.top<0:
        a_enemy.top=0
    if a_enemy.bottom>HEIGHT:
        a_enemy.bottom=HEIGHT

def shoot_self():
    #sounds.bullet.play()
    #global bullet_n
    #print(str(bullet_n)+"+++++++++++++++++++")
    theta_temp=math.radians(tank_self_tang.angle)
    bullet_x=tank_self.x+math.cos(theta_temp)*60
    bullet_y=tank_self.y-math.sin(theta_temp)*60
    #print(str(theta_temp)+"++")
    bullet=Actor("wgtk/bullet",midbottom=(bullet_x,bullet_y))
    bullet.speed=8
    bullet.live=1
    bullet.angle=tank_self_tang.angle
    bullet.theta=math.radians(bullet.angle)
    bullets.append(bullet)




def shoot_enemy(angle,x,y):
    #sounds.bullet.play()
    #global bullet_n
    #print(str(bullet_n)+"+++++++++++++++++++")
    theta_temp=math.radians(angle)
    bullet_x=x+math.cos(theta_temp)*80
    bullet_y=y-math.sin(theta_temp)*80
    #print(str(theta_temp)+"++")
    bullet=Actor("wgtk/bullet",midbottom=(bullet_x,bullet_y))
    bullet.speed=8
    bullet.live=1
    bullet.angle=angle
    bullet.theta=math.radians(bullet.angle)
    bullets.append(bullet)

def shoot_enemy2(a_enemy):
    

    theta2=math.atan((a_enemy.x-tank_self.x)/(a_enemy.y+tank_self.y))
    #print("theta2="+str(theta2))
    theta=theta2+math.pi/2

    a_enemy.angle=math.degrees(theta)


    bullet_x=a_enemy.x+math.cos(theta)*80
    bullet_y=a_enemy.y-math.sin(theta)*80
    bullet=Actor("wgtk/bullet",midbottom=(bullet_x,bullet_y))
    bullet.speed=8
    bullet.live=1

    bullet.angle=math.degrees(theta)
    bullet.theta=theta
    bullets.append(bullet)



def update_bullets():
    for bullet in bullets:
       #bullet.theta=math.radians(bullet.angle)
        bullet.x+=bullet.speed*math.cos(bullet.theta)
        bullet.y-=bullet.speed*math.sin(bullet.theta)
        #print("++++++"+str(bullet.speed*math.cos(bullet.theta)))

        #collide 4 zhou
        if bullet.right > WIDTH or bullet.left<0:
            if bullet.live>0:
                bullet.theta=math.pi-bullet.theta
                bullet.live-=1
            else:
                bullets.remove(bullet)
                create_boom_img(bullet.x,bullet.y)
                continue
        if bullet.bottom > HEIGHT or bullet.top<0:
            if bullet.live>0:
                bullet.theta=2*math.pi-bullet.theta
                bullet.live-=1
            else:
                bullets.remove(bullet)
                create_boom_img(bullet.x,bullet.y)
                continue

        #collide wall
        r=bullet.collidelist(walls)
        if r!=-1:
            #
            if walls[r].left<bullet.x<walls[r].right:
                if bullet.live>0:
                    bullet.theta=2*math.pi-bullet.theta
                    bullet.live-=1
                else:
                    bullets.remove(bullet)
                    create_boom_img(bullet.x,bullet.y)
                    continue
            else:
                if bullet.live>0:
                    bullet.theta=math.pi-bullet.theta
                    bullet.live-=1
                else:
                    bullets.remove(bullet)
                    create_boom_img(bullet.x,bullet.y)
                    continue

        #collide selives
        bullets.remove(bullet)
        r=bullet.collidelist(bullets)
        if r!=-1:
            create_boom_img(bullet.x,bullet.y)
            bullets.remove(bullets[r])
            #print("++")
            #print(bullet.pos)
            #print(bullets[r].pos)
            #print("++++")
        else:
            bullets.append(bullet)


def create_boom_img(x,y):
    boom_img=Actor("wgtk/boom",center=(x,y))
    boom_img.live=15
    boom_imgs.append(boom_img)


def update_tank_enemy():
    global win
    for tank_enemy in tank_enemies:
        #tank_enemy.angle = tank_enemy.angle_to(tank_self.pos)
        #update track
        tank_enemy.a.center=((tank_enemy.x+tank_self.x)/2,(tank_enemy.y+tank_self.y)/2)
        tank_enemy.a.angle=tank_enemy.angle_to(tank_self)

        #track work
        r2=tank_enemy.a.collidelist(walls)
        if not (r2!=-1 and tank_enemy.distance_to(walls[r2])<tank_enemy.distance_to(tank_self) and -90<tank_enemy.angle_to(walls[r2])-tank_enemy.angle_to(tank_self)<90):
                #print("dis1="+str(tank_enemy.distance_to(walls[r2])))
                #print("dis2="+str(tank_enemy.distance_to(tank_self)))
                #print("ang1="+str(tank_enemy.angle_to(walls[r2])))
                #print("ang2="+str(tank_enemy.angle_to(tank_self)))
                tank_enemy.angle = tank_enemy.angle_to(tank_self.pos)
                if tank_enemy.r<=0:
                    shoot_enemy(tank_enemy.angle,tank_enemy.x,tank_enemy.y)
                    tank_enemy.r=60
                else:
                    tank_enemy.r-=1
        else:
            if tank_enemy.r<=0:
                shoot_enemy2(tank_enemy)
                tank_enemy.r=70
            else:
                tank_enemy.r-=1

        #move
        for bullet in bullets:
            if tank_enemy.distance_to(bullet)<360 and -15<bullet.angle-bullet.angle_to(tank_enemy)<15:
                if tank_enemy.m==1:
                    move_tank_enemy_move(tank_enemy,bullet.angle+90*tank_enemy.m_d)
                    tank_enemy.m=2
                else:
                    tank_enemy.m=1

        #hurted
        r=tank_enemy.collidelist(bullets)
        if r!=-1:
            create_boom_img(tank_enemy.x,tank_enemy.y)
            tank_enemies.remove(tank_enemy)
            bullets.remove(bullets[r])



    if len(tank_enemies)==0:
        win=True
        return

#def update_tracks():
#    for track in tracks:
#        track.center=((tank_enemy.x+tank_self.x)/2,(tank_enemy.y+tank_self.y)/2)
#        track.angle=track.angle_to(tank_self)



#更新爆炸效果
def updata_boom_img():
    for boom_img in boom_imgs:
        boom_img.live-=1
        if boom_img.live==10:
            boom_img.image="wgtk/boom2"
        if boom_img.live==5:
            boom_img.image="wgtk/boom3"
        if boom_img.live<=0:
            boom_imgs.remove(boom_img)
