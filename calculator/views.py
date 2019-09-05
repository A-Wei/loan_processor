from django.shortcuts import render
from rest_framework.decorators import api_view
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status

current_loan_obj = None


# Create your views here.
class Calculator():
    def __init__(self, initial_amount, interest_rate, start_date):
        self.principal_amount = initial_amount
        self.interest_rate = interest_rate
        self.daily_interest_rate = float(interest_rate/365.0)
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.total_amount_paid = 0
        self.interest_amount = 0
        self.payment_records = []

    def add_payment(self, amount, payment_date):
        try:
            # import ipdb; ipdb.set_trace()
            if self.get_balance(payment_date) < amount:
                return "Amount exceeds remaining amount!"
            self.total_amount_paid += amount
            payment_date_obj = datetime.strptime(payment_date, "%Y-%m-%d")
            self.payment_records.append((payment_date_obj, amount))
            self.payment_records.sort()
            return "Success"
        except Exception as e:
            print(str(e))
            return str(e)

    def get_balance(self, given_date):
        try:
            given_date = datetime.strptime(given_date, "%Y-%m-%d")
            if given_date < self.start_date:
                print("Exception : Requested date is earlier than start date")
                raise Exception("Requested date is earlier than start date!")
            elif len(self.payment_records) == 0 or given_date > self.payment_records[-1][0]:
                days_passed = (given_date - self.start_date).days
                interest_amount = float(self.principal_amount * self.daily_interest_rate) * days_passed
                total_payable = self.principal_amount + interest_amount
                print(total_payable)
                # total_amount_paid = payments.filter
                remaining_balance = total_payable - self.total_amount_paid
                return remaining_balance
            else:
                payment_sum = 0
                days_passed = (given_date - self.start_date).days
                interest_amount = float(self.principal_amount * self.daily_interest_rate) * days_passed
                total_payable = self.principal_amount + interest_amount
                for payment in self.payment_records:
                    if payment[0] <= given_date:
                        payment_sum += payment[1]
                remaining_balance = total_payable - payment_sum
                return remaining_balance
        except Exception as e:
            return str(e)


# initial new loan
@api_view(["POST"])
def new_loan(request):
    principal_amount = request.data["amount"]
    interest_rate = request.data["interest_rate"]
    loan_date = request.data["start_date"]

    global current_loan_obj
    current_loan_obj = Calculator(principal_amount, interest_rate, loan_date)

    return Response({"message":"new loan initiated"})

@api_view(["POST"])
def new_payment(request):
    if current_loan_obj is not None:
        payment = request.data["payment"]
        payment_date = request.data["payment_date"]
        payment_status = current_loan_obj.add_payment(payment, payment_date)
        if payment_status == "Success":
            return Response({"message":"payment successfull"})
        else:
            return Response({"error": payment_status}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Loan not initialized!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_balance(request):
    if current_loan_obj is not None:
        request_date = request.GET.get("request_date", None)
        balance = current_loan_obj.get_balance(request_date)
        return Response({"Remaining Amount": balance})
    else:
        return Response({"error": "Loan not initialized!"}, status=status.HTTP_400_BAD_REQUEST)
