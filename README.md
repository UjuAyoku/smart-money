# Compound Interest Calculator

Imagine you just took out a loan to purchase a house. The compound interest for your loan will grow exponentially, not quadratically or geometrically.

For example, if you bought a home that cost $500,000 with a 3.0% interest rate (where interest is applied once per month) for a term of 25 years, you would pay $1,057,509.78 assuming your interest rate is fixed for the 30-year duration.
That is more than double the original amount — just from interest.

This Flask web app calculates the compound interest on a loan or investment based on user inputs: principal amount, interest rate, term (years), and compounds per year.


## Demo

Try it live here:  [Compound Interest Calculator](https://compound-interest-calculator.up.railway.app/)


## Features

- Calculate total amount paid including compound interest
- Calculate total interest paid
- Supports custom principal, interest rate (up to 4 decimals), loan term, and compounding frequency
- User-friendly interface with input validation
- Responsive design using Tailwind CSS


## How to Use

1. Enter the **Principal** (loan or investment amount)
2. Enter the **Rate** as a decimal (e.g., 0.0675 for 6.75%)
3. Enter the **Term** in years
4. Enter the number of **Compounds per Year** (e.g., 12 for monthly compounding)
5. Click **Calculate** to see the total paid and interest paid


## Technologies Used

- Python 3
- Flask
- Tailwind CSS
- Railway for hosting and deployment


## Development

To run locally:

```bash
pip install flask
python app.py
