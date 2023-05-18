from locust import HttpUser, task


class PerfTest(HttpUser):

    @task(6)
    def test_home(self):
        self.client.get("/")

    @task(6)
    def login(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task(6)
    def book(self):
        self.client.get("/book/Fall Classic/Simply Lift")

    @task(6)
    def places_purchase(self):
        self.client.post("/purchasePlaces", {
            "club": "Simply Lift",
            "competition": "Fall Classic",
            "places": "1"
        })

    @task(6)
    def point_summary(self):
        self.client.get("/pointSummary")

    @task(6)
    def logout(self):
        self.client.get("/logout")