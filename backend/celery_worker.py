# this file is for the celery worker: it handles the task through the celery broker

# the code below will integrate the celery worker with the flask app so that celery tasks can asscess the flask app(database, configurations, models etc)




from celery import Celery , Task
from celery.schedules import crontab         #     used later with Celery Beat to schedule periodic jobs

from app import app    # to connect the app_context




celery_app = Celery('tasks', broker = 'redis://localhost:6379/1', backend = 'redis://localhost:6379/2', include = ['tasks'])       #creates a celery app and task is base class for creating custom tasks.




from celery import Celery, Task          #code from the https://flask.palletsprojects.com/en/stable/patterns/celery/


class FlaskTask(Task):
    def __call__(self, *args: object, **kwargs: object):             #This method runs every time a Celery task executes
        with app.app_context():                                      #push flask app contet
            return self.run(*args, **kwargs)




celery_app.Task = FlaskTask               # this will replace the celery task (fThat means every task automatically gets Flask's application context)


celery_app.conf.timezone = 'Asia/Kolkata'       # IST

# celery beat : fro periodic tasks

celery_app.conf.beat_schedule = {
    
    'monthly-user-report' : {           #beat scheduled task name
        'task' : 'tasks.send_monthly_user_report',            #send_monthly_user_report is the function name
        'schedule' : crontab(hour = 18, day_of_month = 13, minute = 40),
    },

    'daily-reminder' : {
        'task' : 'tasks.send_daily_reminder',
        'schedule' : crontab(hour = 18, minute = 40),
    }
}