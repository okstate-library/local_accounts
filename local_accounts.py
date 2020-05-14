import pandas as pd
import secrets
import string
import datetime

def main():
    # Read in CSV file from program coordinator
    local = pd.read_csv('local.csv')

    # Get user expiration date and info for comment in EZproxy file
    initials = input('Your initials: ').upper()
    program = input('Program name: ')
    year = int(input('Year user access ends (four-digit year): '))
    month = int(input('Month user access ends (two-digit month): '))
    day = int(input('Day user access ends (two-digit day): '))

    # Use user's email to create a username
    username = lambda row: row.email.split('@')[0]
    local['username'] = local.apply(username, axis=1)

    # Generate passwords for each user
    local['password'] = local.apply(lambda row: password(), axis=1)

    # Add column for expiration date
    expires = lambda row: datetime.datetime(year, month, day).strftime("%Y-%m-%d")
    local['expires'] = local.apply(expires, axis=1)

    # Create entries for EZproxy local accounts file
    ezproxy = lambda row: row.username + ':' + row.password + ':IfBefore=' + row.expires
    local['ezproxy'] = local.apply(ezproxy, axis=1)

    # CSV file for program coordinator
    coordinator = local[['first', 'last', 'email', 'username', 'password']]
    coordinator.to_csv('special_accounts.csv', index=False)
    # CSV file for Alma
    alma = local[['first', 'last', 'email', 'username', 'password', 'expires']]
    alma.to_csv('alma_accounts.csv', index=False)
    # Text file for EZproxy
    ezproxy_accounts = local[['ezproxy']]
    new_heading = columns = '# ' + program + ' ' + datetime.datetime.today().strftime("%Y-%m-%d") + \
                               ' ' + '(' + initials + ')'
    ezproxy_accounts = ezproxy_accounts.rename(columns={'ezproxy': new_heading})
    ezproxy_accounts.to_csv('ezproxy_accounts.txt', index=False)   

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
                                   .replace('I', '') + (string.digits * 2).replace('0', '')
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(14))
        if (any(ch.islower() for ch in password) and \
           any(ch.isupper() for ch in password) and \
           any(ch.isdigit() for ch in password)):
            break
    return(password)

if __name__ == '__main__':
    main()
