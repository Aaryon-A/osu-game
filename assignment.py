# -----------------------------------------------------------------------------
# Name:        Rhythm Hit (assignment.py)
# Purpose:     A game where you click on circles on the screen at a certain time to get a certain number of points
#
# Author:      Aaryon Arora
# Created:     29-Nov-2021
# Updated:     14-Jan-2022
# -----------------------------------------------------------------------------
# I think this project deserves a level 4 because ...
#
# Features Added:
#   Added videos as a background in some game screens
#   Elements of randomness for the game as well as different songs
#   Fully functioning leaderboard that saves progress even after the game is closed
#   Demonstrated good use of functions and classes
#   Added elements to make the game more aesthetic such as a growing and shrinking button
#   Added a cheat code that enables an 'AI' to play the game for the user
#
# -----------------------------------------------------------------------------
# Credits for images and videos
# Win Screen: https://picstatio.com/download/800x600/0ea252/cherry-blossom-anime-couple-kiss.jpg
# Help Background: https://images.genius.com/08ea977c06bdc9d09b8efcb55574465a.1000x1000x1.jpg
# Main Screen Background: https://wallpapercave.com/wp/wp5889965.jpg
# 3D Ocean Video: https://vimeo.com/546426731
# Ranking images, sound effects, cursor and help screen background: https://www.osuskins.me/skin/cookiezi-29-2018-03-18-764
# Songs from: https://www.youtube.com/watch?v=YjtSNyXoeDs&t=3s, https://www.youtube.com/watch?v=HpSW4P2ddMI, https://www.youtube.com/watch?v=dLdN_7IswJk, https://www.youtube.com/watch?v=yROYhefx-gs, https://www.youtube.com/watch?v=QRnO2D1jgWM&t=29s, https://www.youtube.com/watch?v=jeULjg08Lto, https://www.youtube.com/watch?v=7lKmet1dOiU&t=28s, https://www.youtube.com/watch?v=CG4YFATEUmA


# Grade: 4+
# Excellent Job!
import random
from math import sqrt, pi

import cv2
import pygame
from pygame import USEREVENT


# This class makes all the circles for the game screen
class CircleGeneration():
    def __init__(self, surface, position, radius, colour, circleNumber, font, increment):
        """
        This is the init function of the CircleGeneration class
        :param surface: surface
            This is where the circle gets drawn
        :param position: list
            These are the coordinates the circle gets drawn
        :param radius: int
            This is the size of the circle
        :param colour: tuple
            This is the colour of the circle
        :param circleNumber: int
            Each circle has a number on it that increases by 1 as the game progresses
        :param font: font
            This is the font used to render the circle number
        :param increment: int
            This is the number used for the outer ring around the circle to decrease by
        """
        self.surface = surface
        self.position = position
        self.radius = radius
        self.colour = colour
        self.circleNumber = circleNumber

        self.font = font

        self.borderColour = (255, 255, 255)
        self.borderRadius = radius * 3
        self.disappear = False

        self.borderIncrement = increment

    def draw(self):
        """
        This draws the circle on the screen as well as the number and outer ring
        :return:
            None
        """
        pygame.draw.circle(self.surface, self.colour, self.position, self.radius)
        pygame.draw.circle(self.surface, self.borderColour, self.position, self.borderRadius, 5)

        self.surface.blit(self.font.render(str(self.circleNumber), True, (0, 0, 0)),
                          (self.position[0] - 10, self.position[1] - 20))

    def updateBorder(self):
        """
        This slowly shrinks the outer ring to enclose the circle
        :return:
            None
        """
        self.borderRadius -= self.borderIncrement
        # Once the border is past the radius it sets a variable to True
        if self.borderRadius < self.radius - (self.radius / 10):
            self.disappear = True

    def checkCollision(self, point1, point2):
        """
        This calculates the distance between 2 points and returns the value
        :param point1: list
            Coordinates of the first point
        :param point2: list
            Coordinates of the second point
        :return:
            Returns an int value for the distance
        """
        distance = sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))

        return distance

    def borderDistance(self):
        """
        Returns the distance from the border to the circle
        :return:
            Returns an int value as the distance
        """
        return self.borderRadius - self.radius


# This is the class used for the slider generation
class SliderGeneration():
    def __init__(self, surface, rect, radius, rectColour, circleColour, text, font, direction, increment):
        """
        This is the init function of the SliderGeneration class
        :param surface: surface
            This is where the circle gets drawn
        :param rect: list
            This is a list of 4 numbers used to make the rectangle surrounding the circle
        :param radius: int
            This is the size of the circle
        :param rectColour: tuple
            This is the colour of the rectangle of the slider
        :param circleColour: tuple
            This is the colour of the circle
        :param text: int
            This is the number that goes on the circle
        :param font: font
            This is the font used to render the text
        :param direction: str
            This is the direction the slider goes towards (Right, Left, Up or Down)
        :param increment: int
            This is the number used for the outer ring around the circle to decrease by
        """
        self.surface = surface
        self.rect = rect
        self.radius = radius
        self.rectColour = rectColour
        self.circleColour = circleColour
        self.circleNumber = text
        self.font = font
        self.direction = direction

        self.borderRadius = self.radius * 3
        self.disappear = False

        self.borderIncrement = increment

        # Depending on the increment the outer ring closes by, the speed at which the slider moves is changed
        if increment == 0.8:
            self.sliderSpeed = 1
        elif increment == 1:
            self.sliderSpeed = 1.5
        elif increment == 1.2:
            self.sliderSpeed = 2

        # Depending on the direction of the slider, the rectangle and circle needs to be drawn in a different spot/orientation
        if self.direction == "Right":
            self.rect[2] = 150
            self.rect[3] = 60
            self.circlePosition = [self.rect[0] + self.radius, self.rect[1] + self.radius]
        elif self.direction == "Left":
            self.rect[2] = 150
            self.rect[3] = 60
            self.circlePosition = [self.rect[0] + self.rect[2] - self.radius, self.rect[1] + self.radius]
        elif self.direction == "Up":
            self.rect[2] = 60
            self.rect[3] = 150
            self.circlePosition = [self.rect[0] + self.radius, self.rect[1] + self.rect[3] - self.radius]
        elif self.direction == "Down":
            self.rect[2] = 60
            self.rect[3] = 150
            self.circlePosition = [self.rect[0] + self.radius, self.rect[1] + self.radius]

    def draw(self):
        """
        This is where the circle and the rectangle gets drawn to make one slider
        :return:
            None
        """
        pygame.draw.rect(self.surface, self.rectColour, self.rect, 20, 20, 20, 20)
        pygame.draw.circle(self.surface, self.circleColour, self.circlePosition, self.radius)

        pygame.draw.circle(self.surface, self.circleColour, self.circlePosition, self.borderRadius, 5)

        self.surface.blit(self.font.render(str(self.circleNumber), True, (255, 255, 255)),
                          (self.circlePosition[0] - 10, self.circlePosition[1] - 20))

    def update(self):
        """
        This moves the circle across the rectangle depending on the direction
        :return:
            None
        """
        if self.direction == "Right":
            self.circlePosition[0] += self.sliderSpeed
            self.borderRadius += self.borderIncrement
        elif self.direction == "Left":
            self.circlePosition[0] -= self.sliderSpeed
            self.borderRadius += self.borderIncrement
        elif self.direction == "Up":
            self.circlePosition[1] -= self.sliderSpeed
            self.borderRadius += self.borderIncrement
        elif self.direction == "Down":
            self.circlePosition[1] += self.sliderSpeed
            self.borderRadius += self.borderIncrement

    def updateBorder(self):
        """
        This slowly shrinks the outer circle
        :return:
            None
        """
        self.borderRadius -= self.borderIncrement
        # Once the border is past the radius it sets a variable to True
        if self.borderRadius < self.radius:
            self.disappear = True

    def checkCollision(self, point1, point2):
        """
        This calculates the distance between 2 points and returns the value
        :param point1: list
            Coordinates of the first point
        :param point2: list
            Coordinates of the second point
        :return:
            Returns an int value for the distance
        """
        distance = sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))

        return distance

    def borderDistance(self):
        """
            Returns the distance from the border to the circle
            :return:
                Returns an int value as the distance
            """
        return self.borderRadius - self.radius

    def slideFinish(self):
        """
        This is the collision detection to see if the circle has reached the end of the slider
        :return:
            Returns True or False depending on if the circle has reached the end
        """
        if self.direction == "Right":
            return self.circlePosition[0] + self.radius >= self.rect[0] + self.rect[2]
        elif self.direction == "Left":
            return self.circlePosition[0] - self.radius <= self.rect[0]
        elif self.direction == "Up":
            return self.circlePosition[1] - self.radius <= self.rect[1]
        elif self.direction == "Down":
            return self.circlePosition[1] + self.radius >= self.rect[1] + self.rect[3]


