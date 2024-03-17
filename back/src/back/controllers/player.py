from back.controllers.game import Game


class Player:
    def join_game(self, game: Game):
        game.join(self)
