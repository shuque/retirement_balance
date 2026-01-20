#!/usr/bin/env python3

"""
retirement_balance.py

Estimate retirement balance by year based on user-specified parameters.
"""

import argparse
from typing import List, Tuple

def calculate_retirement_balance(
    current_age: int,
    final_age: int,
    current_balance: float,
    yearly_contribution: float,
    yearly_return: float,
    retirement_age: int,
    withdrawal_rate: float,
    retirement_return: float,
    tax_rate: float,
    withdrawal_increase: float,
    current_after_tax_balance: float = 0.0,
    yearly_contribution_after_tax: float = 0.0
) -> List[Tuple[int, float, float, float, float, float]]:
    """
    Calculate retirement balance projections for each year.

    Args:
        current_age: Current age of the person
        final_age: Target retirement age
        current_balance: Current total retirement account balance (pre-tax + after-tax)
        yearly_contribution: Amount contributed per year (pre-tax)
        yearly_return: Expected yearly return rate during accumulation (as a percentage)
        retirement_age: Age at which to start withdrawals
        withdrawal_rate: Annual withdrawal rate as a percentage (e.g., 4 for 4%)
        retirement_return: Expected yearly return rate during retirement (as a percentage)
        tax_rate: Tax rate on withdrawals as a percentage (e.g., 22 for 22%)
        withdrawal_increase: Annual increase in withdrawal amount as a percentage (e.g., 2 for 2%)
        current_after_tax_balance: Current Roth (after-tax) account balance
        yearly_contribution_after_tax: Amount contributed per year to Roth (after-tax)

    Returns:
        List of tuples containing (age, balance, withdrawal, after_tax_monthly, pretax_balance, after_tax_balance) for each year
    """
    # Convert percentage rates to decimals
    yearly_return = yearly_return / 100
    retirement_return = retirement_return / 100
    withdrawal_rate = withdrawal_rate / 100
    tax_rate = tax_rate / 100
    withdrawal_increase = withdrawal_increase / 100

    # Separate pre-tax and after-tax balances
    after_tax_balance = current_after_tax_balance
    pretax_balance = current_balance - current_after_tax_balance
    projections = []
    base_withdrawal = 0.0

    for age in range(current_age, final_age + 1):
        # Calculate withdrawal for retirement phase
        withdrawal = 0.0
        after_tax_monthly = 0.0
        total_balance = pretax_balance + after_tax_balance

        if age >= retirement_age:
            if age == retirement_age:
                # Calculate initial withdrawal amount based on total balance
                base_withdrawal = total_balance * withdrawal_rate
            else:
                # Increase withdrawal by inflation rate
                base_withdrawal *= (1 + withdrawal_increase)
            withdrawal = base_withdrawal

            # Calculate proportional withdrawal from each bucket
            if total_balance > 0:
                pretax_ratio = pretax_balance / total_balance
                after_tax_ratio = after_tax_balance / total_balance
            else:
                pretax_ratio = 0
                after_tax_ratio = 0

            pretax_withdrawal = withdrawal * pretax_ratio
            after_tax_withdrawal = withdrawal * after_tax_ratio

            # Only tax the pre-tax portion of withdrawals
            after_tax_monthly = ((pretax_withdrawal * (1 - tax_rate)) + after_tax_withdrawal) / 12

        # Record the balance at the start of the year
        projections.append((age, total_balance, withdrawal, after_tax_monthly, pretax_balance, after_tax_balance))

        # Apply contributions/withdrawals
        if age < retirement_age:
            # Add yearly contributions during accumulation phase
            pretax_balance += yearly_contribution
            after_tax_balance += yearly_contribution_after_tax
        else:
            # Subtract withdrawals during retirement phase (proportionally)
            if total_balance > 0:
                pretax_ratio = pretax_balance / total_balance
                after_tax_ratio = after_tax_balance / total_balance
                pretax_balance -= withdrawal * pretax_ratio
                after_tax_balance -= withdrawal * after_tax_ratio
            else:
                pretax_balance = 0
                after_tax_balance = 0

        # Apply yearly return based on phase (same rate for both buckets)
        if age < retirement_age:
            pretax_balance *= (1 + yearly_return)
            after_tax_balance *= (1 + yearly_return)
        else:
            pretax_balance *= (1 + retirement_return)
            after_tax_balance *= (1 + retirement_return)

    return projections

