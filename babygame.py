#!/usr/bin/python
import pygame, sys, os
import random
from pygame.locals import *
import pygame.mixer
from time import time

pygame.init() 
 
window = pygame.display.set_mode((800, 600),FULLSCREEN,24) 
pygame.display.set_caption('Baby Game') 
screen = pygame.display.get_surface()
x = 0
y = 0
i = time()
media_sub=""
image_file_name = os.path.join("media","babygame.gif")
music_file = ""
voice_file = ""
old_keypress = "none"
old_voice = "none"
old_music = "none"

def input(events):
    "Get the keypress from the user"
    global media_sub

    for event in events:
        if event.type == QUIT:
            pygame.mixer.music.stop()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit(0)
            if (event.key > 47 and event.key < 58) \
               or (event.key > 64 and event.key < 91) \
               or (event.key > 96 and event.key < 123):
                # convert the ASCII key to a character
                media_sub = chr(event.key)

while True:
    old_keypress = media_sub
    input(pygame.event.get())
    if not os.path.exists(os.path.join("media",media_sub)):
        media_sub = ""
    if old_keypress != media_sub:
        for file in os.listdir(os.path.join("media",media_sub)):
            if file.endswith(".wav"):
                voice_file = os.path.join("media",media_sub,file)
                pygame.mixer.music.load( voice_file )
                pygame.mixer.music.play(0, 0.0)
                old_voice = voice_file
        for file in os.listdir(os.path.join("media",media_sub)):
            if file.endswith(".mp3"):
                music_file = os.path.join("media",media_sub,file)
                pygame.mixer.music.queue( music_file )
                old_music = music_file
        i = time() - 2.0
    if (time() - i) > 1.5:
        r = random.randrange(128,256)
        g = random.randrange(128,256)
        b = random.randrange(128,256)
        screen.fill((r,g,b))
        i = time()
        for file in os.listdir(os.path.join("media",media_sub)):
            if file.endswith(".gif"):
                x = random.randrange(10,791)
                y = random.randrange(10,591)
                image_file_name = os.path.join("media",media_sub,file)
                image_surface = pygame.image.load(image_file_name)
                if x + image_surface.get_width() > 800:
                    x = 800 - x
                if y + image_surface.get_height() > 600:
                    y = 600 - y
                screen.blit(image_surface, (x,y))
    font = pygame.font.SysFont("Arial Black", 165
                                   )
    text = font.render(media_sub.upper(), 1, (0, 0, 0))
    textpos = text.get_rect(centerx=screen.get_width()/2
                            ,centery=screen.get_height()/2)
    screen.blit(text, textpos)
    pygame.display.flip()
