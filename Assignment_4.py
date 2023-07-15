#Luke Brennan
#11/18/19
#Assignment #4

# - Algorithm -
#The filename is asked for and entered and then opened
#the function construct() is entered which takes the file and turns it into a list (maze)
#if the list is blank an error message is sent, If there is an invalid character a different list is returned and error message is sent
#the function FindS() is triggered which returns the starting point of the maze and an error message is the maze is missing E or S
#if the starting position is valid then solve() is started which solves the maze
#the entire solve function is in a loop where X and Y are the vertical and horizontal positions and are difines by the list 'pos' at the beginning of the loop
#at each execution of the loop the positions in all directions are checked to see if the exist and bool values are assigned accordingly
#each if and elif afterwards checks all positions for blank space and if blank space is found it is replaced with the correct ascii arrow
#if no 'E' or blank space is found the backtrack function is started which grabs the nearest arrow, replaces it with '.' and moves the position back one
#if no blank space is found after backtrack is ran, it executes again and again until an alternate route is found
#when 'E' is found the program ends, if every position has been checked and the E is not found then the program will end with the message letting the user know there is no solution

#*****The program is finished everything works*****

def main():
    
    mazefilename = input("please enter the name of the file with a maze: ")
    
    try:
        
        mazefile = open(mazefilename, 'r')  #opens the file to read
        Cmaze = construct(mazefile)  #Cmaze is assigned to the value of construct() which is a list that contains the entire maze if correct and error information if there is an invalid character
        if Cmaze == []:
            print('\nError: Specified file contains no maze.”\n')               #if construct returns an empty maze
        elif not Cmaze[0]:                                                      #Cmaze[0] is assigned to the bool 'False' if there is an invalid character
            print('\nError: Maze contains invalid characters. Line', Cmaze[1], 'contains invalid character ‘%s’\n' %(Cmaze[2]))
        else:
            XY = FindS(Cmaze)  #FindS() will take a maze and return [False, E_in, S_in] if missing start or end and return [True, [X,Y]] where X and Y are the start postions if start and end exist
            if XY[0]:           #The start and end positions exist if XY[0] is 'True'
                solve(Cmaze, XY[1])     #solves the maze where XY[1] is [X,Y] where X and Y are the start coordinates
            else:
                if not XY[1]:
                    print('\nError: No end position found.\n')  #checks to see which Key location is not found to return the appropriate error message; if both are missing it will return no end position found
                elif not XY[2]:
                    print('\nError: No start position found.\n')
        mazefile.close()        #closes the file before ending the program
        
    except FileNotFoundError:
        print("\nError: Specified file does not exist.\n")
        
def construct(Raw):
    
    maze = []
    row = 1
    
    for line in Raw:
        L = []      #L is the list for the line of the maze
        for P in line:
            if P not in ['#',' ','S','E','\n']: #checks to see if there are any characters that are not among these approved characters
                return [False,row,P]
            if P != '\n':       #\n is allowed to be in the file but it is not wanted in the maze so this line makes sure it is not added
                L.append(P)     #appends each character to the maze list
        
        maze.append(L) #once each line is finished the list is added to the maze list 
        row += 1  #the row is kept track of incase an invalid character is entered so that the line of the incorrect character can be correctly printed
        
    return maze #the final correct list is returned without any invalid characters

def FindS(M):
    
    E_in = False    #these variables are defaultes to false and become true once they are located
    S_in = False
    Y = 0
    for j in M:     #for each list inside the list for the maze; each list is one line of the maze
        if 'E' in j:   #if 'E' is in the list it will continue to look for 'S', otherwise it will check the next line
            E_in = True   
            for i in M:         #same for loop but now looking for 'S'
                if 'S' in i:
                    S_in = True
                    X = i.index('S') #X is set to the position in the line
                    XY = [Y,X]          #the positon in the line and the row are put in a list as one variable and then returned 
                    return [True,XY]
                Y += 1                  #Y is the line the function is currently on and will be used when S is found
                
    return [False, E_in, S_in]      #this will excecute if one of the key positions is not found in the maze; if E is not found the program will not look for S

