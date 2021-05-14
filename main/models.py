from distutils import errors
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activate'),
    ]
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    inn = models.CharField('INN', max_length=12, unique=True)
    balance = models.DecimalField('Balance', max_digits=10, decimal_places=2)
    status = models.CharField(max_length=6, default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount > self.balance:
            raise errors.InsufficientFunds()
        self.balance -= amount
        self.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'User accounts'
