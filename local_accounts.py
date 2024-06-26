"""
Local Accounts
This script creates comma-separated (.csv) files that assist in creating local/temporary accounts for EZproxy and Primo. Use this script when creating accounts for users from special programs that do not have matriculated status but need access to library resources. The script takes a comma-separated (.csv) file with three columns describing users: `first`, `last`, and `email`. It produces several text-based files:
- `special_accounts.csv`: user accounts and passwords for giving to the program coordinator after setting up the accounts
- `ezproxy_accounts.txt`: account information for pasting into the `LocalAccounts.txt` configuration file on the EZproxy server
This script requires Python 3 to run and the `pandas` package. See the `requirements.txt` file.
"""

import pandas as pd
import secrets
import string
import datetime

def main():
    # Read in CSV file from program coordinator
    local = pd.read_csv('/Users/ringsmu/Desktop/local/local.csv')

    # Get user expiration date and info for comment in EZproxy file
    initials = input('Your initials: ').upper()
    program = input('Program name: ')
    expiration_date = input("Enter the program expiration date (YYYY-MM-DD format): ")
    # Ensure date is formatted correctly
    try:
        expiration_date = datetime.datetime(*[ int(num) for num in expiration_date.split("-") ])
    except TypeError as err:
        print("\nPlease enter a valid date in YYYY-MM-DD format.\n")
        raise err
    # Ensure date is in the future
    try:
        assert (expiration_date - datetime.datetime.today()).days >= 0
    except AssertionError as err:
        print("\nPlease ensure the program's expiration date is a future date past tomorrow.\n")
        raise err

    # Use user's email to create a username
    username = lambda row: row.email.split('@')[0]
    local['username'] = local.apply(username, axis=1)

    # Generate passwords for each user
    local['password'] = local.apply(lambda row: password(), axis=1)

    # Add column for expiration date
    expires = lambda row: expiration_date.strftime("%Y-%m-%d")
    local['expires'] = local.apply(expires, axis=1)

    # Create entries for EZproxy local accounts file
    ezproxy = lambda row: row.username + ':' + row.password + ':IfBefore=' + row.expires
    local['ezproxy'] = local.apply(ezproxy, axis=1)

    # Add columns that are standard for all users
    local["campus"] = "STW"
    local["user_group"] = "AFFILIATEZ"
    local["purge"] = local["expires"]
    local["address"] = "Distance Learning"
    local["address_type"] = "school"
    local["email_type"] = "school"

    # CSV file for program coordinator
    coordinator = local[['first', 'last', 'email', 'username', 'password']]
    coordinator.to_csv('/Users/ringsmu/Desktop/local/special_accounts.csv', index=False)
    # Text file for EZproxy
    ezproxy_accounts = local[['ezproxy']]
    new_heading = columns = '# ' + program + ' ' + datetime.datetime.today().strftime("%Y-%m-%d") + \
                               ' ' + '(' + initials + ')'
    ezproxy_accounts = ezproxy_accounts.rename(columns={'ezproxy': new_heading})
    ezproxy_accounts.to_csv('/Users/ringsmu/Desktop/local/ezproxy_accounts.txt', index=False)   

def password():
    '''
    Generate a 14-digit passwords with at least one of the following:
    upper-case letter, lower-case letter, and number.
    See this article: 
    https://medium.com/better-programming/best-practices-for-generating-secure-passwords-and-tokens-in-python-ebb91d459267
    '''
    # Do not allow the following characters: 0, o, O, l, and I
    alphabet = string.ascii_letters.replace('o', '')\
                                   .replace('O', '')\
                                   .replace('0', '')\
                                   .replace('l', '')\
                                   .replace('I', '') + (string.digits * 2).replace('0', '')\
                                                                          .replace('1', '')
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(14))
        if (any(ch.islower() for ch in password) and \
           any(ch.isupper() for ch in password) and \
           any(ch.isdigit() for ch in password)):
            break
    return(password)

if __name__ == '__main__':
    main()