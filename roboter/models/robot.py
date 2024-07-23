from roboter.models import ranking
from roboter.views import console

DEFAULT_ROBOT_NAME = 'Robomi'

class Robot(object):

    def __init__(self, name=DEFAULT_ROBOT_NAME, user_name='',
                 speak_color='blue',good_by_color='red'):
        self.name = name
        self.user_name = user_name
        self.speak_color = speak_color
        self.good_by_color = good_by_color

    def hello(self):
        while True:
            template = console.get_template('hello.txt', self.speak_color)
            user_name = input(template.substitute({
                'robot_name': self.name}))
            if user_name:
                self.user_name = user_name.title()
                break

class TouristRobot(Robot):

    def __init__(self,name=DEFAULT_ROBOT_NAME):
        super().__init__(name=name)
        self.ranking_model = ranking.RankingModel()

    def _hello_decorator(func):

        def wrapper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return wrapper

    @_hello_decorator
    def recommend_tourist_spot(self):

        new_recommend_tourist_spot = self.ranking_model.get_most_popular()
        if not new_recommend_tourist_spot:
            return None

        will_recommend_tourist_spot = [new_recommend_tourist_spot]
        while True:
            template = console.get_template('greeting.txt', self.speak_color)
            is_yes = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
                'tourist_spot': new_recommend_tourist_spot
            }))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                break

            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                new_recommend_tourist_spot = self.ranking_model.get_most_popular(
                    not_list=will_recommend_tourist_spot)
                if not new_recommend_tourist_spot:
                    break
                will_recommend_tourist_spot.append(new_recommend_tourist_spot)

    @_hello_decorator
    def ask_user_favorite(self):
        while True:
            template = console.get_template(
                'which_tourist_spot.txt', self.speak_color)
            tourist_spot = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
            }))
            if tourist_spot:
                self.ranking_model.increment(tourist_spot)
                break

    @_hello_decorator
    def thank_you(self):
        template = console.get_template('good_by.txt', self.speak_color)
        print(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
