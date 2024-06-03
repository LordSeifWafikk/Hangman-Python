import random
import os
import linecache
import turtle
gameTitle = "Hangman "
window = turtle.Screen()
window.title(gameTitle)

#Creating the man
man = turtle.Turtle()
man.width(10)
man.hideturtle()
man.color("darkgreen")
man.penup() 
noose = turtle.Turtle()
noose.width(10)
noose.hideturtle()
noose.color("black")
noose.penup()

def drawNoose():
    noose.penup()
    noose.goto(-200,-200)
    noose.pendown()
    noose.goto(200,-200)
    noose.goto(150,-200)
    noose.goto(100,-150)
    noose.goto(50,-200)
    noose.penup()
    noose.goto(100,-200)
    noose.pendown()
    noose.goto(100,200)
    noose.goto(0,200)
    noose.penup()
    noose.goto(0,200)
    noose.pendown()
    noose.goto(0,150)
    noose.penup()    
    window.update()
    man = turtle.Turtle()
    man.hideturtle()
# Drawing HANGMAN

def newLimb(limbs):
    
    if limbs <= 4: #Draw rope

        man.goto(0,100)#head
        man.pendown()
        man.circle(25)
        man.penup()        


    if limbs <= 3: #Draw body
        man.goto(0,100)
        man.pendown()
        man.goto(0,25)
        man.penup()
        man.goto(0,25)
        man.pendown()
        man.goto(-30,-40)
        man.penup()        
    

    if limbs <= 2: #Draw right leg
        man.goto(0,25)
        man.pendown()
        man.goto(30,-40)
        man.penup()

    if limbs <= 1: #Draw left arm
        man.goto(0,75)
        man.pendown()
        man.goto(-30,15)
        man.penup()

    if limbs <= 0: 
        #Draw right arm
        man.goto(0,75)
        man.pendown()
        man.goto(30,15)
        man.penup()


def start_game():
  # Print a welcome message
  print("Welcome to Hangman!")
                 


  # Get the player's name
  name = input("enter your name:")

  # Check if the player has a saved game
  if name + ".txt" in os.listdir():
    # Ask the player if they want to start a new game or continue a previous one
    print("A saved game was found for player {}. Would you like to start a new game or continue the previous one?".format(name))
    print('1. Resume')
    print('2. New')
    choice = input()
    
    if choice.lower() == "1":
      # Load the game state from the file
      load_game_state(name )

      # Start the game with the loaded data
      
    elif choice.lower() == "2":
      play_game(name ,word=None, correct_letters=None)
      return name
  else:
    # Create a new file for the player's saved game
    with open(name + ".txt", "w") as f:
      f.write("")
    play_game(name ,word=None, correct_letters=None)
    return name


def choose_word(word_file='hangman_words_sample.txt'):
  # Read the categories and words from the file and store them in a dictionary
  categories = {}
  with open("hangman_words_sample.txt", 'r') as f:
    lines = f.read().lower().splitlines()
  current_category = None
  for line in lines:
    if line.endswith(':'):
      current_category = line[0:-1]
      categories[current_category] = []
    elif line:  # Skip empty lines
      categories[current_category].append(line)

  # Sort the categories by the number of words in each category
  sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]))

  # Print the categories to the user and ask them to choose one
  print("Select a category:")
  for i, category in enumerate(sorted_categories):
    print(f"  {i+1}. {category[0]} ({len(category[1])} words)")
  choice = input()
  while int(choice) > len(sorted_categories):
    print("Please choose a correct category: ")
    choice = input()
  selected_category = sorted_categories[int(choice) - 1][0]

  # Choose a random word from the list of words in the selected category
  word = random.choice(categories[selected_category])

  return word