# This class is used to draw the circle button on the start screen
class CircleButtonGeneration():
    def __init__(self, surface, position, radius, colour, text, font):
        """
        This is the init function of the CircleButtonGeneration class
        :param surface: surface
            This is where the circle gets drawn
        :param position: list
            These are the coordinates the circle gets drawn
        :param radius: int
            This is the size of the circle
        :param colour: tuple
            This is the colour of the circle
        :param text: int
            The start button has text on it that says start
        :param font: font
            This is the font used to render the text
        """
        self.surface = surface
        self.position = position
        self.radius = radius
        self.originalRadius = radius
        self.colour = colour
        self.text = text
        self.font = font

        self.grow = "Grow"

    def draw(self):
        """
        This is used to draw the circle
        :return:
            None
        """
        pygame.draw.circle(self.surface, self.colour, self.position, self.radius)
        self.update()
        self.surface.blit(self.font.render(str(self.text), True, (0, 0, 0)),
                          (self.position[0] - 25, self.position[1] - 20))

    def update(self):
        """
        This makes the circle grow and shrink over time
        :return:
            None
        """
        if self.grow == "Grow":
            self.radius += 0.5
            if self.radius >= self.originalRadius * 2:
                self.grow = "Shrink"
        elif self.grow == "Shrink":
            self.radius -= 0.5
            if self.radius <= self.originalRadius:
                self.grow = "Grow"

    def large(self, grow):
        """
        This function is used to make the circle remain large when a mouse hovers over it
        :param grow: bool
            If True it will stop growing and shrinking
        :return:
            None
        """
        if grow:
            self.grow = "Stop"
            self.radius = self.originalRadius * 2.5
        else:
            self.grow = "Shrink"

    def checkCollision(self):
        """
        Determines the distance between 2 points
        :return:
            Returns True or False if the distance is less than the radius of the circle
        """
        point1 = pygame.mouse.get_pos()
        point2 = self.position
        distance = sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))

        return distance < self.radius


class ButtonGeneration():
    def __init__(self, rect, text, font, colour):
        """
        This is the init function of the button class
        :param rect: list
            List of 4 values that is used for the position of the button
        :param text: str
            String for the text that is printed on the button
        :param font: font
            Font variable that is used for the font of the text
        :param colour: list
            List of values for the colour
        """
        self.rect = rect
        self.text = text
        self.font = font
        self.colour = colour

    def draw(self, surface, offsetx, offsety):
        """
        Function for displaying the button on the screen
        :param surface: mainSurface
            Main Surface to display everything
        :return:
            None
        """
        pygame.draw.rect(surface, self.colour, self.rect, 0, 10, 10, 10, 10)

        # This is the code to show the text in the button
        words = self.font.render(self.text, True, (255, 255, 255))
        text_rect = (self.rect[0] + offsetx, self.rect[1] - offsety)
        surface.blit(words, text_rect)

    def update(self):
        """
        Checks to see if the mouse is inside the button
        :return:
            Returns True if the mouse is inside the button
        """
        if self.collidePoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def collidePoint(self, pointIn):
        """
        Function to check if the mouse is inside the button

        Gets the coordinates of the mouse and sees if its between the x coordinates and the y coordinates of the rectangle
        :param pointIn: list
            List of mouse coordinates
        :return:
            Returns True if the mouse is inside the rectangle
            Returns False if the mouse is not inside the rectangle
        """
        rectX = self.rect[0]
        rectY = self.rect[1]
        rectWidth = self.rect[2]
        rectHeight = self.rect[3]

        xIn = pointIn[0]
        yIn = pointIn[1]

        if rectX < xIn < rectX + rectWidth and rectY < yIn < rectY + rectHeight:
            return True
        else:
            return False

    def changeColour(self, hover):
        """
        Changes the colour of the rectangle depending on if the mouse is in the button
        :param hover: boolean
            True or False value
        :return:
            None
        """
        if hover:
            self.colour = pygame.Color("#556DC8")
        else:
            self.colour = pygame.Color("#E2BAB1")


