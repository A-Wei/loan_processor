# loan_processor
## This is aservice for simulating loan processing that supports the following operations through some network based interface (e.g. rest or graphql):

* Initiate loan: with arguments for initial amount, annual interest rate, and start date.
* Add payment: with arguments for amount and date.
* Get balance: takes a date as an argument and returns the balance of that date.

## Assumptions:
* Get balance can accept a past date, the balance should not include payment made after the given date.
* When the payment amount is greater than balance, it will return an error message.
* Interest is daily basis and always calculated based on initial loan amount.
