import unittest
import requests
from django.test import TestCase, Client

class New_Loan_Test(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.initialized_loan = self.client.post(
            "/api/v1/new_loan/",
            data={
                "amount" : 40000,
                "interest_rate": 0.05,
                "start_date": "2019-09-01"
            },
            content_type="application/json",
        )

    def test_initialize_loan(self):
        msg = """{"message":"new loan initiated"}"""

        self.assertEqual(self.initialized_loan.content.decode("utf-8"), msg)

    def test_new_payment_success(self):
        data = {
        	"payment": 10000,
	        "payment_date": "2019-10-10"
        }
        resp = self.client.post(
            "/api/v1/new_payment/",
            data=data,
            content_type="application/json",
        )
        msg = '{"message":"payment successfull"}'

        self.assertEqual(resp.content.decode("utf-8"), msg)

    def test_new_payment_date_earlier_than_loan_start_date(self):
        data = {
        	"payment": 10000,
	        "payment_date": "2019-08-10"
        }
        resp = self.client.post(
            "/api/v1/new_payment/",
            data=data,
            content_type="application/json",
        )
        msg = '{"error":"Date is earlier than loan start date!"}'

        self.assertEqual(resp.content.decode("utf-8"), msg)

    def test_new_payment_amount_exceed_remaining_amount(self):
        data = {
        	"payment": 50000,
	        "payment_date": "2019-09-10"
        }
        resp = self.client.post(
            "/api/v1/new_payment/",
            data=data,
            content_type="application/json",
        )
        msg = '{"error":"Payment amount exceeds remaining amount!"}'

        self.assertEqual(resp.content.decode("utf-8"), msg)


    def test_get_balance(self):
        resp = self.client.get(
            "/api/v1/get_balance/?request_date=2019-10-11",
            content_type="application/json",
        )
        msg = '{"Remaining Amount":40219.18}'

        self.assertEqual(resp.content.decode("utf-8"), msg)

    def test_get_balance_deduct_past_payment(self):
        data = {
        	"payment": 10000,
	        "payment_date": "2019-09-10"
        }
        self.client.post(
            "/api/v1/new_payment/",
            data=data,
            content_type="application/json",
        )
        resp = self.client.get(
            "/api/v1/get_balance/?request_date=2019-10-11",
            content_type="application/json",
        )
        msg = '{"Remaining Amount":30219.18}'

        self.assertEqual(resp.content.decode("utf-8"), msg)

    def test_get_balance_do_not_deduct_future_payment(self):
        data = {
        	"payment": 10000,
	        "payment_date": "2020-09-10"
        }
        self.client.post(
            "/api/v1/new_payment/",
            data=data,
            content_type="application/json",
        )
        resp = self.client.get(
            "/api/v1/get_balance/?request_date=2019-10-11",
            content_type="application/json",
        )
        msg = '{"Remaining Amount":40219.18}'

        self.assertEqual(resp.content.decode("utf-8"), msg)

if __name__ == '__main__':
    unittest.main()
