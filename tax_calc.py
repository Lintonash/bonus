from typing import Dict, Tuple
# from numpy import isclose

DEDUCT_RATE = 0.8084
DEDUCT_INTERCEPT = -60926

BIG_DEDUCT_RATE = 0.9856
BIG_DEDUCT_INTERCEPT = -113078


def deduct(income: int) -> float:
    if income <= 600000:
        return income * DEDUCT_RATE + DEDUCT_INTERCEPT
    else:
        return income * BIG_DEDUCT_RATE + BIG_DEDUCT_INTERCEPT


def get_income_tax(x: int, deduct_amount: int = 0) -> float:
    if deduct_amount is None:
        x = deduct(x)
    else:
        x -= deduct_amount
    if x <= 36000:
        return x * 0.03
    elif 36000 < x <= 144000:
        return x * 0.1 - 2520
    elif 144000 < x <= 300000:
        return x * 0.2 - 16920
    elif 300000 < x <= 420000:
        return x * 0.25 - 31920
    elif 420000 < x <= 660000:
        return x * 0.3 - 52920
    elif 660000 < x <= 960000:
        return x * 0.35 - 85920
    elif x > 960000:
        return x * 0.45 - 181920
    else:
        raise ValueError('x must bigger than 0')


def get_bonus_tax(x: int) -> float:
    monthly_x = x / 12
    if monthly_x <= 3000:
        return x * 0.03
    elif 3000 < monthly_x <= 12000:
        return x * 0.1 - 210
    elif 12000 < monthly_x <= 25000:
        return x * 0.2 - 1410
    elif 25000 < monthly_x <= 35000:
        return x * 0.25 - 2660
    elif 35000 < monthly_x <= 55000:
        return x * 0.3 - 4410
    elif 55000 < monthly_x <= 80000:
        return x * 0.35 - 7160
    elif monthly_x > 80000:
        return x * 0.45 - 15160
    else:
        raise ValueError('x must bigger than 0')


def optimize(money_sum: int, precision: int = 1000, deduct_amount: int = 0) -> Tuple[Dict[str, int], int]:
    min_tax = None
    combination = (0, 0)
    for bonus in range(0, money_sum + 1, precision):
        income = money_sum - bonus
        income_tax = get_income_tax(income, deduct_amount=deduct_amount)
        bonus_tax = get_bonus_tax(bonus)
        tax_sum = round(income_tax + bonus_tax, 2)
        if min_tax is None or tax_sum < min_tax:
            min_tax = tax_sum
            combination = {"income": income, "bonus": bonus}
    return combination, min_tax
