#!/usr/bin/python
import pygame, sys, os
import random
from pygame.locals import *
import pygame.mixer
from time import time


def initialize_screen(fullscreen=False):
  print "Initializing pygame"
  pygame.init()
   
  fullscreen = False
    
  if fullscreen:
      depth = 0
      flags = FULLSCREEN | HWSURFACE | DOUBLEBUF
  else:
      depth = 16
      flags = SWSURFACE | DOUBLEBUF
  modes = pygame.display.list_modes(depth, flags)

  if fullscreen:
      if modes == -1:  # Welcome to exceptionlessland
          raise SystemExit("Failed to initialize display")
      else:
          mode = max(modes)
  else:
      mode = (800, 600)

  pygame.display.set_mode(mode, flags, depth)

  pygame.display.set_caption('Baby Game') 
  screen = pygame.display.get_surface()
  return screen


screen = initialize_screen(False)

x = 0
y = 0
i = time()
keypress=""
image_file_name = os.path.join("media","babygame.gif")
music_file = ""
voice_file = ""
old_keypress = "none"
old_voice = "none"
old_music = "none"

def input(events):
  "Get the keypress from the user"
  global keypress

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
        print "Event.key = " + str(event.key)
        keypress = chr(event.key)
        print "keypress = " + str(keypress)

def locate_media(keypress):
  dirname = keypress
  filename = "%s.wav" % keypress
  return os.path.join("media", dirname, filename)

while True:
  old_keypress = keypress

  input(pygame.event.get())

  if not os.path.exists(os.path.join("media",keypress)):
    keypress = ""

  if old_keypress != keypress:
    voice_file = locate_media(keypress)
    print "voice_file = %s" % voice_file
    pygame.mixer.music.load(voice_file)
    pygame.mixer.music.play(0, 0.0)
    old_voice = voice_file
    i = time() - 2.0

  if (time() - i) > 1.5:
    r = random.randrange(128,256)
    g = random.randrange(128,256)
    b = random.randrange(128,256)
    screen.fill((r,g,b))
    i = time()
    for file in os.listdir(os.path.join("media",keypress)):
      if file.endswith(".gif"):
        x = random.randrange(10,791)
        y = random.randrange(10,591)
        image_file_name = os.path.join("media",keypress,file)
        image_surface = pygame.image.load(image_file_name)
        if x + image_surface.get_width() > 800:
          x = 800 - x
        if y + image_surface.get_height() > 600:
          y = 600 - y
        screen.blit(image_surface, (x,y))

  # Render
  font = pygame.font.SysFont("Arial Black", 165)
  
  text_color = (0, 0, 0)
  #text = font.render(keypress.upper(), 1, text_color)
  antialias = True
  text = font.render(keypress.upper(), antialias, text_color)

  textpos = text.get_rect(centerx=screen.get_width()/2
                          ,centery=screen.get_height()/2)
  screen.blit(text, textpos)
  pygame.display.flip()
