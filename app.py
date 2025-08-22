from flask import Flask, render_template, request
import locale
import math
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64

import os

app = Flask(__name__)

# Set locale for currency formatting (US)
locale.setlocale(locale.LC_ALL, '')


def calculate_monthly_payment(principal, rate, term):
    '''Calculate amortized monthly payment for loans/mortgages.'''
    monthly_rate = rate / 12
    total_payments = term * 12
    if monthly_rate == 0:  # Handle 0% interest loans
        return principal / total_payments
    return principal * (monthly_rate * (1 + monthly_rate)**total_payments) / ((1 + monthly_rate)**total_payments - 1)

@app.route("/", methods=["GET", "POST"])
def index():
    total = None
    interest = None
    monthly_payment_ = None
    error = None
    payment_message = None  
    amortization_chart = None

    if request.method == "POST":
        try:
            # Initialize calculation variables
            total_value = 0
            interest_value = 0
            monthly_payment = None
            months_needed = None

            # get and validate inputs
            principal = float(request.form.get("principal", ""))
            rate = float(request.form.get("rate", ""))
            term = int(request.form.get("term", ""))
            compound = int(request.form.get("compound", ""))
            mode = request.form.get("mode", "investment")
            monthly_payment = request.form.get("monthly_payment", "") 
            monthly_payment = float(monthly_payment) if monthly_payment else None

            # Convert rate from percentage to decimal
            rate = rate / 100

            #if all(val < 0 for val in [principal, rate, term, compound]):
            if principal <= 0 or rate < 0 or term <= 0 or compound <= 0:
                error = "Principal, term, and compound must be positive. Rate cannot be negative"
            elif mode in ['loan', 'mortgage'] and monthly_payment and monthly_payment <= 0:
                error = "Monthly payment must be positive."
            else:
                if mode == "investment":
                    total_value = principal * (1 + rate / compound) ** (compound * term)
                    interest_value = total_value - principal

                elif mode == "loan":
                    monthly_rate = rate / 12
                    n_payments = term * 12
                    min_required_payment = calculate_monthly_payment(principal, rate, term)

                    if monthly_payment:
                        if monthly_payment < min_required_payment:
                            payment_message = f"${monthly_payment:,.2f} is too small to repay the loan in {term} years. Minimum payment required is ${min_required_payment:,.2f}."
                        else:
                            # Calculate how much is paid with monthly payments (amortization)
                            total_value = monthly_payment * 12 * term
                            interest_value = total_value - principal
                    else:
                        # No payments = unpaid loan, use compound interest
                        total_value = principal * (1 + rate / compound) ** (compound * term)
                        interest_value = total_value - principal

                elif mode == "mortgage":  # with amortization
                    if monthly_payment:
                        monthly_rate = rate / 12
                        if monthly_rate == 0:
                            months_needed = principal / monthly_payment
                        else:
                            try:
                                # Calculate how many months needed to pay off
                                months_needed = math.log(monthly_payment/(monthly_payment - monthly_rate * principal)) / math.log(1 + monthly_rate)
                                
                                # If payment doesn't cover interest, this will raise ValueError
                                years_needed = months_needed / 12
                                
                                if monthly_payment <= principal * monthly_rate:
                                    payment_message = f"Warning: ${monthly_payment:,.2f}/month doesn't cover the interest (minimum payment should be ${principal * monthly_rate:,.2f})"
                                    total_value = float('inf')
                                    interest_value = float('inf')
                                elif years_needed > term:
                                    payment_message = f"Warning: At ${monthly_payment:,.2f}/month, it will take {years_needed:,.1f} years (longer than {term}-year term)"
                                    total_value = monthly_payment * 12 * term
                                    interest_value = total_value - principal
                                else:
                                    payment_message = f"At ${monthly_payment:,.2f}/month, it will take {years_needed:,.1f} years"
                                    total_value = monthly_payment * months_needed
                                    interest_value = total_value - principal
                                    
                            except ValueError:
                                payment_message = f"${monthly_payment:,.2f} monthly payment is too small to cover interest. (Minimum payment is ${principal * monthly_rate:,.2f})"
                                #total_value = float('0.00')
                                #interest_value = float('0.00')
                    else:
                        # auto-calculate monthly payment if not provided
                        monthly_payment = calculate_monthly_payment(principal, rate, term)
                        total_value = monthly_payment * 12 * term
                        interest_value = total_value - principal

                # Inside your main route where monthly_payment is known
                

                if mode in ['mortgage'] and monthly_payment:
                    # Skip chart if payment doesn't cover interest (mortgage) or is too small (loan)
                    if (mode == 'mortgage' and monthly_payment > principal * (rate / 12)) or \
                    (mode == 'loan' and monthly_payment >= calculate_monthly_payment(principal, rate, term)):
                        balance = principal
                        r_monthly = rate / 12
                        n_payments = term * 12

                        balances = []
                        principals = []
                        interests = []
                        months = []

                        for i in range(1, n_payments + 1):
                            interest_paid = balance * r_monthly
                            principal_paid = monthly_payment - interest_paid
                            balance -= principal_paid

                            months.append(i)
                            interests.append(interest_paid)
                            principals.append(principal_paid)
                            balances.append(max(balance, 0))  # avoid small negative due to float error

                        # Plot the graph
                        plt.figure(figsize=(8, 4))
                        plt.stackplot(months, interests, principals, labels=['Interest', 'Principal'], colors=['#f97316', "#C0C2CB"])
                        plt.legend(loc='upper right')
                        plt.title('Interest & Principal Payments')
                        plt.xlabel('Number of Payments')
                        plt.ylabel('Amount ($)')
                        plt.tight_layout()

                        # Save plot to base64 to embed in HTML
                        buf = BytesIO()
                        plt.savefig(buf, format='png')
                        buf.seek(0)
                        chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
                        amortization_chart = f"data:image/png;base64,{chart_base64}"
                        plt.close()

                #else:
                    #total_value = interest_value = 0

                # format results
                total = "${:,.2f}".format(total_value)
                interest = "${:,.2f}".format(interest_value)
                # Only format if monthly_payment exists
                if monthly_payment is not None:
                    monthly_payment_ = "${:,.2f}".format(monthly_payment)

        except (ValueError, ZeroDivisionError):
            # Invalid form values or division by zero
            #total = interest = None
            error = "Invalid input values. Please check your entries."
            total = None
            interest = None
            monthly_payment_ = None
            amortization_chart = None

    return render_template("index.html", 
                           total=total, 
                           interest=interest, 
                           monthly_payment_=monthly_payment_, 
                           payment_message=payment_message, 
                           error=error,
                           amortization_chart=amortization_chart)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
