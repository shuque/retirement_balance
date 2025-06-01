## Prompts to Cursor AI

2025-05

I used Cursor AI to generate this program, with mostly no actual code
written by me.

The AI/LLM models configured for use in Cursor were the following:

* claude-3.5-sonnet
* claude-4-opus-thinking
* claude-4-sonnet-thinking
* gemini-2.5-pro-preview-05-06
* gpt-4.1
* gpt-4o
* o3


### Prompts given:


Write a python script that prints estimated retirement balance by year. It should use the argparse module to allow the user to specify the values for current age, final age, current balance, yearly contribution amount, and yearly return.

Show me the example output.

Format the balance value so that all the values on each line are aligned to the right.

Make the script executable.

Running the script with "-h" gives an error. Can you fix that?

Rename the script to retirement_balance.py

Run pylint on the script and fix the warnings.

Add /Library/Frameworks/Python.framework/Versions/3.12/bin to the PATH and try again.

<couldn't fix the trailing WS and NL - asked me to do it>

I've done this.

"#!/usr/bin/env python3" should be on the first line, not after the comment string. Please fix.

Add arguments for retirement age and withdrawal rate. If the retirement age is less than or equal to the final age, then for every year from the retirement age onward, subtract the withdrawal amount from the balance.

Add two more output columns for yearly and monthly withdrawal amounts during the retirement phase.

Stop yearly contribution amounts after retirement age.

Add an argument for tax rate, and a column for monthly after tax amount

Add another argument for withdrawal increase rate, to withdraw more each year to account for inflation.

Can you re-order the calculation so that the balance shown at the starting age is the current balance given to the program?

Change the arguments yearly-return, retirement-return, withdrawal-rate, and tax-rate to use percent values rather than decimals.

Also change withdrawal-increase rate to take percent values.

Preface the output with the summary of the input parameters, 1 per line.

Delete the opening line "Input parameters", and move the line "Retirement Balance Projections" to that location.


