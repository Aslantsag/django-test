from decimal import Decimal
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from main.models import Account


class AccountTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='passw1')
        self.user2 = User.objects.create(username='user2', password='passw2')
        self.user3 = User.objects.create(username='user3', password='passw3')
        self.user4 = User.objects.create(username='user4', password='passw4')
        self.account1 = Account.objects.create(user=self.user1, inn='0123456788', balance=1000)
        self.account2 = Account.objects.create(user=self.user2, inn='0123456789', balance=500)
        self.account3 = Account.objects.create(user=self.user3, inn='1123456789', balance=500)
        self.account4 = Account.objects.create(user=self.user4, inn='2123456781', balance=500)

    def test_homepage(self):
        response = self.client.get(reverse('transfer'))
        self.assertEqual(response.status_code, 200)

    def test_transaction1(self):
        test_data = {
            'user_id': self.account1.id,
            'users_to': self.account2.inn,
            'balance': 500,
        }

        self.client.post(reverse('transfer'), data=test_data)
        self.assertEqual(Account.objects.get(user=self.user1).balance, Decimal(500))

    def test_transaction2(self):
        test_data = {
            'user_id': self.account1.id,
            'users_to': "{}, {}, {}".format(self.account2.inn, self.account3.inn, self.account4.inn),
            'balance': 300,
        }

        self.client.post(reverse('transfer'), data=test_data)
        self.assertEqual(Account.objects.get(user=self.user1).balance, Decimal(700))
        self.assertEqual(Account.objects.get(user=self.user2).balance, Decimal(600))
        self.assertEqual(Account.objects.get(user=self.user3).balance, Decimal(600))
        self.assertEqual(Account.objects.get(user=self.user4).balance, Decimal(600))

    def test_transaction3(self):
        test_data = {
            'user_id': self.account1.id,
            'users_to': "{}, {}, {}".format(self.account2.inn, self.account3.inn, self.account4.inn),
            'balance': 1300,
        }

        response = self.client.post(reverse('transfer'), data=test_data)
        msg = list(get_messages(response.wsgi_request))
        self.assertIn(str(msg[0]), 'Insufficient funds!')
        self.assertEqual(Account.objects.get(user=self.user1).balance, Decimal(1000))
        self.assertEqual(Account.objects.get(user=self.user2).balance, Decimal(500))
        self.assertEqual(Account.objects.get(user=self.user3).balance, Decimal(500))
        self.assertEqual(Account.objects.get(user=self.user4).balance, Decimal(500))

    def test_transaction4(self):
        test_inn = '000000000'
        test_data = {
            'user_id': self.account1.id,
            'users_to': "{}, {}, {}".format(test_inn, self.account3.inn, self.account4.inn),
            'balance': 100,
        }

        response = self.client.post(reverse('transfer'), data=test_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(str(messages[0]), f'User with {test_inn} - INN number is not found!')
        self.assertEqual(Account.objects.get(user=self.user1).balance, Decimal(1000))
        self.assertEqual(Account.objects.get(user=self.user2).balance, Decimal(500))
        self.assertEqual(Account.objects.get(user=self.user3).balance, Decimal(500))
        self.assertEqual(Account.objects.get(user=self.user4).balance, Decimal(500))
