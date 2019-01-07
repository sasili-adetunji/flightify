from locust import HttpLocust, TaskSet, task
import json
from decouple import config

# def login(l):
#     data = {
#         "email": config('EMAIL'),
#         "password": config('PASSWORD')
#     }
#     l.client.post("/api/v1/auth/token/", data=json.dumps(data))

# def get_flights(l):
#     l.client.get("/api/v1/flights/")


class UserBehavior(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        data = {
            "email": config('EMAIL'),
            "password": config('PASSWORD')
        }
        self.client.post("/api/v1/auth/token/", data=json.dumps(data))

    @task(1)
    def get_flights(self):
        self.client.get("/api/v1/flights/")


    # tasks = {get_flights: 2, login: 2}

    # def on_start(self):
    #     self.client.headers['Content-Type'] = "application/json"
    #     self.client.headers['Authorization'] = "Bearer {}".format(config('TOKEN'))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
