import pygame

from src.interface.menu import MenuStartScreen, MenuOptions
from src.interface import colors


class StartScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        # self.banner = pygame.image.load(
        #     "pac-idol.png"
        # ).convert_alpha()

        self.menu = MenuStartScreen()

    def events(self, events):
        action = self.menu.handle_events(events)

        if action == "Start Game":
            pass

        elif action == "View Highscores":
            self.game.change_screen(HighscoresScreen(self.game))

        elif action == "Instructions":
            self.game.change_screen(InstructionsScreen(self.game))

        elif action == "Options":
            self.game.change_screen(OptionsScreen(self.game))

        elif action == "Exit":
            self.game.running = False

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        # banner_rect = self.banner.get_rect()
        # banner_rect.centerx = screen.get_rect().centerx
        # banner_rect.top = 100

        # screen.blit(self.banner, banner_rect)

        self.menu.draw(screen)


class OptionsScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.menu = MenuOptions()

    def events(self, events):
        action = self.menu.handle_events(events)

        if action == "Back":
            self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)
        self.menu.draw(screen)


class InstructionsScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
        self.back_button = pygame.Rect(100, 900, 100, 60)

    def events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_screen(StartScreen(self.game))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time):
        pass

    def draw_text(self, screen, text, x, y, font):
        text = font.render(text, True, colors.white)
        screen.blit(text, (x, y))

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        self.draw_text(screen, "INSTRUCTIONS", 100, 100, self.title)

        self.draw_text(screen, "Move with the arrow keys", 100, 200, self.font)
        self.draw_text(screen, "Eat the Pac-gums", 100, 240, self.font)
        self.draw_text(screen, "Avoid the ghosts", 100, 280, self.font)
        self.draw_text(screen, "Eat Super Pac-gums", 100, 320, self.font)

        pygame.draw.rect(screen, colors.yellow, self.back_button)

        button_text = self.font.render("Retour", True, colors.black)
        button_text_rect = button_text.get_rect(
            center=self.back_button.center
        )

        screen.blit(button_text, button_text_rect)


class PauseScreen:
    def __init__(self, game):
        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
        # self.background = pygame.image.load(
        #     "background-pause.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        pass

    def events(self, events):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen):
        screen.fill(colors.black)
        # screen.blit(self.background, (0, 0))


class HighscoresScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
        self.back_button = pygame.Rect(100, 900, 100, 60)

        self.rank_x = 150
        self.name_x = 350
        self.score_x = 700

        # self.scores = self.game.highscore.top_score()

        # temp score pour test
        self.scores = [
            ("EMILIE", 12500),
            ("PLAYER2", 10000),
            ("PLAYER3", 8500),
            ("PLAYER4", 7000),
            ("PLAYER5", 6000),
            ("PLAYER6", 5000),
            ("PLAYER7", 4000),
            ("PLAYER8", 3000),
            ("PLAYER9", 2000),
            ("PLAYER10", 1000),
        ]

    def events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_screen(StartScreen(self.game))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time):
        pass

    def draw_text(self, screen, text, x, y, font):
        text = font.render(text, True, colors.white)
        screen.blit(text, (x, y))

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        self.draw_text(screen, "HIGHSCORES", 100, 100, self.title)

        self.draw_text(screen, "RANK", self.rank_x, 200, self.font)
        self.draw_text(screen, "PLAYER", self.name_x, 200, self.font)
        self.draw_text(screen, "SCORE", self.score_x, 200, self.font)

        for i, (name, score) in enumerate(self.scores):
            y = 250 + i * 50

            # name = entry["name"]
            # score = entry["score"]

            # self.draw_text(
            #     screen,
            #     str(i + 1),
            #     self.rank_x,
            #     y,
            #     self.font
            # )

            # self.draw_text(
            #     screen,
            #     name,
            #     self.name_x,
            #     y,
            #     self.font
            # )

            # self.draw_text(
            #     screen,
            #     str(score),
            #     self.score_x,
            #     y,
            #     self.font
            # )

            self.draw_text(screen, str(i + 1), self.rank_x, y, self.font)
            self.draw_text(screen, name, self.name_x, y, self.font)
            self.draw_text(screen, str(score), self.score_x, y, self.font)

        pygame.draw.rect(screen, colors.yellow, self.back_button)

        button_text = self.font.render("Retour", True, colors.black)
        button_text_rect = button_text.get_rect(
            center=self.back_button.center
        )

        screen.blit(button_text, button_text_rect)


class GameOverScreen:

    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_screen(
                        NameInputScreen(self.game)
                    )

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        font = pygame.font.Font(None, 80)

        text = font.render(
            "GAME OVER",
            True,
            colors.white
        )

        rect = text.get_rect(
            center=screen.get_rect().center
        )

        screen.blit(text, rect)


class VictoryScreen:

    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_screen(
                        NameInputScreen(self.game)
                    )

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        font = pygame.font.Font(None, 80)

        text = font.render(
            "VICTORY!",
            True,
            colors.white
        )

        rect = text.get_rect(
            center=screen.get_rect().center
        )

        screen.blit(text, rect)


class NameInputScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.name = ""

    def events(self, events):
        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.name.strip():
                        if self.game.highscore.add_score(
                            self.name.strip(),
                            self.game.score
                        ):
                            self.game.highscore.save_score()

                        self.game.change_screen(
                            HighscoresScreen(self.game)
                        )

                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]

                else:
                    if (
                        len(self.name) < 10
                        and (event.unicode.isalnum() or event.unicode == " ")
                    ):
                        self.name += event.unicode

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        font = pygame.font.Font(None, 50)
        title = pygame.font.Font(None, 70)

        text = title.render(
            "ENTER YOUR NAME",
            True,
            colors.white
        )
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, 250)
        )
        screen.blit(text, text_rect)

        name_text = font.render(
            self.name,
            True,
            colors.white
        )
        name_rect = name_text.get_rect(
            center=(screen.get_width() // 2, 400)
        )
        screen.blit(name_text, name_rect)
