from locust import HttpUser, task
import random

emails = ["john@simplylift.co", 'invalid@mail.com']
competitions_name = ["Full Classic", "Fall Classic"]
clubs_name = ['Simply Lift', "Iron Temple"]
number_of_places = [-1, 3, 11, 12, 15]


class ProjectPerformancesTest(HttpUser):
    @task
    def index(self):
        response = self.client.get("/")
        assert response.status_code == 200

    @task
    def showSummary(self):
        email = random.choice(emails)
        response = self.client.post("/showSummary", {'email': email})
        assert response.status_code == 200

    @task
    def book(self):
        competition = random.choice(competitions_name).strip()
        club = random.choice(clubs_name).strip()
        response = self.client.get("/book/" + competition + "/" + club)
        assert response.status_code == 200

    @task
    def purchasePlaces(self):
        competition = random.choice(competitions_name)
        club = random.choice(clubs_name)
        places = random.choice(number_of_places)
        response = self.client.post("/purchasePlaces",
                                    {'places': places, 'competition':
                                        competition, 'club': club})
        assert response.status_code == 200

    @task
    def board(self):
        club = random.choice(clubs_name).strip()
        response = self.client.get("/board/" + club )
        assert response.status_code == 200

    @task
    def logout(self):
        response = self.client.get("/logout")
        assert response.status_code == 302

