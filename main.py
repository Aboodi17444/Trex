import pygame
import os
import random

# Initiera Pygame biblioteket
pygame.init()

# Globala konstanter för skärmbredd och skärmhöjd
SKÄRM_BREDD = 1100
SKÄRM_HÖJD = 600
# Skapa en skärm med angiven storlek
SKÄRM = pygame.display.set_mode((SKÄRM_BREDD, SKÄRM_HÖJD))

# Ladda bilder för T-rex-dinosaurie, kaktusar, fågel, himmel och marken
SPRINGA = [pygame.image.load(os.path.join("T-rex/Dinasorie", "Ruscha1.png")),
           pygame.image.load(os.path.join("T-rex/Dinasorie", "Ruscha2.png"))]
HOPPA = pygame.image.load(os.path.join("T-rex/Dinasorie", "Hoppa.png"))
DUCKA = [pygame.image.load(os.path.join("T-rex/Dinasorie", "Ducka1.png")),
           pygame.image.load(os.path.join("T-rex/Dinasorie", "Ducka2.png"))]

KAKTUS = [pygame.image.load(os.path.join("T-rex/Kaktus", "Kaktus1.png")),
          pygame.image.load(os.path.join("T-rex/Kaktus", "Kaktus2.png")),
          pygame.image.load(os.path.join("T-rex/Kaktus", "Kaktus3.png"))]
STOR_KAKTUS = [pygame.image.load(os.path.join("T-rex/Kaktus", "Storkaktus1.png")),
               pygame.image.load(os.path.join("T-rex/Kaktus", "Storkaktus2.png")),
               pygame.image.load(os.path.join("T-rex/Kaktus", "Storkaktus3.png"))]

FÅGEL = [pygame.image.load(os.path.join("T-rex/Fågel", "Fågel1.png")),
         pygame.image.load(os.path.join("T-rex/Fågel", "Fågel2.png"))]

HIMMEL = pygame.image.load(os.path.join("T-rex/Annat", "Himmel.png"))
MARKEN = pygame.image.load(os.path.join("T-rex/Annat", "Marken.png"))



# Klassen för dinosaurien
class Dinosaur:
    X_axel = 80
    Y_axel = 310
    Y_axel_DUCKA = 340
    HÖJD_DUCKA = 8.5

    def __init__(self):
        # Ladda bilderna för ducka, springa och hoppa
        self.duck_img = DUCKA
        self.run_img = SPRINGA
        self.jump_img = HOPPA

        # Boolean-värden för att hantera olika tillstånd
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        # Index för steg och hoppets hastighet
        self.step_index = 0
        self.jump_vel = self.HÖJD_DUCKA
        # Aktuell bild och rektangel för dinosaurien
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_axel
        self.dino_rect.y = self.Y_axel

    # Uppdatera dinosauriens tillstånd baserat på användarinmatning
    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    # Metod för att ducka
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_axel
        self.dino_rect.y = self.Y_axel_DUCKA
        self.step_index += 1

    # Metod för att springa
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_axel
        self.dino_rect.y = self.Y_axel
        self.step_index += 1

    # Metod för att hoppa
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.HÖJD_DUCKA:
            self.dino_jump = False
            self.jump_vel = self.HÖJD_DUCKA

    # Metod för att rita dinosaurien på skärmen
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


# Klassen för moln
class Cloud:
    def __init__(self):
        # Slumpmässig position och bild för molnet
        self.x = SKÄRM_BREDD + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = HIMMEL
        self.width = self.image.get_width()

    # Uppdatera molnets position
    def update(self):
        self.x -= SPEL_HASTIGHET
        if self.x < -self.width:
            self.x = SKÄRM_BREDD + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    # Rita molnet på skärmen
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


# Klassen för hinder
class Obstacle:
    def __init__(self, image, type):
        # Bild och typ för hindret samt rektangel
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SKÄRM_BREDD

    # Uppdatera hinderets position
    def update(self):
        self.rect.x -= SPEL_HASTIGHET
        if self.rect.x < -self.rect.width:
            hinder.pop()

    # Rita hindret på skärmen
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


# Klassen för små kaktusar
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


# Klassen för stora kaktusar
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


# Klassen för fåglar
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    # Rita fågeln på skärmen
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global SPEL_HASTIGHET, x_axel_marken, y_axel_marken, POÄNG, hinder
    spela = True
    while spela:
        run = True
        clock = pygame.time.Clock()
        player = Dinosaur()
        cloud = Cloud()
        SPEL_HASTIGHET = 20
        x_axel_marken = 0
        y_axel_marken = 380
        POÄNG = 0
        font = pygame.font.Font('freesansbold.ttf', 20)
        hinder = []
        death_count = 0

        def score():
            global POÄNG, SPEL_HASTIGHET
            POÄNG += 1
            if POÄNG % 100 == 0:
                SPEL_HASTIGHET += 1

            text = font.render("Points: " + str(POÄNG), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SKÄRM.blit(text, textRect)

        def background():
            global x_axel_marken, y_axel_marken
            image_width = MARKEN.get_width()
            SKÄRM.blit(MARKEN, (x_axel_marken, y_axel_marken))
            SKÄRM.blit(MARKEN, (image_width + x_axel_marken, y_axel_marken))
            if x_axel_marken <= -image_width:
                SKÄRM.blit(MARKEN, (image_width + x_axel_marken, y_axel_marken))
                x_axel_marken = 0
            x_axel_marken -= SPEL_HASTIGHET

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    spela = False  # Sätt spela till False för att avsluta spelet

            SKÄRM.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()

            player.draw(SKÄRM)
            player.update(userInput)

            if len(hinder) == 0:
                if random.randint(0, 2) == 0:
                    hinder.append(SmallCactus(KAKTUS))
                elif random.randint(0, 2) == 1:
                    hinder.append(LargeCactus(STOR_KAKTUS))
                elif random.randint(0, 2) == 2:
                    hinder.append(Bird(FÅGEL))

            for obstacle in hinder:
                obstacle.draw(SKÄRM)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)

            background()

            cloud.draw(SKÄRM)
            cloud.update()

            score()

            clock.tick(30)
            pygame.display.update()

        pygame.quit()  # Avsluta pygame-körningen när spelet är slut

# Funktion för att visa menyn
def menu(death_count):
    global POÄNG
    starta = True
    while starta:
        SKÄRM.fill((255, 255, 255))
        rita = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = rita.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = rita.render("Press any Key to Restart", True, (0, 0, 0))
            score = rita.render("Your Score: " + str(POÄNG), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SKÄRM_BREDD // 2, SKÄRM_HÖJD // 2 + 50)
            SKÄRM.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SKÄRM_BREDD // 2, SKÄRM_HÖJD // 2)
        SKÄRM.blit(text, textRect)
        SKÄRM.blit(SPRINGA[0], (SKÄRM_BREDD // 2 - 20, SKÄRM_HÖJD // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                starta = False
            if event.type == pygame.KEYDOWN:
                main()

# Starta menyn
menu(death_count=0)


