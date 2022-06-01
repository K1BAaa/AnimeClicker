from django.db import models
from django.contrib.auth.models import User


class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)

    def click(self, commit=True):
        self.coins += self.click_power
        if commit:
            self.save()
        return self.coins