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


def play_file(filename):
  if os.path.exists(filename):
    try:
      pygame.mixer.music.load(filename)
      pygame.mixer.music.play(0, 0.0)
    except:
      print "Error playing %s" % filename


def play_voice_file(keypress):
  "Play the voice file for the provided keypress"
  dirname = keypress
  filename = "%s.wav" % keypress.upper()
  voice_file = os.path.join("media", dirname, filename)
  print "voice_file = %s" % voice_file
  if os.path.exists(voice_file):
    try:
      pygame.mixer.music.load(voice_file)
      pygame.mixer.music.play(0, 0.0)
    except:
      print "Error playing %s" % voice_file


def play_clap_file():
  play_file("media/clap.wav")


def get_image(keypress):
  "Get image for the keypress, or None if not available"
  if not keypress: return None

  media_dir = os.path.join("media",keypress)
  if not os.path.exists(media_dir): return None

  extensions = set([".gif", ".png", ".jpg", ".jpeg"])

  for filename in os.listdir(media_dir):
    root, ext = os.path.splitext(filename)
    if ext in extensions:
      word = filename.split(".")[0].upper()
      image_file_name = os.path.join("media", keypress, filename)
      image = pygame.image.load(image_file_name)
      width = image.get_width()
      height = image.get_height()
      desired_height = 256
      scale = 1.0 * desired_height / height
      new_width = int(scale * width)
      new_height = int(scale * height)
      image = pygame.transform.smoothscale(image, (new_width, new_height))
      return image, word

  return None, ""


def random_color():
  "Get a random color"
  r = random.randrange(128,256)
  g = random.randrange(128,256)
  b = random.randrange(128,256)
  return (r,g,b)


def random_word():
  words = ["LUCY", "BALL", "APPLE", "OUTSIDE", "UP", "SHOES", "DIAPER"]
  return words[random.randrange(0, len(words))]


# Main
def main(argv=[]):
  "Main entry point"

  # Parse command line args
  fullscreen = False
  for arg in sys.argv:
    if arg == "-f" or arg == "--fullscreen":
      fullscreen = True

  # Initialization
  screen = initialize_screen(fullscreen)

  keypress = None
  last_keypress = None
  last_update_time = time()
  image = None
  refresh = True
  update_period = 1.5 
  last_word = ""
  remaining_word = last_word
  letters_found = 0
  new_word_queued = False
  word_completed_time = time()
  current_letter_word = ""

  # Main program loop
  while True:
    keypress = get_input(pygame.event.get())

    if keypress:
      play_voice_file(keypress)
      image, word = get_image(keypress)
      refresh = True
      last_keypress = keypress
      #if remaining_word and keypress.upper() == remaining_word[0].upper():
      #  letters_found += 1
      #  remaining_word = last_word[letters_found:]
      print "Getting new word"
      last_word = word
      letters_found = 0
      remaining_word = last_word
      new_word_queued = False

    if refresh or time() - last_update_time > update_period:
      refresh = False
      last_update_time = time()

      #if not remaining_word and not new_word_queued:
      #  print "Completed word!!!"
      #  word_completed_time = time()
      #  new_word_queued = True
      #  play_clap_file()

      # Switch fill color and move sprites
      background_color = random_color()

      if image and screen.get_rect().contains(image.get_rect()):
        x = random.randrange(0, screen.get_width() - image.get_width())
        y = random.randrange(0, screen.get_height() - image.get_height())

    #if new_word_queued and time() - word_completed_time > 1:
    #  print "Getting new word"
    #  last_word = random_word()
    #  letters_found = 0
    #  remaining_word = last_word
    #  new_word_queued = False

    # Render
    screen.fill(background_color)

    # Render image
    if image:
      screen.blit(image, (x,y))

    # Text options
    antialias = True
    
    word_font = pygame.font.SysFont("Arial Black", 120)

    if letters_found > 0:
      completed_word_color = (64, 212, 64)
      completed_word_text = word_font.render(last_word[:letters_found], antialias, completed_word_color)
      completed_word_pos  = completed_word_text.get_rect(x=10, y=0)
      screen.blit(completed_word_text, completed_word_pos)
      cursor_x = completed_word_pos.x + completed_word_text.get_width()
      cursor_y = completed_word_pos.y
    else:
      cursor_x = 10
      cursor_y = 0

    if letters_found < len(last_word):
      current_letter_color = (0, 255, 255)
      current_letter_text = word_font.render(
        last_word[letters_found],
        antialias,
        current_letter_color)
      current_letter_pos  = current_letter_text.get_rect(x=cursor_x, y=cursor_y)
      screen.blit(current_letter_text, current_letter_pos)
      cursor_x = current_letter_pos.x + current_letter_text.get_width()
      cursor_y = current_letter_pos.y      

    word_color = (32, 32, 32)
    word_text = word_font.render(last_word[letters_found+1:], antialias, word_color)
    word_pos  = word_text.get_rect(x=cursor_x, y=cursor_y)
    screen.blit(word_text, word_pos)

    if last_keypress:
      letter_color = (0, 0, 0)
      letter_font = pygame.font.SysFont("Arial Black", 300)      
      letter_text = letter_font.render(last_keypress.upper(), antialias, letter_color)
      letter_pos  = letter_text.get_rect(
        centerx=screen.get_width() / 2,
        centery=screen.get_height() / 2)
      screen.blit(letter_text, letter_pos)

      #if time() - last_keypress_time > 3:
      #  last_keypress = None

    pygame.display.flip()


# Main entry point
if __name__ == "__main__":
  main(sys.argv)