def play_game( name , word=None, correct_letters=None, used_letters=None, num_guesses=None):

  while True:

    game_won = False
    if word is None:
      # Choose a word
      word = choose_word()
      word_letters = set(word)
      correct_letters=set()
      used_letters=set()
    else:
       for letter in used_letters:
        if letter in word and letter != " ":
          word = word.replace(letter, "")
          

    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    
    used_words = set()
    if num_guesses is None:
      num_guesses=5
    

    # Set up the game loop

    while num_guesses > 0:


        drawNoose()
        newLimb(num_guesses)
                    
        
        # Print the current state of the game
        print('You have {} guesses left'.format(num_guesses))
        print('Used letters:', ' '.join(used_letters))
        print('Word:', ' '.join([x if x in used_letters else '_' for x in word]))

        # Get the player's next guess
        guess = input('Enter your next guess or enter "-1" to pause: ').lower()
        if guess == "-1":
          pause(name ,word, correct_letters,used_letters , num_guesses)
          return name , word ,correct_letters , used_letters ,num_guesses
        # Check if the guess is valid
        if guess in alphabet - used_letters:
            used_letters.add(guess)
            if guess in word_letters:
                print('Correct!')
                correct_letters.add(guess)
                word_letters -= set(guess)
                if not word_letters:
                    print('Congratulations! You won!')
                    game_won = True
                    break
            else:
                print('Incorrect!')
                num_guesses -= 1
        elif guess in used_letters:
            print('You already used that letter')
        elif len(guess) == len(word) and guess not in used_words:
            used_words.add(guess)
            if guess == word:
                save_game_state(name , word, correct_letters, used_letters,num_guesses, newLimb)
                print('Congratulations! You won!')
                game_won = True
                break
            else:
                print('Incorrect!')
                num_guesses -= 1
        else:
            print('Invalid input')
      
        
    # The player has run out of guesses
    if not game_won:
        man.goto(0,75)
        man.pendown()
        man.goto(30,15)
        man.penup()
      
        print('You lost! The word was', word)
    
    # Prompt the user if they want to play again
    play_again = input('Do you want to play again? (y/n) ').lower()
    if play_again == 'y':
        
      play_again
      print("Hero, now we'll give u another word")
      drawNoose()
      man.clear()
      # Reset the game variables for the next game
      play_game( name , word=None, correct_letters=None, used_letters=None, num_guesses=None)
      
      continue
    else:
      exit()
  



def save_game_state(name , word, correct_letters, used_letters,num_guesses, newLimb):#seif wafikk basha  
  # Save the game state to a file
  

  with open(name+".txt", "w") as f:
    f.write(word+'\n')
    f.write(str(correct_letters)+'\n')
    f.write(str(used_letters)+'\n')
    f.write(str(num_guesses))
    f.close()


def load_game_state(filename): #seif wafik basha bardo
  if not filename:
    print("Error: No filename provided.")
    return

  try:
    #checking if there is a folder with the player name but there is no saved data(statred the game but didn't save it)
    if os.stat(filename+'.txt').st_size == 0: 
      print('No data saved for {}'.format(filename))
      play_game( filename , word=None, correct_letters=None, used_letters=None, num_guesses=None)
    else:
        # Split the data into the word , the correct letters ,used letters, num of guesses  
      with open(filename+'.txt', 'r') as f:
        word = linecache.getline(filename+'.txt', 1).rstrip()
        num_guesses=int(linecache.getline(filename+'.txt', 4).rstrip())
        correct_letters=[]
        used_letters=[]
        alpha = list("abcdefghijklmnopqrstuvwxyz")
        if linecache.getline(filename+'.txt', 3).rstrip()=='set()':
          #if the user started a game and didn't give an input and saved the game 
          used_letters=set()
          correct_letters=set()
          play_game( filename , word, correct_letters,used_letters,num_guesses, newLimb)
        else:
        
          for char in linecache.getline(filename+'.txt', 3).rstrip():  
            if char in alpha:
              used_letters.append(char)
      
          for char in linecache.getline(filename +'.txt', 2).rstrip(): 
            if char in alpha:
              correct_letters.append(char)
      
      
      
          used_letters=set(used_letters)
          correct_letters=set(correct_letters)
        
          play_game(filename ,word,correct_letters,used_letters,num_guesses)


  except FileNotFoundError:
    print("Error: File not found.")
    return



def pause(name,word, correct_letters,used_letters,num_guesses):
  # Ask the player if they want to pause and save, continue, or exit
  print("1. Save and exit ")
  print("2. Continue ")
  print("3. Exit without saving")
  choice = input()
  if choice.lower() == "1":
    save_game_state(name,word, correct_letters,used_letters,num_guesses, newLimb)
    print("Your game has been saved. See you soon!")
    exit()
    
  elif choice.lower() == "2":
    play_game(name, word, correct_letters,used_letters,num_guesses)
    return

      
  elif choice.lower() == "3":
      # Print a goodbye message and exit the program
      print("Thank you for playing Hangman! Goodbye.")
      exit()
      
  else:
      # Print an error message and return to the main menu
      print("Invalid input. Please try again.")
      return

# Start the game
start_game()
