from roboter.models import robot

def talk_about_tourist_spot():

    tourist_robot = robot.TouristRobot()
    tourist_robot.hello()
    tourist_robot.recommend_tourist_spot()
    tourist_robot.ask_user_favorite()
    tourist_robot.thank_you()

