from otree.api import *

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
    NAME_IN_URL = 'adam_game_heart'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    """All players have to choose between the same goods."""
    """Computer, Headphones, Cellphone"""
    """Attributes: image, price, guarantee"""

    COMPUTER_IMAGE = 'choosing_attributes/computer.jpg'
    HEADPHONES_IMAGE = 'choosing_attributes/headphones.jpg'
    CELLPHONE_IMAGE = 'choosing_attributes/cellphone.jpg'
    QUESTION_IMAGE = 'choosing_attributes/question.jpg'
    EMPTY_HEART = 'choosing_attributes/empty_heart.png'
    FILLED_HEART = 'choosing_attributes/filled_heart.png'

    COMPUTER_PRICE = 1199.99
    HEADPHONES_PRICE = 299.99
    CELLPHONE_PRICE = 899.99
    
    COMPUTER_GUARANTEE = 2
    HEADPHONES_GUARANTEE = 1 
    CELLPHONE_GUARANTEE = 1

    SECONDS = 45

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    goods_choice = models.IntegerField(
        doc="""Choice between three goods.""",
        choices=[0, 1, 2, 3],
        initial=0,
    )
    open_order = models.StringField(initial='')
    open_time = models.StringField(initial='')
    # Stores the degreees of likeness for every good.
    like = models.StringField(initial='')
    # Stores the good as an integer associated with its corresponding like.
    # 1 = headphones, 2 = computer, 3=cellphone
    like_order = models.StringField(initial='')
    # Player goes to the next page
    next = models.BooleanField()
    satisfaction = models.IntegerField(
        label="Now rate how much do you like your choice.",
        choices=[
            [1,"I hate it"],
            [2,"Dislike"],
            [3,"Indiferent"],
            [4,"Like"],
            [5,"I love it"]],
        widget=widgets.RadioSelectHorizontal,
    )


# FUNCTIONS

# PAGES
class Instructions(Page):
    pass

class Page1(Page):
    form_model = 'player'
    form_fields = ['goods_choice']
    timeout_seconds = 200

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.next = True

    @staticmethod
    def vars_for_template(player: Player):
        numbers = [i for i in range(1,10)]
        return dict(numbers=numbers)

    @staticmethod
    def live_method(player: Player, data):
        from datetime import datetime
        current_time = datetime.now().time()
        current_time = str(current_time.strftime('%H:%M:%S.%f')[:-4])
        button = data['button']
        like = data['like']
        
        strings = [str(i) for i in range(1, 10)]
        for string in strings:
            if button == string:
                player.open_order += button
                player.open_time += ', ' + current_time
            if  like == string:
                # One like per box opened
                if len(player.open_order) - 1 >= len(player.like):
                    player.like += like
                    return {player.id_in_group: dict(error=False, empty=True)}
                if not like:
                    player.like += '0'
                if data['headphones'] == True:
                    player.like_order += '1'
                if data['computer'] == True:
                    player.like_order += '2'
                if data['cellphone'] == True:
                    player.like_order += '3'
                else:
                    return {player.id_in_group: dict(error=True)}
                
    

class Page2(Page):
    form_model = 'player'
    form_fields = ['goods_choice']
    timeout_seconds = 160

    @staticmethod
    def is_displayed(player: Player):
        return player.goods_choice == 0

    @staticmethod
    def vars_for_template(player: Player):
        numbers = [i for i in range(1,10)]
        return dict(numbers=numbers)

    @staticmethod
    def live_method(player: Player, data):
        from datetime import datetime
        current_time = datetime.now().time()
        current_time = str(current_time.strftime('%H:%M:%S.%f')[:-4])
        button = data['button']
        like = data['like']
        
        strings = [str(i) for i in range(1, 10)]
        for string in strings:
            if button == string: # and button  not in player.open_order
                player.open_order += button
                player.open_time += ', ' + current_time
            if  like == string:
                # One like per box opened
                if len(player.open_order) - 1 >= len(player.like):
                    player.like += like
                    if data['headphones'] == True:
                        player.like_order += '1'
                    if data['computer'] == True:
                        player.like_order += '2'
                    if data['cellphone'] == True:
                        player.like_order += '3'
                else:
                    return {player.id_in_group: dict(error=True)}
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        if timeout_happened:
            player.goods_choice = random.choice([1, 2, 3])
                
class Satisfaction(Page):
    form_model = 'player'
    form_fields = ['satisfaction']
    
    @staticmethod
    def vars_for_template(player: Player):
        if player.goods_choice == 1:
            return dict(good='headphones')
        if player.goods_choice == 2:
            return dict(good='computer')
        if player.goods_choice == 3:
            return dict(good='cellphone')

page_sequence = [Instructions, Page1, Page2, Satisfaction]