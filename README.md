<a id="readme-top"></a>

<div align="center">
  <h1>SmartMoney</h1>
  <h3>Make smarter financial decisions.</h3>
  
[![Live Demo](https://img.shields.io/badge/Try-Live_Demo-green)]()

</div>

When you take out a mortgage or loan, compound interest can dramatically increase the total amount you repay, often far beyond the original principal. Unlike simple interest (which grows linearly), compound interest grows exponentially, meaning even a small rate difference can cost you tens of thousands over time.

Example: A $500,000 Home Loan

| Parameter | Value |
| :--- | :--- |
| **Principal** | $500,000 |
| **Interest Rate** | 3.0% (fixed) |
| **Term** | 25 years |
| **Compounding** | Monthly |
| **Monthly Payment** | $2,371.48 |
| **Total Repaid** | $711,444.00 |
| **→ Interest Paid** | **$211,444.00** (over 42% of the principal!) |

Whether you are borrowing, investing, or buying a home, this app helps you make smarter financial decisions.

## Demo Link

Available on request

## Features
- Calculate the future value of an investment, loan, or mortgage with compound interest.
- Understand the total interest paid over the full term.
- Clean, responsive web interface built with Tailwind CSS.

## Technologies Used

- **Backend:** Python 3, Flask
- **Frontend:** HTML, Tailwind CSS
- **Deployment:** Google Cloud, Railway

## How to Use
1.  Enter the **Principal** amount (the initial sum of money).
2.  Enter the **Annual Interest Rate** (as a percentage).
3.  Set the **Term** (in years).
4.  In the **Compounds per Year:** field, Enter how often interest is applied in a year:
   
    | To Compound: | Enter: |
    | :--- | :--- |
    | Monthly | `12` |
    | Quarterly | `4` |
    | Annually | `1` |
    
5.  (Optional for Loan and Mortgage) Enter the **Monthly Payment** you plan to make.
6.  Click **Calculate** to see the results, including your monthly payment, total repaid, and total interest.

## Development
To run locally:

Follow these steps to run a copy of this project on your local machine.

1.  **Clone the repository**

2.  **(Optional) Create and activate a virtual environment**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Ensure you have a `requirements.txt` file with `Flask` and any other dependencies listed.*

4.  **Run the Flask application**
    ```bash
    python app.py
    ```

5.  **Open your browser** and go to `http://localhost:5000`.

## License

This project is licensed under the MIT License.