def gameLoop(gameState):
    # -----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    global mousePos, borderDistance, combo, maxCirclesClicked, difficulty
    pygame.init()  # Prepare the pygame module for use
    pygame.mixer.init()
    surfaceSize = 480  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    # These are the songs and sounds used in the code
    hitSound = pygame.mixer.Sound("Media//Audio//drum-hitclap.wav")
    failSound = pygame.mixer.Sound("Media//Audio//combobreak-default.wav")

    gameSongs = ["Media//Audio//A Cruel Angel.mp3", "Media//Audio//Black Catcher.mp3",
                 "Media//Audio//Crossing Fields.mp3", "Media//Audio//Noragami.mp3", "Media//Audio//Inferno.mp3",
                 "Media//Audio//Polaris.mp3", "Media//Audio//Tokyo Revengers.mp3", "Media//Audio//Unravel.mp3"]

    # A variable to ensure certain sounds are only played once
    playFailSound = True

    # Variables for the circle generation
    circleRadius = 30
    circleNumber = 1
    borderDistance = 0
    borderCheck = False
    borderIncrement = 0.8

    # Font downloaded from https://fonts.google.com/specimen/Raleway
    # Fonts used throughout the code
    font = pygame.font.Font("Media//Raleway-MediumItalic.ttf", 40)
    buttonFont = pygame.font.Font("Media//Raleway-MediumItalic.ttf", 28)
    scoreFont = pygame.font.Font("Media//Raleway-MediumItalic.ttf", 24)
    textFont = pygame.font.Font("Media//Raleway-MediumItalic.ttf", 18)
    helpFont = pygame.font.Font("Media//Raleway-MediumItalic.ttf", 15)
    # Lists for the circles and sliders
    circles = []
    sliders = []

    # Different buttons used throughout the code
    startButton = ButtonGeneration([290, 130, 160, 35], "Start", buttonFont, pygame.Color("#556DC8"))
    helpButton = ButtonGeneration([300, 180, 150, 35], "Help", buttonFont, pygame.Color("#556DC8"))
    backButton = ButtonGeneration([50, 400, 100, 35], "Back", buttonFont, pygame.Color("#556DC8"))
    exitButton = ButtonGeneration([300, 230, 150, 35], "Exit", buttonFont, pygame.Color("#556DC8"))
    playButton = ButtonGeneration([350, 300, 130, 35], "Play", buttonFont, pygame.Color("#556DC8"))

    easyButton = ButtonGeneration([60, 100, 115, 200], "Easy", buttonFont, pygame.Color("#556DC8"))
    mediumButton = ButtonGeneration([185, 100, 115, 200], "Medium", buttonFont, pygame.Color("#556DC8"))
    hardButton = ButtonGeneration([310, 100, 115, 200], "Hard", buttonFont, pygame.Color("#556DC8"))

    # Pause Menu Buttons
    retryButton = ButtonGeneration([200, 100, 130, 35], "Retry", buttonFont, pygame.Color("#556DC8"))
    continueButton = ButtonGeneration([200, 150, 130, 35], "Continue", buttonFont, pygame.Color("#556DC8"))

    cheatCodeHelpButton = ButtonGeneration([50, 350, 100, 35], "Help", buttonFont, pygame.Color("#556DC8"))

    # Variables to determine if the mouse is hovering on a button
    startHover = False
    helpHover = False
    backHover = False
    exitHover = False
    playHover = False

    easyHover = False
    mediumHover = False
    hardHover = False

    retryHover = False
    continueHover = False

    cheatCodeHelpHover = False

    # These variables are used for the start screen button
    circleButtonPos = [200, 200]
    circleButtonRadius = 50
    circleButton = CircleButtonGeneration(mainSurface, circleButtonPos, circleButtonRadius, pygame.Color("#556DC8"),
                                          "Start",
                                          buttonFont)
    startCircleGrow = False
    circleHover = False

    # This variable makes it so the start screen buttons are only shown if the button is clicked
    showButtons = False

    # The help screen circle is displayed on the help screen
    helpScreenCircle = CircleGeneration(mainSurface, (100, 300), circleRadius, (255, 255, 255), 1, font,
                                        borderIncrement)
    helpScreenCircle2 = CircleGeneration(mainSurface, (300, 350), circleRadius, (255, 255, 255), 2, font,
                                         borderIncrement)
    helpScreenCircle.borderRadius = 50
    helpScreenCircle2.borderRadius = 70

    # This makes the mouse disappear and adds a custom image instead
    pygame.mouse.set_visible(False)
    cursorImage = pygame.image.load("Media//Images//cursor.png")
    cursorImageRect = cursorImage.get_rect()

    # Code on how to display videos found from https://stackoverflow.com/questions/21356439/how-to-load-and-play-a-video-in-pygame
    video = cv2.VideoCapture("Media//Videos//3d_ocean_1590675653.mov")
    startVideo = cv2.VideoCapture("Media//Videos//startVideo.mov")

    # These variables are used to display fading text
    goodbyeText = font.render("Goodbye", True, (255, 255, 255))
    copyGoodbyeText = goodbyeText.copy()
    alpha_surf = pygame.Surface(copyGoodbyeText.get_size(), pygame.SRCALPHA)
    alpha = 255

    winText = font.render("You Won", True, (255, 255, 255))
    copyWinText = winText.copy()
    win_surf = pygame.Surface(copyWinText.get_size(), pygame.SRCALPHA)
    winAlpha = 255

    # This is used for the combo display
    combo = 0
    fontSize = 40
    comboSizeIncrease = "Grow"

    # These variables are used for the sliders
    direction = ["Right", "Left", "Up", "Down"]
    sliderMove = False
    sliderBreak = False
    mouseSliderBreak = False

    # Used for the leaderboard
    leaderboardPoints = []
    leaderboardRanks = []
    leaderboardText = "--------"
    leaderboardFont = pygame.font.Font("Media//Raleway-MediumItalic.ttf", 20)

    try:
        # Reads the leaderboard file if it exists and assigns the values to a list
        file = open("points.txt", "r")
        point = file.readlines()
        for lines in point:
            leaderboardPoints.append(lines)

        file.close()
        leaderboardPoints = leaderboardPoints[-1].split(" ")
        del leaderboardPoints[-1]
    except FileNotFoundError as e:
        pass

    try:
        # Reads the leaderboard file if it exists and assigns the values to a list
        file = open("ranks.txt", "r")
        point = file.readlines()
        for lines in point:
            leaderboardRanks.append(lines)

        file.close()
        leaderboardRanks = leaderboardRanks[-1].split(" ")
        del leaderboardRanks[-1]
    except FileNotFoundError as e:
        pass

    # Used for the cheat code
    keysPressed = []
    cheatCode = False

    # If the game state is a cheat code it sets it equal to True and changes the difficulty
    if gameState[:-1] == "Cheat":
        cheatCode = True
        if gameState[-1] == "E":
            gameState = "Easy"
        elif gameState[-1] == "M":
            gameState = "Medium"
        elif gameState[-1] == "H":
            gameState = "Hard"

    # Depending on the difficulty it changes the durartion of the match, how quick objects spawn in and the speed at which they shrink and move
    if gameState == "Easy":
        pygame.time.set_timer(USEREVENT, random.randint(2000, 2500))
        borderIncrement = 0.8
        maxCirclesClicked = 30
        gameState = "Game"
        difficulty = 0.5

    if gameState == "Medium":
        pygame.time.set_timer(USEREVENT, 1800)
        borderIncrement = 1
        maxCirclesClicked = 40
        gameState = "Game"
        difficulty = 1

    if gameState == "Hard":
        pygame.time.set_timer(USEREVENT, 1500)
        borderIncrement = 1.2
        maxCirclesClicked = 50
        gameState = "Game"
        difficulty = 1.5

    # Used to keep track of progress of circles and sliders clicked
    circlesClicked = 0
    accuracy = 100.00
    hit300 = 0
    hit100 = 0
    hit50 = 0
    hit0 = 0

    # Used to determine the endgame
    endGame = False

    # Used to make the points smoothly increase
    points = 0
    oldPoints = 0

    # Used to ensure certain actions only happen once
    once = True
    twice = True

    while True:
        # -----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            return "Break"  # ... leave game loop
        elif ev.type == USEREVENT and not gameState == "Pause":
            rand = random.randint(1, 3)
            # This ensures only circles spawn in during the endgame
            if maxCirclesClicked - circlesClicked <= 3:
                circlePos = (random.randint(100, 400), random.randint(100, 400))
                circles.append(
                    CircleGeneration(mainSurface, circlePos, circleRadius, (255, 255, 255), circleNumber, font,
                                     borderIncrement))
            # This randomly spawns in either a slider or circle
            elif rand == 3:
                sliderRect = [random.randint(10, 325), random.randint(50, 325), 0, 0]
                sliders.append(
                    SliderGeneration(mainSurface, sliderRect, circleRadius, (255, 255, 255), (0, 0, 0), circleNumber,
                                     font, direction[random.randint(0, 3)], borderIncrement))
            elif rand == 1 or rand == 2:
                circlePos = (random.randint(100, 400), random.randint(100, 400))
                circles.append(
                    CircleGeneration(mainSurface, circlePos, circleRadius, (255, 255, 255), circleNumber, font,
                                     borderIncrement))
            circleNumber += 1
            # Once circleNumber goes over a random number it resets it back to 1
            if circleNumber > random.randint(5, 10):
                circleNumber = 1
        elif ev.type == pygame.KEYDOWN:
            # This detects input from the 'z' or 'x' key
            if (ev.key == pygame.K_z or ev.key == pygame.K_x) and not sliderMove and not cheatCode:
                if len(circles) > 0:
                    # Checks to ensure if there was a collision between the mouse and circle
                    if circles[0].checkCollision(mousePos, circles[0].position) < circleRadius:
                        # Saves the distance between the circle radius and the border
                        borderDistance = circles[0].borderDistance()
                        borderCheck = True
                        # Removes it from the screen
                        circles.pop(0)
                        combo += 1
                        comboSizeIncrease = "Grow"
                if len(sliders) > 0:
                    # Same collision detection happens for the sliders
                    if sliders[0].checkCollision(mousePos, sliders[0].circlePosition) < circleRadius:
                        sliderMove = True
                        borderDistance = sliders[0].borderDistance()
                        borderCheck = True
                        points += 30
            elif ev.key == pygame.K_ESCAPE:
                # On specific screen the escape key changes the game states
                if gameState == "Game":
                    gameState = "Pause"
                elif gameState == "Pause":
                    gameState = "Game"
                elif gameState == "Help":
                    return "Start"
                elif gameState == "Start":
                    showButtons = False
                elif gameState == "Main":
                    return "Start"
                elif gameState == "difficultySelection":
                    return "Main"
        elif ev.type == pygame.KEYUP:
            # On a slider you need to hold the button, if you let go the slider 'breaks'
            if ev.key == pygame.K_z or ev.key == pygame.K_x:
                if sliderMove:
                    sliderBreak = True
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            # This detects if the mouse clicked the button in the correct game state and does its correct action
            circleClicked = circleButton.checkCollision()
            if circleClicked and circleHover:
                showButtons = True
            startClicked = startButton.update()
            if startClicked and startHover:
                return "Main"
            helpClicked = helpButton.update()
            if helpClicked and helpHover:
                return "Help"
            backClicked = backButton.update()
            if backClicked and backHover and (gameState == "Pause" or gameState == "Win"):
                return "Main"
            elif backClicked and backHover and gameState == "Cheat Code Help":
                gameState = "Main"
            elif backClicked and backHover:
                return "Start"
            exitClicked = exitButton.update()
            if exitClicked and exitHover:
                return "Exit"
            playClicked = playButton.update()
            if playClicked and playHover:
                gameState = "difficultySelection"
            easyClicked = easyButton.update()
            if easyClicked and easyHover and cheatCode:
                return "CheatE"
            elif easyClicked and easyHover:
                return "Easy"
            mediumClicked = mediumButton.update()
            if mediumClicked and mediumHover and cheatCode:
                return "CheatM"
            elif mediumClicked and mediumHover:
                return "Medium"
            hardClicked = hardButton.update()
            if hardClicked and hardHover and cheatCode:
                return "CheatH"
            elif hardClicked and hardHover:
                return "Hard"
            retryClicked = retryButton.update()
            if retryClicked and retryHover:
                if difficulty == 0.5:
                    return "Easy"
                elif difficulty == 1:
                    return "Medium"
                elif difficulty == 1.5:
                    return "Hard"
            continueClicked = continueButton.update()
            if continueClicked and continueHover:
                gameState = "Game"
            cheatCodeHelpClicked = cheatCodeHelpButton.update()
            if cheatCodeHelpClicked and cheatCodeHelpHover:
                gameState = "Cheat Code Help"
            # The mouse also serves the same role as the 'z' and 'x' keys and can click circles and sliders
            if gameState == "Game" and not sliderMove and not cheatCode:
                if len(circles) > 0:
                    if circles[0].checkCollision(mousePos, circles[0].position) < circleRadius:
                        borderDistance = circles[0].borderDistance()
                        borderCheck = True
                        circles.pop(0)
                        combo += 1
                        comboSizeIncrease = "Grow"
                if len(sliders) > 0:
                    if sliders[0].checkCollision(mousePos, sliders[0].circlePosition) < circleRadius:
                        sliderMove = True
                        borderDistance = sliders[0].borderDistance()
                        borderCheck = True
                        points += 30
        # It also needs to be checked if the slider was broken
        elif ev.type == pygame.MOUSEBUTTONUP:
            if sliderMove and not cheatCode:
                sliderBreak = True
        # Once a certain number of circles have been clicked the timer turns off and it enters the endgame
        if gameState == "Game" and circlesClicked == maxCirclesClicked:
            pygame.time.set_timer(USEREVENT, 0)
            endGame = True
        # This block of code records all key inputs and gets looped through to see if a certain combination was pressed
        if ev.type == pygame.KEYDOWN and gameState == "Main":
            keysPressed.append(ev.key)
            if len(keysPressed) >= 11:
                for i in range(len(keysPressed) - 10):
                    if keysPressed[i] == pygame.K_UP and keysPressed[i + 1] == pygame.K_UP and keysPressed[
                        i + 2] == pygame.K_DOWN and keysPressed[i + 3] == pygame.K_DOWN and keysPressed[
                        i + 4] == pygame.K_LEFT and keysPressed[i + 5] == pygame.K_RIGHT and keysPressed[
                        i + 6] == pygame.K_LEFT and keysPressed[i + 7] == pygame.K_RIGHT and keysPressed[
                        i + 8] == pygame.K_b and keysPressed[i + 9] == pygame.K_a and keysPressed[
                        i + 10] == pygame.K_RETURN:
                        cheatCode = True

        # -----------------------------Game Logic---------------------------------------------#
        # Update your game objects and data structures here...
        if gameState == "Game":
            # This ensures the music starts playing only once
            once = True
            if twice:
                musicStop(0) # Stops music from the help screen
                musicStop(2)
                backgroundMusic(random.choice(gameSongs), 1)
                twice = False
            elif not twice:
                musicResume(1)
                musicStop(0) # Stops the music if you click continue from the help screen

            # Runs if the cheat code has been activated
            if cheatCode:
                # I used 2 if statements to ensure that if the mouse is on a slider it stays on the slider until it finishes
                # Since if statements go in order the mouse won't move to the circle until the slider finishes
                if len(sliders) >= 1:
                    if len(sliders) >= 1:
                        # Same thing happens with the sliders
                        pygame.mouse.set_pos(sliders[0].circlePosition)
                        if sliders[0].borderDistance() <= 15:
                            if not sliderMove:
                                borderCheck = True
                            sliderMove = True
                            borderDistance = 15
                            points += 30
                    elif len(circles) >= 1:
                        # The circles automatically get clicked once the border reaches a certain point
                        pygame.mouse.set_pos(circles[0].position)
                        if circles[0].borderDistance() <= 15:
                            borderDistance = 15
                            borderCheck = True
                            circles.pop(0)
                            combo += 1
                            comboSizeIncrease = "Grow"
                elif len(circles) >= 1:
                    if len(circles) >= 1:
                        # The circles automatically get clicked once the border reaches a certain point
                        pygame.mouse.set_pos(circles[0].position)
                        if circles[0].borderDistance() <= 15:
                            borderDistance = 15
                            borderCheck = True
                            circles.pop(0)
                            combo += 1
                            comboSizeIncrease = "Grow"
                    elif len(sliders) >= 1:
                        # Same thing happens with the sliders
                        pygame.mouse.set_pos(sliders[0].circlePosition)
                        if sliders[0].borderDistance() <= 15:
                            if not sliderMove:
                                borderCheck = True
                            sliderMove = True
                            borderDistance = 15
                            points += 30

            # This block of code allows a video to be displayed on the game screen
            # It will remain commented because it makes the frame count of the game drop

            # success, videoImage = video.read()
            # if success:
            #     videoSurf = pygame.image.frombuffer(videoImage.tobytes(), videoImage.shape[1::-1], "BGR")
            # else:
            #     print("Done")

            # Saves the position of the mouse in a variable
            mousePos = pygame.mouse.get_pos()

            # If the mouse leaves the circle while the slider has started moving it is considered a slider break
            if sliderMove and not mouseSliderBreak:
                if sliders[0].checkCollision(mousePos, sliders[0].circlePosition) > circleRadius + 10:
                    sliderBreak = True
                    mouseSliderBreak = True

            # Once that happens the combo resets and a sound might play depending on the combo
            if sliderBreak:
                if playFailSound and combo >= 5:
                    musicPlay(failSound)
                    playFailSound = False
                sliderBreak = False
                combo = -1

            # Depending on the time when the circle was clicked, a certain number of points are rewarded
            if borderCheck:
                if borderDistance <= 15:
                    points += 300 + (300 * (((combo - 1) * difficulty) / 25))
                    hit300 += 1
                    musicPlay(hitSound)
                elif 15 < borderDistance <= 25:
                    points += 100 + (100 * (((combo - 1) * difficulty) / 25))
                    hit100 += 1
                    musicPlay(hitSound)
                elif 25 < borderDistance <= 30:
                    points += 50 + (50 * (((combo - 1) * difficulty) / 25))
                    hit50 += 1
                    musicPlay(hitSound)
                else:
                    if combo >= 5:
                        musicPlay(failSound)
                    combo = -1
                    hit0 += 1

                # This ensures the points are only rewarded once
                borderCheck = False
                circlesClicked += 1

            # -----------------------------Drawing Everything-------------------------------------#
            # We draw everything from scratch on each frame.
            # So first fill everything with the background color

            mainSurface.fill((0, 0, 0))

            # This is used to display the video and will also remain commented
            # mainSurface.blit(videoSurf, (0, 0))

            # Instead I chose to blit an image to the screen
            mainSurface.blit(pygame.image.load("Media//Images//Game Screen Background.jpg"), (0, 0))

            # If there is more than one object on the screen, a line is drawn between them
            if len(circles) >= 2:
                pygame.draw.aaline(mainSurface, (255, 255, 255), circles[0].position, circles[1].position)
            elif len(circles) >= 1 and len(sliders) >= 1:
                pygame.draw.aaline(mainSurface, (255, 255, 255), circles[0].position, sliders[0].circlePosition)
            elif len(sliders) >= 2:
                pygame.draw.aaline(mainSurface, (255, 255, 255), sliders[0].circlePosition, sliders[1].circlePosition)

            if sliderMove and len(sliders) > 0:
                # This moves the slider across the screen
                sliders[0].update()
                points += 30

                # Once the slider finishes it resets all variables and removes the slider from the screen
                if sliders[0].slideFinish():
                    points += 30
                    sliders.pop(0)
                    sliderMove = False
                    combo += 1
                    musicPlay(hitSound)
                    mouseSliderBreak = False
                    playFailSound = True

            # The slider also disappears if the user fails to click it and it is treated as a slider break
            if len(sliders) > 0:
                if sliders[0].disappear:
                    sliders.pop(0)
                    sliderMove = False
                    if combo >= 5:
                        musicPlay(failSound)

                    combo = 0
                    comboSizeIncrease = "Grow"
                    circlesClicked += 1
                    hit0 += 1

            # This was a concept for drawing a curved slider
            # I wasn't able to do it but I'm leaving it commented

            # pygame.draw.arc(mainSurface, (255, 255, 255), [100, 100, 20, 300], pi / 4, (17*pi) / 9, 60)

            # Circles also disappear if they aren't clicked in time
            if len(circles) > 0:
                if circles[0].disappear:
                    circles.pop(0)
                    if combo >= 5:
                        musicPlay(failSound)

                    combo = 0
                    comboSizeIncrease = "Grow"
                    circlesClicked += 1
                    hit0 += 1

            # This draws both the circle and slider in their respective lists
            for circle in circles:
                circle.draw()
                circle.updateBorder()

            for slider in sliders:
                slider.draw()
                slider.updateBorder()

            # This is used to display a visual aid to show the progress of the game
            pygame.draw.circle(mainSurface, (255, 255, 255), (230, 30), 25, 2)
            if circlesClicked > 0:
                pygame.draw.arc(mainSurface, (255, 255, 255), [205, 5, 50, 50], 0,
                                (circlesClicked / maxCirclesClicked) * (2 * pi), 60)

            # This makes the combo grow and shrink each time it increases
            if combo > 1:
                fontSize = displayCombo(mainSurface, fontSize, combo, comboSizeIncrease)
                # Once the font is at a certain size it changes the variable to be used in the function
                if fontSize >= 50:
                    comboSizeIncrease = "Shrink"
                elif fontSize <= 40:
                    comboSizeIncrease = "Stop"

            if circlesClicked > 0:
                # This calculates accuracy
                accuracy = calculateAccuracy(hit0, hit50, hit100, hit300, accuracy)

            # This displays the accuracy on the screen and centers it
            accuracyText = buttonFont.render("{:.2f}%".format(accuracy), True, (255, 255, 255))
            accuracyRect = accuracyText.get_rect(center=(surfaceSize / 4, 30))
            mainSurface.blit(accuracyText, accuracyRect)

            # This calculates the points
            oldPoints = calculateScore(oldPoints, points)
            # This is used to display a number of 0's along with the actual number
            pointText = "0" * (7 - len(str(oldPoints))) + str(oldPoints)
            pointRenderedText = buttonFont.render(pointText, True, (255, 255, 255))
            mainSurface.blit(pointRenderedText, pointRenderedText.get_rect(center=((3 * surfaceSize) / 4, 30)))

            if endGame:
                # Once the game has entered the endgame it displays text and fades away
                if winAlpha > 0:
                    # Reduce alpha each frame, but make sure it doesn't get below 0.
                    winAlpha = max(winAlpha - 4, 0)
                    copyWinText = winText.copy()  # Don't modify the original text surf.
                    # Fill alpha_surf with this color to set its alpha value.
                    win_surf.fill((255, 255, 255, winAlpha))
                    # To make the text surface transparent, blit the transparent
                    # alpha_surf onto it with the BLEND_RGBA_MULT flag.
                    copyWinText.blit(win_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                else:
                    # Once the text fades away it enters the win gamestate and records the point and rank to the leaderboard
                    gameState = "Win"
                    leaderboardPoints.append(f"{(round(points))}")
                    leaderboardRanks.append(f"{calculateRank(accuracy, hit0, hit50)}")

                    # Writes the points in the leaderboardPoints list in a file
                    file = open("points.txt", "w")
                    for point in leaderboardPoints:
                        file.write(f"{point} ")

                    file.close()

                    # Writes the ranks in the leaderboardRanks list in a file
                    file = open("ranks.txt", "w")
                    for rank in leaderboardRanks:
                        file.write(f"{rank} ")

                    file.close()

                mainSurface.fill((30, 30, 30))
                mainSurface.blit(copyWinText, copyWinText.get_rect(center=(240, 240)))

        if gameState == "Pause":
            # Pause the game music
            musicPause(1)

            mainSurface.fill((0, 0, 0))

            mainSurface.blit(pygame.image.load("Media//Images//pauseScreenBackground.png"), (0, 0))

            # Draw the pause screen buttons
            backButton.draw(mainSurface, 15, 5)
            backHover = backButton.update()
            backButton.changeColour(backHover)

            retryButton.draw(mainSurface, 15, 0)
            retryHover = retryButton.update()
            retryButton.changeColour(retryHover)

            continueButton.draw(mainSurface, 0, 0)
            continueHover = continueButton.update()
            continueButton.changeColour(continueHover)

            # Play the pause screen sound once so it doesn't keep resetting
            if once:
                backgroundMusic("Media//Audio//failsound.mp3", 0)
                once = False

        if gameState == "Win":
            # Resets twice variable for later use and stops the game music
            twice = True
            musicStop(1)

            mainSurface.fill((0, 0, 0))
            mainSurface.blit(pygame.image.load("Media//Images//Win Screen.jpg"), (0, 0))

            # Displays the leaderboard
            displayLeaderboard(leaderboardPoints, leaderboardRanks, mainSurface, leaderboardFont, leaderboardText)
            displayStats(hit0, hit50, hit100, hit300, accuracy, buttonFont, scoreFont, mainSurface, points)

            backButton.draw(mainSurface, 20, 5)
            backHover = backButton.update()
            backButton.changeColour(backHover)

            # Plays the win music once
            if once:
                backgroundMusic("Media//Audio//applause.mp3", 0)
                once = False

        if gameState == "Main":
            mainSurface.fill((0, 0, 0))
            mainSurface.blit(pygame.image.load("Media//Images//mainScreenBackground.jpg"), (0, 0))

            # Draws the buttons for the main screen
            playButton.draw(mainSurface, 50, 5)
            playHover = playButton.update()
            playButton.changeColour(playHover)

            backButton.draw(mainSurface, 20, 5)
            backHover = backButton.update()
            backButton.changeColour(backHover)

            mainSurface.blit(font.render("Leaderboard", True, (0, 0, 0)), (50, 35))

            displayLeaderboard(leaderboardPoints, leaderboardRanks, mainSurface, leaderboardFont, leaderboardText)

            # If the cheat code has been activated then displays a hidden help screen and text
            if cheatCode:
                mainSurface.blit(buttonFont.render("Cheat Code Activated", True, (0, 0, 0)), (200, 400))

                cheatCodeHelpButton.draw(mainSurface, 20, 5)
                cheatCodeHelpHover = cheatCodeHelpButton.update()
                cheatCodeHelpButton.changeColour(cheatCodeHelpHover)

        if gameState == "Cheat Code Help":
            mainSurface.fill((0, 0, 0))

            mainSurface.blit(pygame.image.load("Media//Images//helpBackground.jpg"), (0, 0))

            backButton.draw(mainSurface, 20, 5)
            backHover = backButton.update()
            backButton.changeColour(backHover)

            # Help screen text
            displayText(mainSurface, font, "You have Activated", (255, 255, 255), [0, 20], True)
            displayText(mainSurface, font, "the Cheat Code", (255, 255, 255), [0, 50], True)
            displayText(mainSurface, textFont, "The game will now be auto played by AI", (255, 255, 255), [0, 150],
                        True)
            displayText(mainSurface, textFont, "The cheat code will remain for the duration of the song",
                        (255, 255, 255), [0, 175], True)
            displayText(mainSurface, textFont, "If you go back or click retry the cheat code will deactivate",
                        (255, 255, 255), [0, 200], True)
            displayText(mainSurface, font, "Have Fun!", (255, 255, 255), [0, 300], True)

        if gameState == "difficultySelection":
            # This screen is only used to select a difficulty for the game

            mainSurface.fill((0, 0, 0))
            mainSurface.blit(pygame.image.load("Media//Images//mainScreenBackground.jpg"), (0, 0))

            # Draws the different buttons for the difficulties
            easyButton.draw(mainSurface, 30, -50)
            easyHover = easyButton.update()
            easyButton.changeColour(easyHover)

            mediumButton.draw(mainSurface, 5, -50)
            mediumHover = mediumButton.update()
            mediumButton.changeColour(mediumHover)

            hardButton.draw(mainSurface, 30, -50)
            hardHover = hardButton.update()
            hardButton.changeColour(hardHover)

        if gameState == "Start":
            mainSurface.fill((0, 0, 0))

            musicStop(0)
            # Stops music and plays a random song from the list of gameSongs
            if once:
                backgroundMusic(random.choice(gameSongs), 2)
                once = False

            # This code is used to display a video on the start screen
            startSuccess, startVideoImage = startVideo.read()
            if startSuccess:
                startVideoSurf = pygame.image.frombuffer(startVideoImage.tobytes(), startVideoImage.shape[1::-1], "BGR")
            else:
                return "Start"

            mainSurface.blit(startVideoSurf, (-100, -100))

            # This code shows the large circle button
            circleHover = circleButton.checkCollision()
            # If the mouse is on the circle button then keep the button large
            if circleButton.checkCollision():
                circleButton.large(True)
                startCircleGrow = True

            if startCircleGrow and not showButtons:
                circleButton.large(False)
                startCircleGrow = False

            if showButtons:
                # Draws the buttons if the circle button is clicked
                startButton.draw(mainSurface, 50, 5)
                startHover = startButton.update()
                startButton.changeColour(startHover)

                helpButton.draw(mainSurface, 40, 5)
                helpHover = helpButton.update()
                helpButton.changeColour(helpHover)

                exitButton.draw(mainSurface, 40, 5)
                exitHover = exitButton.update()
                exitButton.changeColour(exitHover)

                displayText(mainSurface, font, "Rhythm Hit", (255, 255, 255), [50, 400], False)

            circleButton.draw()

        if gameState == "Help":
            # The game state is used to display instructions
            mainSurface.fill((0, 0, 0))

            mainSurface.blit(pygame.image.load("Media//Images//helpBackground.jpg"), (0, 0))

            backButton.draw(mainSurface, 20, 5)
            backHover = backButton.update()
            backButton.changeColour(backHover)

            displayText(mainSurface, font, "Welcome to Rhythm Hit", (255, 255, 255), [0, 20], True)
            displayText(mainSurface, helpFont, "To play the game you must hit circles that appear on the screen.",
                        (255, 255, 255), [0, 100], True)
            displayText(mainSurface, helpFont,
                        "You must click it when the border is as close to the circle as possible.", (255, 255, 255),
                        [0, 125], True)
            displayText(mainSurface, helpFont, "Clicking circles with more accuracy awards you more points.",
                        (255, 255, 255), [0, 150], True)
            displayText(mainSurface, helpFont, "You can either use the mouse button or the keys Z or X.",
                        (255, 255, 255), [0, 175], True)
            displayText(mainSurface, helpFont, "Hover your mouse over the circle and click whatever key you want.",
                        (255, 255, 255), [0, 200], True)

            # Draws 2 circles as visual aid for the user
            pygame.draw.aaline(mainSurface, (255, 255, 255), helpScreenCircle.position, helpScreenCircle2.position)
            helpScreenCircle.draw()
            helpScreenCircle2.draw()

        if gameState == "Exit":
            # Code on how to fade text found at https://stackoverflow.com/questions/52856030/how-to-fade-in-and-out-a-text-in-pygame
            if alpha > 0:
                # Reduce alpha each frame, but make sure it doesn't get below 0.
                alpha = max(alpha - 4, 0)
                copyGoodbyeText = goodbyeText.copy()  # Don't modify the original text surf.
                # Fill alpha_surf with this color to set its alpha value.
                alpha_surf.fill((255, 255, 255, alpha))
                # To make the text surface transparent, blit the transparent
                # alpha_surf onto it with the BLEND_RGBA_MULT flag.
                copyGoodbyeText.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                return "Break"

            mainSurface.fill((30, 30, 30))
            mainSurface.blit(copyGoodbyeText, copyGoodbyeText.get_rect(center=(240, 240)))

        cursorImageRect.center = pygame.mouse.get_pos()
        mainSurface.blit(cursorImage, cursorImageRect)

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        clock.tick(60)  # Force frame rate to be slower


def musicPlay(sound):
    """
    Plays music by taking in a sound effect and stops it once it has finished playing
    :param sound: Sound
        Sound object to be played
    :return:
        None
    """
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()


def backgroundMusic(soundFile, channel):
    """
    Plays a sound file on a specific channel. I use 0 for sound effects and 1 for background music
    :param soundFile: str
        Sound file to be played
    :param channel: int
        Channel number to play sound file on
    :return:
        None
    """
    pygame.mixer.Channel(channel).play(pygame.mixer.Sound(soundFile))


def musicStop(channel):
    """
    Stops playing music on a specific channel
    :param channel: int
        Channel number to stop playing music in
    :return:
        None
    """
    pygame.mixer.Channel(channel).stop()


def musicPause(channel):
    """
    Pauses music on a specific channel
    :param channel: int
        Channel number to pause music in
    :return:
        None
    """
    pygame.mixer.Channel(channel).pause()


def musicResume(channel):
    """
    Resumes music on a specific channel
    :param channel: int
        Channel number to resume music in
    :return:
        None
    """
    pygame.mixer.Channel(channel).unpause()


def displayText(surface, font, text, colour, position, center):
    """
    A function to easily display text on the screen
    :param surface: Surface
        Surface to display text on
    :param font: font
        Font object used to render text
    :param text: str
        Text to display on the screen
    :param colour: tuple
        Numbers for the colour of the text
    :param position: list
        Coordinates to display the text at
    :param center: bool
        If True the text will be centered on the screen
    :return:
        None
    """
    renderedText = font.render(text, True, colour)
    if center:
        # If the text is to be centered it gets centered at the middle of the screen
        centerPosition = renderedText.get_rect(center=(240, 240))
        position[0] = centerPosition[0]
    surface.blit(renderedText, position)


def displayCombo(surface, fontSize, text, increase):
    """
    Used to display the combo in an aesthetic way. When the combo increases it momentarily grows then shrinks
    :param surface: surface
        Surface to display the combo on
    :param fontSize: int
        Used to increase the font size and decrease the font size
    :param text: str
        Combo text
    :param increase: str
        Used to tell the program if the combo needs to shrink or grow
    :return:
        Returns the font size to be used in the code and re-used in the function
    """
    comboFont = pygame.font.Font("Media//Raleway-MediumItalic.ttf", fontSize)
    renderedText = comboFont.render(f"{str(text)}x", True, (255, 255, 255))
    centerPosition = renderedText.get_rect(center=(35, 430))

    surface.blit(renderedText, centerPosition)

    if increase == "Grow":
        fontSize += 1
    elif increase == "Shrink":
        fontSize -= 1

    return fontSize


def displayStats(hit0, hit50, hit100, hit300, accuracy, font, scoreFont, surface, score):
    """
    A function to display the stats on the win screen
    :param hit0: int
        Number of times a circle was missed
    :param hit50: int
        Number of times 50 points was scored
    :param hit100: int
        Number of times 100 points was scored
    :param hit300: int
        Number of times 300 points was scored
    :param accuracy: float
        Final accuracy for the game
    :param font: Font
        Font used to render the text
    :param surface: Surface
        Surface to display the stats on
    :param score: int
        Final score after completing the game
    :return:
        None
    """
    # Displays all the points scored
    points0 = font.render(f"    X: {hit0}", True, (255, 240, 240))
    points50 = font.render(f"  50: {hit50}", True, (255, 240, 240))
    points100 = font.render(f"100: {hit100}", True, (255, 240, 240))
    points300 = font.render(f"300: {hit300}", True, (255, 240, 240))

    surface.blit(points0, (275, 250))
    surface.blit(points50, (275, 300))
    surface.blit(points100, (275, 350))
    surface.blit(points300, (275, 400))

    # Displays the points and centers it
    statText = scoreFont.render(f"Score: {int(score)} points", True, (255, 255, 255))
    surface.blit(statText, statText.get_rect(center=(325, 205)))

    pygame.draw.rect(surface, (255, 255, 255), [225, 230, 200, 230], 1)

    # Displays the accuracy
    accuracyText = font.render(f"{accuracy}%", True, (255, 255, 255))
    surface.blit(accuracyText, accuracyText.get_rect(center=(110, 30)))

    # Calculates the rank and depending on the rank it displays an image
    rank = calculateRank(accuracy, hit0, hit50)

    if rank == "S":
        rankS = pygame.image.load("Media//Images//ranking-S-small@2x.png")
        surface.blit(rankS, rankS.get_rect(center=(400, 50)))
    elif rank == "A":
        rankA = pygame.image.load("Media//Images//ranking-A-small@2x.png")
        surface.blit(rankA, rankA.get_rect(center=(400, 50)))
    elif rank == "B":
        rankB = pygame.image.load("Media//Images//ranking-B-small@2x.png")
        surface.blit(rankB, rankB.get_rect(center=(400, 50)))
    elif rank == "C":
        rankC = pygame.image.load("Media//Images//ranking-C-small@2x.png")
        surface.blit(rankC, rankC.get_rect(center=(400, 50)))
    elif rank == "D":
        rankD = pygame.image.load("Media//Images//ranking-D-small@2x.png")
        surface.blit(rankD, rankD.get_rect(center=(400, 50)))


def calculateRank(accuracy, hit0, hit50):
    """
    Returns a rank depending on how good the user performed
    :param accuracy: float
        Final accuracy of the game
    :param hit0: int
        Number of times 0 points was scored
    :param hit50: int
        Number of times 50 points was scored
    :return:
    """
    if accuracy >= 95 and hit0 == 0 and hit50 == 0:
        return "S"
    elif accuracy >= 92 and hit0 == 0:
        return "A"
    elif accuracy >= 86:
        return "B"
    elif accuracy >= 76:
        return "C"
    else:
        return "D"


def displayLeaderboard(leaderboardPoints, leaderboardRanks, surface, font, text):
    """
    Used to display the leaderboard on the main screen and the win screen
    :param leaderboardPoints: list
        List of points scored in all games
    :param leaderboardRanks: list
        List of ranks achieved in all games
    :param surface: Surface
        Surface used to display the leaderboard on
    :param font: Font
        Font used to render the text for the leaderboard
    :param text: str
        Text used as filler text if there is not enough points
    :return:
    """

    # Changes all the points in the list to int
    leaderboardPoints = [int(i) for i in leaderboardPoints]

    # Credit for sorting 2 lists: https://stackoverflow.com/questions/9764298/how-to-sort-two-lists-which-reference-each-other-in-the-exact-same-way
    try:
        # Sorts 2 different lists but keeps the order
        leaderboardPoints, leaderboardRanks = zip(*sorted(zip(leaderboardPoints, leaderboardRanks), reverse=True))
    except ValueError as e:
        pass

    try:
        # This ensures that only 9 different points are listed in the leaderboard
        if len(leaderboardPoints) > 5:
            for i in range(5):
                surface.blit(
                    font.render(f"{i + 1}: {leaderboardPoints[i]} points --- {leaderboardRanks[i]}", True, (0, 0, 0)),
                    (50, i * 30 + 90))
        else:
            for i in range(len(leaderboardPoints)):
                surface.blit(
                    font.render(f"{i + 1}: {leaderboardPoints[i]} points --- {leaderboardRanks[i]}", True, (0, 0, 0)),
                    (50, i * 30 + 90))

        # After printing the points print some filler text
        for i in range(len(leaderboardPoints), 5):
            surface.blit(font.render(f"{i + 1}: {text}", True, (0, 0, 0)),
                         (50, i * 30 + 90))
    except Exception as e:  # An error occurs if the file is not created (The user clicks on the leaderboard right away)
        for i in range(5):
            surface.blit(font.render(f"{i + 1}: {text}", True, (0, 0, 0)),
                         (50, i * 30 + 90))


def calculateAccuracy(hit0, hit50, hit100, hit300, accuracy):
    """
    This function is used to smoothly increase the accuracy during the game
    :param hit0: int
        Number of times a circle was missed
    :param hit50: int
        Number of times 50 points was scored
    :param hit100: int
        Number of times 100 points was scored
    :param hit300: int
        Number of times 300 points was scored
    :param accuracy: float
        Final accuracy for the game
    :return:
        Returns the last accuracy to be used again in the function
    """
    # newAccuracy is the most recent accuracy and lastAccuracy is the previous accuracy
    newAccuracy = ((50 * hit50) + (100 * hit100) + (300 * hit300)) / (300 * (hit0 + hit50 + hit100 + hit300)) * 100
    newAccuracy = round(newAccuracy, 2)
    lastAccuracy = round(accuracy, 2)

    # The function checks if the accuracy has changed
    # If it has it either increases the last accuracy or decreases it
    # It also changes it by the digit
    if newAccuracy != lastAccuracy:
        if lastAccuracy > newAccuracy:
            if (lastAccuracy - newAccuracy) <= 0.1:
                lastAccuracy -= 0.01
            elif (lastAccuracy - newAccuracy) <= 1:
                lastAccuracy -= 0.1
            elif (lastAccuracy - newAccuracy) <= 10:
                lastAccuracy -= 1
            else:
                lastAccuracy -= 10
        elif lastAccuracy < newAccuracy:
            if (newAccuracy - lastAccuracy) <= 0.1:
                lastAccuracy += 0.01
            elif (newAccuracy - lastAccuracy) <= 1:
                lastAccuracy += 0.1
            elif (newAccuracy - lastAccuracy) <= 10:
                lastAccuracy += 1
            else:
                lastAccuracy += 10

    return lastAccuracy


def calculateScore(oldScore, newScore):
    """
    This function smoothly changes the score to be displayed on the game screen
    :param oldScore: int
        Previous score that the user had
    :param newScore: int
        Most recent score the user has
    :return:
        Returns the previous accuracy to be re-used by the function
    """

    # The old score keeps changing and once old score is equal to new score the function doesn't do anything
    if oldScore < newScore:
        if (newScore - oldScore) <= 10:
            oldScore += 1
        elif (newScore - oldScore) <= 100:
            oldScore += 10
        else:
            oldScore += 100

    return oldScore


def main():
    """
    This is the function where the game loop runs forever until exited
    :return:
        None
    """
    gameState = "Start"
    while True:
        # The game state is used as a parameter as the function and it keeps changing when the gameLoop changes game states
        # I did it like this to make it easier to reset every variable for playing again
        gameState = gameLoop(gameState)
        if gameState == "Break":
            break


main()
