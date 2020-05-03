import pygame
import random
import numpy
from scipy.spatial import distance
from tensorflow import keras

M,N,grid_size=40,30,20
grids=[(i,j) for i in range(M) for j in range(N)]
Actions=['Top','Right','Bottum','Left']
Episode,High_score,snake_wait_time= 1,0,0
Train_data,Train_label=[[1,0,0,0,20,10,1,4]],[0]
model=  keras.Sequential([
                keras.layers.Flatten(input_shape=(8,1)),
                keras.layers.Dense(32,activation='relu'),
                keras.layers.Dense(4,activation='softmax')
                ])
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
def food():
    global Food
    snake_no_grids= [i for i in grids if i not in Snake]
    Food = random.choice(snake_no_grids)
def display():
    pygame.draw.rect(screen,(0,0,0), (0,0,M*grid_size,N*grid_size))
    for i in Snake:
        pygame.draw.rect(screen,(255,255,255), (i[0]*grid_size,i[1]*grid_size,grid_size,grid_size),1)
    pygame.draw.rect(screen,(255,255,255), (Food[0]*grid_size,Food[1]*grid_size,grid_size,grid_size))
    pygame.display.update()
def update_snake():
    global snake_tail,snake_head,snake_body,right_label
    (x,y)=Snake[0]
    if action == 'Right' :
        Snake.insert(0,(x+1,y))
    elif action == 'Left' :
        Snake.insert(0,(x-1,y))
    elif action == 'Top' :
        Snake.insert(0,(x,y-1))
    elif action == 'Bottum' :
        Snake.insert(0,(x,y+1))
    snake_tail=Snake.pop()
    snake_head=Snake[0]
    snake_body=Snake[1:len(Snake)]
    display()
def prediction():
    global action
    (x,y)=Snake[0]
    r=(x+1,y)
    l=(x-1,y)
    t=(x,y-1)
    b=(x,y+1)
    block=[0 if (i not in grids or i in Snake) else 1 for i in [t,r,b,l]]
    dist=[distance.euclidean(i, Food) for i in [t,r,b,l]]
    predict=model.predict(numpy.reshape(block+dist,(1,8,1)))
    action=Actions[numpy.argmax(predict[0])]
    op=[dist[i] if block[i]==1 else 100 for i in range(4)]
    Train_label.append(op.index(min(op)))
    Train_data.append(block+dist)

mloop=True
while mloop:
    pygame.init()
    screen = pygame.display.set_mode((M*grid_size,N*grid_size))
    Snake=[random.choice(grids)]
    food()
    model.fit(numpy.reshape(Train_data,(len(Train_data),8,1)),numpy.array(Train_label),epochs=4)
    loop=True
    while loop:
        pygame.time.wait(snake_wait_time)
        prediction()
        update_snake()
        if snake_head==Food:
            food()
            Snake.append(snake_tail)
        elif snake_head not in grids or snake_head in snake_body:
            score=len(Snake)-1
            if score > High_score:
                High_score=score
            print('Episodes :',Episode,', High_score :',High_score,', Score :',score)
            Episode+=1
            loop=False
        ev=pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                loop=False
                mloop=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop=False
                elif event.key == pygame.K_DOWN:
                    snake_wait_time+=25
                    print(snake_wait_time)
                elif event.key == pygame.K_UP:
                    if snake_wait_time>=25:
                        snake_wait_time-=25
                        print(snake_wait_time)
