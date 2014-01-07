#!/usr/bin/python
import pygame, sys, os
import random
from pygame.locals import *
import pygame.mixer
from time import time

def initialize_screen(fullscreen=False):
  print "Initializing pygame"
  pygame.init()
       
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

def get_input(events):
  "Get the keypress from the user"
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
        return keypress
  return None

def play_voice_file(keypress):
  "Play the voice file for the provided keypress"
  dirname = keypress
  filename = "%s.wav" % keypress
  voice_file = os.path.join("media", dirname, filename)
  print "voice_file = %s" % voice_file
  if os.path.exists(voice_file):
    pygame.mixer.music.load(voice_file)
    pygame.mixer.music.play(0, 0.0)

def get_image(keypress):
  "Get image for the keypress, or None if not available"
  if not keypress: return None

  media_dir = os.path.join("media",keypress)
  if not os.path.exists(media_dir): return None

  extensions = set([".gif", ".png", ".jpg", ".jpeg"])

  for filename in os.listdir(media_dir):
    root, ext = os.path.splitext(filename)
    if ext in extensions:
      image_file_name = os.path.join("media", keypress, filename)
      image = pygame.image.load(image_file_name)
      return image

  return None      


def random_color():
  "Get a random color"
  r = random.randrange(128,256)
  g = random.randrange(128,256)
  b = random.randrange(128,256)
  return (r,g,b)



def main(fullscreen=False):

  # Initialization
  screen = initialize_screen(fullscreen)

  keypress = None
  last_keypress = None
  last_update_time = time()
  image = None
  update = True
  update_period = .75

  # Main program loop
  while True:
    keypress = get_input(pygame.event.get())

    if keypress and not os.path.exists(os.path.join("media",keypress)):
      keypress = None

    if keypress and last_keypress != keypress:
      play_voice_file(keypress)
      image = get_image(keypress)
      update = True
      last_keypress = keypress

    update = update or time() - last_update_time > update_period

    if update:
      update = False
      last_update_time = time()

      screen.fill(random_color())

      if image and screen.get_rect().contains(image.get_rect()):
        x = random.randrange(0, screen.get_width() - image.get_width())
        y = random.randrange(0, screen.get_height() - image.get_height())
        screen.blit(image, (x,y))

    # Render
    if last_keypress:
      font = pygame.font.SysFont("Arial Black", 265)
      
      antialias = True
      text_color = (0, 0, 0)
      text = font.render(last_keypress.upper(), antialias, text_color)

      textpos = text.get_rect(
        centerx=screen.get_width() / 2,
        centery=screen.get_height() / 2)

      screen.blit(text, textpos)

    pygame.display.flip()


if __name__ == "__main__":
  
  fullscreen = False
  
  for arg in sys.argv:
    if arg == "-f" or arg == "--fullscreen":
      fullscreen = True

  main(fullscreen)
