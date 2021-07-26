# local_accounts

This script creates comma-separated (.csv) files that assist in creating local/temporary accounts for EZproxy and Primo. Use this script when creating accounts for users from special programs that do not have matriculated status but need access to library resources. The script takes a comma-separated (.csv) file with three columns describing users: `first`, `last`, and `email`. It produces several text-based files:

- `special_accounts.csv`: user accounts and passwords for giving to the program coordinator after setting up the accounts
- `ezproxy_accounts.txt`: account information for pasting into the `LocalAccounts.txt` configuration file on the EZproxy server
- `alma_accounts.csv`: account information for uploading accounts into Alma/Primo using the CSV uploader tool

This script requires Python 3 to run and the `pandas` package. See the `requirements.txt` file.