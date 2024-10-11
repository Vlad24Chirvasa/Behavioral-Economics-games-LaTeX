from otree.api import *
from datetime import datetime
import random

doc="""
Individual game. The player has to choose between goods. 
For each good there are attributes put in a matrix.
Each player has to choose what cell to open in order to find out
the attribute.
He can choose bewtween the goods at any time, idependently of
the attributes he has seen about a good.  
"""

# MODELS

class C(BaseConstants):
    NAME_IN_URL = 'adam_game_thermometer_guided'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 8

    """All players have to choose between the same goods."""
    """Computer, Headphones, Cellphone"""
    """Attributes: image, price, guarantee"""

    COMPUTER_IMAGE = 'choosing_attributes/computer.jpg'
    HEADPHONES_IMAGE = 'choosing_attributes/headphones.jpg'
    CELLPHONE_IMAGE = 'choosing_attributes/cellphone.jpg'
    QUESTION_IMAGE = 'choosing_attributes/question.jpg'
    COMPUTER_PRICE = 1199.99
    HEADPHONES_PRICE = 299.99
    CELLPHONE_PRICE = 899.99
    
    COMPUTER_GUARANTEE = 2
    HEADPHONES_GUARANTEE = 1 
    CELLPHONE_GUARANTEE = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    goods_choice = models.StringField(initial='')
    # Stores the likes for every good.
    like = models.StringField(initial='')
    # Which good has been liked whether 1, 2, or 3.
    like_order = models.StringField(initial='')
    # Recording the time of giving a like.
    time_stamp = models.StringField(initial='')
    # Boxes already opened.
    boxes_opened = models.StringField(initial='')
    # Satisfaction with your choices.
    satisfaction = models.IntegerField(
        label="How much satisfied are you with the choice made?",
        choices= [
            [0, 'I hate'],
            [1, 'I like'],
            [2, 'I love'],
        ],
        widget=widgets.RadioSelectHorizontal,
        )

# FUNCTIONS
def creating_session(subsession: Subsession):
    session = subsession.session
    session.boxes = [str(i) for i in range(2,10)]
    session.next_box = '1'

# PAGES

class Page1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Page2(Page):

    # Variable number of rounds.
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        for i in range(1,4):
            if str(i) in player.goods_choice:
                return upcoming_apps[0]

    @staticmethod
    def live_method(player: Player, data):
        like = data['like']
        # The good which the user has liked.
        good = data['good']
        choice = data['choice']
        current_time = str(datetime.now().time().strftime('%H:%M:%S.%f')[:-4])
        
    
        strings = [str(i) for i in range(0,101)]
        for string in strings:
            if string == like and len(player.like) == 0:
                player.like += like
                if len(player.time_stamp) == 0:
                    player.time_stamp += current_time
                else:
                    player.time_stamp += ',' + current_time
                for i in range(1, 4):
                    if str(i) == good:
                        player.like_order += good
                return {player.id_in_group: dict(error=True,)}
        
        strings = [str(i) for i in range(0,4)]
        for string in strings:
            if choice == string:
                player.goods_choice += choice
                return {player.id_in_group: dict(error=False,)}
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        boxes = session.boxes
        
        if len(boxes) > 1:
            next_box = random.choice(boxes)
            boxes.remove(next_box)
            session.next_box = next_box

class LastPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 8
    
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(last_box = session.boxes[0])
        



page_sequence = [Page1, Page2, LastPage]