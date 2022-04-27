'''
This game is a hangman game made by Nicolas Tabet

Variables: 
error_counts: it will count the error and increase at each error
shown_word = '' : it is the world that will not appear on the screen and will stay in the code written in letters
hidden_word : is the word which is not in letters but will appear on the screen in - - - - - - which will be created by a for loop form the shown_word
gameLost become True if we lose and will make appear the message on the screen from the redraw_window()
gameWon become  ""   "" "" win "" "" """ "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" """" "" ""
input_letter = None because it should be created at the beginning and is the letter that is inputted by the user

Functions:
main(): is the main game function
redraw_window() is to redraw everything on the window
hideWord(word) is to hide the word which will be shown word and transform it into hidden word
listToString(string) will convert a string to a list
stringToList(lst) willl convert a list to a string
get_input(x,y) will take the position of the mouse, look at which button is it and will take the chr(index 5) of this button (onlyy wheb we click on the mouse)

main_menu() opens the main menu if we ckick on it with the mouse it calls main

Buttons:
each buton is a list of 5 index ([color, x_pos, y_pos, radius, visible, char])
in a for loop of range(26) it will create a new one where the x pos will increase and the index[5] will be  65 + i so we will print out chr(index[5])
chr(65) = a 66 b ...
to get info we used the get_input()
'''
import pygame
import random
import os 

from random_word import RandomWords

pygame.init()
r = RandomWords()

WIDTH, HEIGHT = 900, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Nicolas Tabet")


#colors
RED = (255,0,0)
GREEN = (0,175,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_BLUE = (152,226,251)
LIGHT_GREEN = (153, 255, 204)

#images load
HANGMAN = [pygame.image.load(os.path.join("images", "hangman0.png")), pygame.image.load(os.path.join("images", "hangman1.png")), pygame.image.load(os.path.join("images", "hangman2.png")), pygame.image.load(os.path.join("images", "hangman3.png")), pygame.image.load(os.path.join("images", "hangman4.png")), pygame.image.load(os.path.join("images", "hangman5.png")), pygame.image.load(os.path.join("images", "hangman6.png"))]

#fonts
endgame_font = pygame.font.SysFont('comicsans', 60)
main_font = pygame.font.SysFont('comicsans', 50)
word_font = pygame.font.SysFont('comicsans', 100)

#hangman position
X_HANGMAN = WIDTH/2 - 85
Y_HANGMAN = HEIGHT/2 - 65

def stringToList(string):
	stringslist = list(string)
	string = stringslist
	return string

def listToString(lst):
	lst = ''.join(lst)
	return lst

def hideWord(word):
		shownWord = ''
		for i in word:
			shownWord += "-"
		return shownWord

def main():
	error_count = 0

	FPS = 60
	clock = pygame.time.Clock()

	hidden_word = r.get_random_word().upper()
	while '-' in hidden_word:
		hidden_word = r.get_random_word().upper()

	shown_word = ''
	input_letter = None

	buttons = []
	radius_button = 25

	# Setup buttons
	division = round(WIDTH / 13) #13 because we will divide by 13 letters for each column
	for i in range(26):
		if i < 13:
			y = 85
			x = 25 + (division * i)
		else:
			x = 25 + (division * (i - 13))
			y = 150

		buttons.append([LIGHT_GREEN, x, y, radius_button, True, 65 + i])
		# buttons.append([color, x_pos, y_pos, radius, visible, char])

	run =  True
	gameLost = False
	gameWon = False
	def redraw_window():
		WIN.fill(LIGHT_BLUE)

		if error_count <= 6:
			WIN.blit(HANGMAN[error_count], (X_HANGMAN, Y_HANGMAN))

		# Buttons
		for i in range(len(buttons)):
			if buttons[i][4]:
				pygame.draw.circle(WIN, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3]) #a bigger circle for the contour of the circle
				pygame.draw.circle(WIN, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)#the button inside the circle
				label = main_font.render(chr(buttons[i][5]), 1, BLACK)
				WIN.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))


		#remaining chances on the top right corner
		chances_label = main_font.render(f"remaining lives {6 - error_count}", 1, WHITE)
		WIN.blit(chances_label, (450, 0))
		
		#print the hidden word
		word_label = word_font.render(f"{shown_word}", 1, WHITE)
		WIN.blit(word_label, (WIDTH/2 - word_label.get_width()/2, 600))

		if gameLost:
			lostgame_label = endgame_font.render("You lost!!", 1, RED)
			WIN.blit(lostgame_label, (WIDTH/2 - lostgame_label.get_width()/2, 400))

		if gameWon:
			wongame_label = endgame_font.render("Nice you won!!", 1, GREEN)
			WIN.blit(wongame_label, (WIDTH/2 - wongame_label.get_width()/2, 400))

		pygame.display.update()

	def get_input(x, y):
		for i in range(len(buttons)):
			if buttons[i][1] - radius_button < x < buttons[i][1] + radius_button:
				if buttons[i][2] - radius_button < y < buttons[i][2] + 20:
					return chr(buttons[i][5])

	shown_word = hideWord(hidden_word)
	print(f"DEBUG: {hidden_word}")
	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				input_letter = get_input(mouse_pos[0], mouse_pos[1])

		if error_count >= 6:
			gameLost = True
			redraw_window()
			run = False

		if not ("-" in shown_word):
			gameWon = True
			redraw_window()
			run = False


		while input_letter != None:
			if hidden_word.count(input_letter) == 1 :
				hidden_word = stringToList(hidden_word)
				for i in hidden_word:
					if i == input_letter:
						indexx = hidden_word.index(i)
						shown_word = stringToList(shown_word)
						shown_word[indexx] = input_letter
						shown_word = listToString(shown_word)

				input_letter = None

			elif hidden_word.count(input_letter) > 1:
				hidden_word = stringToList(hidden_word)
				for indexx,letter in enumerate(hidden_word):
					if letter == input_letter:
						shown_word = stringToList(shown_word)
						shown_word[indexx] = input_letter
						shown_word = listToString(shown_word)

				input_letter = None
			else:
				error_count += 1
				input_letter = None


		redraw_window()


def main_menu():
	title_font = pygame.font.SysFont('comicsans', 70)
	run = True
	while run:
		WIN.fill(LIGHT_BLUE)
		title_label = title_font.render("Press the mouse to begin...",1, (255,255,255))
		WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
		pygame.display.update()
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					main()


main_menu()
quit()
	
	
	