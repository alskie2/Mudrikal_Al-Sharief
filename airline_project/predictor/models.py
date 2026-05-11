from django.db import models

class Prediction(models.Model):
    # Inputs
    online_boarding     = models.IntegerField()
    inflight_wifi       = models.IntegerField()
    seat_comfort        = models.IntegerField()
    cleanliness         = models.IntegerField()
    travel_class        = models.CharField(max_length=20)
    type_of_travel      = models.CharField(max_length=30)
    flight_distance     = models.IntegerField()
    total_delay         = models.IntegerField()

    # Output
    prediction          = models.CharField(max_length=30)
    predicted_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} — {self.predicted_at.strftime('%Y-%m-%d %H:%M')}"