def solve(maze, Pos):  #solve() is the brains of the program that will go from the start position to the end
    
    while True:
        Y = Pos[0]   #Pos is [X, Y] where X and Y are the positions vertically and horizontally so the list is broken up into it's components
        X = Pos[1]   #Pos[0] is X and Pos[1] is Y and will be referred to multiple times throughout this function
        
        Right = True  #by default a position over in every direction exists
        Down = True
        Left = True
        Up = True
        
        try:
            maze[Y][X+1]
        except IndexError:      #this try/except labyrinth checks a position in every direction to see if it exists; the variable for that direction is set to False if it doesn't exist
            Right = False
        try:
            maze[Y+1][X]
        except IndexError:
            Down = False
        try:
            maze[Y][X-1]
        except IndexError:
            Left = False
        try:
            maze[Y-1][X]
        except IndexError:
            Up = False

            
        if maze[Pos[0]][Pos[1]] == 'E':   #checks to see if the current position is the End and will break the loop if true
            #create(maze)  # <<<<this is here for testing and will only print the finished maze in cases of large test mazes
            break
        
        elif Right and len(maze[Y]) > X+1 and (maze[Y][X+1] in [' ','E']):      #first checks if spot to the right exists and then makes sure that that spot isn't greater than the length of the maze
            if maze[Y][X] != 'S':                                               #and finally checks is the spot to the right is a blank or the End
                maze[Y][X] = '>'    #will then make the previous position the right arrow unless it is the 'S'
            Pos = [Y, X+1]
            
        elif Down and len(maze) > Y+1 and (maze[Y+1][X] in [' ','E']):          #^^^^^same code written for every direction
            if maze[Y][X] != 'S':
                maze[Y][X] = 'v'
            Pos = [Y+1, X]
            
        elif Left and X-1 >= 0 and (maze[Y][X-1] in [' ','E']):         #for checking below and checking to the left the function makes sure the position wouldn't be less than zero
            if maze[Y][X] != 'S':
                maze[Y][X] = '<'
            Pos = [Y, X-1]
            
        elif Up and Y-1 >= 0 and (maze[Y-1][X] in [' ','E']):
            if maze[Y][X] != 'S':
                maze[Y][X] = '^'
            Pos = [Y-1, X]
            
        else:
            Blist = Backtrack(maze, Pos, X, Y, Right, Down, Left, Up)       #after checking all directions for space or E and there is none backtrack is triggered
            maze = Blist[0]
            Pos = Blist[1]
            
        if (not Right or maze[Y][X+1] not in [' ','>','<','v','^','S']) and (not Down or maze[Y+1][X] not in [' ','>','<','v','^','S']) and (not Left or maze[Y][X-1] not in [' ','>','<','v','^','S']) and (not Up or maze[Y-1][X] not in [' ','>','<','v','^','S']):
            print('\nError: No route could be found from start to end. Maze unsolvable.\n')     #after every single position that is possible is checked the program will end and be diclared impossible
            break
        
        create(maze) #every iteration at the end of the loop the maze is sent to create() which prints the maze so far

def create(maze):
    
    print('')
    for line in maze:           #prints the maze line by line
        string = ''
        for i in line:
            string += i
        print(string)
    print('')
    
def Backtrack(maze, Pos, X, Y, Right, Down, Left, Up): #backtrack() must import all variables used in solve() in order to
    
    if Right and len(maze[Y]) > X+1 and (maze[Y][X+1] in ['<',' ','S']):  
        if maze[Y][X] != 'S':
            maze[Y][X] = '.'
        Pos = [Y, X+1]
        
    elif Down and len(maze) > Y+1 and (maze[Y+1][X] in ['^',' ','S']):      #using the same syntax as in the solve(), backtrack() will do one step backwards onto a previous arrow and changes the position by one
        if maze[Y][X] != 'S':
            maze[Y][X] = '.'
        Pos = [Y+1, X]
        
    elif Left and X-1 >= 0 and (maze[Y][X-1] in ['>',' ','S']): #instead of looking for space or E, backtrack() will look for S or the arrow that would correspond to the opposite direction backtrack() is moving
        if maze[Y][X] != 'S':
            maze[Y][X] = '.'
        Pos = [Y, X-1]
        
    elif Up and Y-1 >= 0 and (maze[Y-1][X] in ['v',' ','S']):
        if maze[Y][X] != 'S':
            maze[Y][X] = '.'
        Pos = [Y-1, X]
        
    return [maze, Pos]    #backtrack() returns the maze with an added period and the position moved back one space

main()

#¤
