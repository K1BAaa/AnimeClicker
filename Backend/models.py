from copy import copy
from django.db import models
from django.contrib.auth.models import User
from .constants import BOOST_TYPE_CHOICES, BOOST_TYPE_VALUES


class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def update_coins(self, coins, commit=True):
        self.coins = coins
        is_level_updated = self.is_levelup()
        boost_type = 0
        if is_level_updated:
            self.level += 1
            if self.level % 3 == 0:
                boost_type = 1
        if commit:
            self.save()
        return is_level_updated, boost_type

    def is_levelup(self):
        return self.coins >= self.calculate_next_level()

    def calculate_next_level(self):
        return (self.level ** 2) * 10 * self.level


class Boost(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    power = models.IntegerField(default=1)
    type = models.PositiveSmallIntegerField(default=0, choices=BOOST_TYPE_CHOICES)

    def levelup(self, coins):
        if coins < self.price:
            return False

        old_boost_values = copy(self)

        self.core.coins = coins - self.price
        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type]['click_power_scale']
        self.core.auto_click_power += self.power * BOOST_TYPE_VALUES[self.type]['auto_click_power_scale']
        self.core.save()

        self.level += 1
        self.power *= 2
        self.price *= self.price * BOOST_TYPE_VALUES[self.type]['price_scale']
        self.save()

        return old_boost_values, self
