from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from main.forms import TransForm
from main.models import Account


class Main(View):

    form = TransForm()
    template_name = "main/main.html"

    def get(self, request):
        context = {
            'form': self.form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = TransForm(request.POST)
        if form.is_valid():
            user_id = form['user_id'].value()
            balance = Decimal(form.cleaned_data['balance'])
            users_to = form.cleaned_data['users_to']
            account = get_object_or_404(Account, id=user_id)
            if account.balance >= balance:
                inn_list = users_to.split(",")
                chek_users = True
                for inn in inn_list:
                    user = Account.objects.filter(inn=inn.strip())
                    if not user.exists():
                        chek_users = False
                        messages.error(request, f"User with {inn} - INN number is not found!")

                if chek_users:
                    amount = Decimal(balance / len(inn_list))
                    for i in inn_list:
                        user = Account.objects.get(inn=i.strip())
                        user.deposit(amount)
                        account.withdraw(amount)
                        messages.success(request, f"Transfer success to {i}")
            else:
                messages.error(request, "Insufficient funds!")
        return redirect('/')



