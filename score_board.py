from pico2d import *
import play_mode


class Score_board:

    def __init__(self):
        self.image = load_image('score_board.png')
        self.player_score_font = load_font('ENCR10B.TTF', 35)
        self.opponent_score_font = load_font('ENCR10B.TTF', 35)
    def update(self):
        pass

    def draw(self):
        self.image.draw(120, 530)
        if play_mode.player_score < 10:
            self.player_score_font.draw(162, 553, str(play_mode.player_score), (255,255,255))
        else:
            self.player_score_font.draw(149, 553, str(play_mode.player_score), (255, 255, 255))

        if play_mode.opponent_score < 10:
            self.opponent_score_font.draw(162, 507, str(play_mode.opponent_score), (255,255,255))
        else:
            self.opponent_score_font.draw(149, 507, str(play_mode.opponent_score), (255, 255, 255))