def main():
    """Parse arguments and print retirement balance projections."""
    parser = argparse.ArgumentParser(
        description='Calculate retirement balance projections'
    )
    parser.add_argument(
        '--current-age',
        type=int,
        required=True,
        metavar='AGE',
        help='Current age'
    )
    parser.add_argument(
        '--final-age',
        type=int,
        required=True,
        metavar='AGE',
        help='Target final age for projections'
    )
    parser.add_argument(
        '--current-balance',
        type=float,
        required=True,
        metavar='AMOUNT',
        help='Current retirement account balance'
    )
    parser.add_argument(
        '--yearly-contribution',
        type=float,
        required=True,
        metavar='AMOUNT',
        help='Amount contributed per year'
    )
    parser.add_argument(
        '--yearly-return',
        type=float,
        required=True,
        metavar='RATE',
        help='Expected yearly return rate during accumulation as a percentage (e.g., 7 for 7%%)'
    )
    parser.add_argument(
        '--retirement-age',
        type=int,
        required=True,
        metavar='AGE',
        help='Age at which to start withdrawals'
    )
    parser.add_argument(
        '--withdrawal-rate',
        type=float,
        required=True,
        metavar='RATE',
        help='Annual withdrawal rate as a percentage (e.g., 4 for 4%%)'
    )
    parser.add_argument(
        '--retirement-return',
        type=float,
        required=True,
        metavar='RATE',
        help='Expected yearly return rate during retirement as a percentage (e.g., 4 for 4%%)'
    )
    parser.add_argument(
        '--tax-rate',
        type=float,
        required=True,
        metavar='RATE',
        help='Tax rate on withdrawals as a percentage (e.g., 22 for 22%%)'
    )
    parser.add_argument(
        '--withdrawal-increase',
        type=float,
        required=True,
        metavar='RATE',
        help='Annual increase in withdrawal amount as a percentage (e.g., 2 for 2%%)'
    )
    parser.add_argument(
        '--current-after-tax-balance',
        type=float,
        default=0.0,
        metavar='AMOUNT',
        help='Current Roth (after-tax) account balance (default: 0)'
    )
    parser.add_argument(
        '--yearly-contribution-after-tax',
        type=float,
        default=0.0,
        metavar='AMOUNT',
        help='Amount contributed per year to Roth (after-tax) accounts (default: 0)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed breakdown of pre-tax and after-tax balances'
    )

    args = parser.parse_args()

    # Validate inputs
    if args.current_age >= args.final_age:
        parser.error("Final age must be greater than current age")
    if args.retirement_age < args.current_age:
        parser.error("Retirement age must be greater than or equal to current age")
    if args.retirement_age > args.final_age:
        parser.error("Retirement age must be less than or equal to final age")
    if args.yearly_return < 0 or args.yearly_return > 100:
        parser.error("Yearly return must be between 0 and 100")
    if args.retirement_return < 0 or args.retirement_return > 100:
        parser.error("Retirement return must be between 0 and 100")
    if args.withdrawal_rate < 0 or args.withdrawal_rate > 100:
        parser.error("Withdrawal rate must be between 0 and 100")
    if args.tax_rate < 0 or args.tax_rate > 100:
        parser.error("Tax rate must be between 0 and 100")
    if args.withdrawal_increase < 0 or args.withdrawal_increase > 100:
        parser.error("Withdrawal increase rate must be between 0 and 100")
    if args.current_after_tax_balance < 0:
        parser.error("Current after-tax balance must be non-negative")
    if args.current_after_tax_balance > args.current_balance:
        parser.error("Current after-tax balance cannot exceed current total balance")
    if args.yearly_contribution_after_tax < 0:
        parser.error("Yearly after-tax contribution must be non-negative")

    # Calculate and display projections
    projections = calculate_retirement_balance(
        args.current_age,
        args.final_age,
        args.current_balance,
        args.yearly_contribution,
        args.yearly_return,
        args.retirement_age,
        args.withdrawal_rate,
        args.retirement_return,
        args.tax_rate,
        args.withdrawal_increase,
        args.current_after_tax_balance,
        args.yearly_contribution_after_tax
    )

    # Print input parameters summary
    print("\nRetirement Balance Projections:")
    print(f"Current Age: {args.current_age}")
    print(f"Final Age: {args.final_age}")
    print(f"Current Balance: ${args.current_balance:,.2f}")
    if args.current_after_tax_balance > 0:
        print(f"  Pre-tax: ${args.current_balance - args.current_after_tax_balance:,.2f}")
        print(f"  After-tax (Roth): ${args.current_after_tax_balance:,.2f}")
    print(f"Yearly Contribution: ${args.yearly_contribution:,.2f}")
    if args.yearly_contribution_after_tax > 0:
        print(f"  Pre-tax: ${args.yearly_contribution:,.2f}")
        print(f"  After-tax (Roth): ${args.yearly_contribution_after_tax:,.2f}")
    print(f"Yearly Return: {args.yearly_return}%")
    print(f"Retirement Age: {args.retirement_age}")
    print(f"Withdrawal Rate: {args.withdrawal_rate}%")
    print(f"Retirement Return: {args.retirement_return}%")
    print(f"Tax Rate: {args.tax_rate}%")
    print(f"Withdrawal Increase: {args.withdrawal_increase}%")

    if args.verbose:
        print(f"\n{'Age':>4}    {'Balance':>15}    {'Pre-Tax':>15}    {'After-Tax':>15}    {'Yearly':>12}    {'Monthly':>12}    {'After Tax':>12}")
        print("-" * 110)
        for age, balance, withdrawal, after_tax_monthly, pretax_balance, aftertax_balance in projections:
            monthly = withdrawal / 12 if withdrawal > 0 else 0
            print(f"{age:4d}    ${balance:>14,.2f}    ${pretax_balance:>14,.2f}    ${aftertax_balance:>14,.2f}    ${withdrawal:>10,.2f}    ${monthly:>10,.2f}    ${after_tax_monthly:>10,.2f}")
    else:
        print(f"\n{'Age':>4}    {'Balance':>15}    {'Yearly':>12}    {'Monthly':>12}    {'After Tax':>12}")
        print("-" * 70)
        for age, balance, withdrawal, after_tax_monthly, pretax_balance, aftertax_balance in projections:
            monthly = withdrawal / 12 if withdrawal > 0 else 0
            print(f"{age:4d}    ${balance:>14,.2f}    ${withdrawal:>10,.2f}    ${monthly:>10,.2f}    ${after_tax_monthly:>10,.2f}")

if __name__ == "__main__":
    main()
