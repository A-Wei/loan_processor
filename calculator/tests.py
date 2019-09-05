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

    def test_new_payment(self):
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


    def test_get_balance(self):
        resp = self.client.get(
            "/api/v1/get_balance/?request_date=2019-10-11",
            content_type="application/json",
        )
        msg = '{"Remaining Amount":40219.17808219178}'

        self.assertEqual(resp.content.decode("utf-8"), msg)

if __name__ == '__main__':
    unittest.main()
