# Traders API Documentation

- [User Management](#user-related)
- [Account Management](#account-related)
- [Position Management](#position-related)
- [Exchange Rates Management](#exchange-rates-related)

## User Related

## Users Manipulation [/users]
### Sign up the new user [POST]

+ Request Body (application/json)

        {
            "email": "someone@email.com",
            "username": "someone",
            "password": "somepassword"
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully signed up",
            "user_id": 123
        }

### Delete a user [DELETE]

+ Request Body (application/json)

        {
            "email": "someone@email.com",
            "id": 111
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully deleted a user",
        }

### Get all users [GET]

This API endpoint exists just for testing.

+ Response 200 (application/json)

        {
            "status": true,
            "users": [
                {
                    "email": "someone@email.com",
                    "username": "someone",
                    "user_id": 123,
                    "last_login": 2018-10-10 11:11:11
                },
                {
                    "email": "someoneelse@email.com",
                    "username": "someoneelse",
                    "user_id": 1234,
                    "last_login": 2018-10-10 11:11:11
                }
            ]
        }

## User Sign in [/signin]
### Sign in a user [POST]

+ Request Body (application/json)

        {
            "email": "someone@email.com",
            "password": "somepassword"
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully signed in",
            "user_id": 123,
            "account_ids": [
                123,
                123,
                123
            ]
        }


## Account Related

## New Sub-account Creation [/new_account?uid=<INT>]

### Create a sub-account under a user [POST]

+ Request Body (application/json)

        {
            "account_name": "someaccountname"
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully created a new sub-account",
            "account_id": 321,
        }


## Sub-account [/{user_id}/{account_id}]

### Request account information [GET]

+ Response 200 (application/json)

        {
            "status": true,
            user_id": 123,
            "account_name": "someaccountname",
            "account_id": 321,
            "available_equity": 100000.0
            "account_value": 12345
            "open_date": datetime.datetime(2018, 10, 31, 18, 51, 34), 
            'close_date': None
        }

### Delete account [DELETE]

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully delete the account",
            "deleted_account_name": "someaccountname",
            "close_date": 2018-10-10 24:24:24
        }


## Position Related

## Position Management [/users/{user_id}/accounts/{account_id}/positions]

### Get all positions [GET]
This API lets `from_date`, `to_date`, and `status` to be configured.  If you want to get positions
within specific dates, send request to
`/users/{user_id}/accounts/{account_id}/positions/from/{from_date}/to/{to_date}`.
If you want to get positions within specific dates and with certain status (open or close), make a
request to `/users/{user_id}/accounts/{account_id}/positions/from/{from_date}/to/{to_date}/status/{status}`.
If you want to see positions that are with certain status, make a request to 
`/users/{user_id}/accounts/{account_id}/positions/status/{status}`.

+ Response 200 (application/json)

        {
            "status": true,
            "positions": [
                {
                    "id": 1,
                    "currency_from": "gbp",
                    "currency_to": "usd",
                    "open_rate_id": 1,
                    "open_rate_time": 2018-10-10 11:11:11,
                    "close_rate_id": null,
                    "close_rate_time": null,
                    "position_type": "short",
                    "position_status": "open",
                    "volume": 123.3
                    "value": 12345
                },
                {
                    "id": 1,
                    "currency_from": "gbp",
                    "currency_to": "usd",
                    "open_rate_id": 1,
                    "open_rate_time": 2018-10-10 11:11:11,
                    "close_rate_id": null,
                    "close_rate_time": null,
                    "position_type": "short",
                    "position_status": "open",
                    "volume": 123.3
                    "value": 12345
                }
            ]
        }

### Create a new position [POST]

+ Request Body (application/json)

        {
            "currency_from": "usd",
            "currency_to": "gbp",
            "time": 2018-10-10 11:11:11,
            "position_type": "short",
            "volume": 123.3
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully created a new position",
            "position_id": 4
        }

or

        {
            "status": false,
            "message": "Failed to create a new position",
            "code": 100
        }
Code Representation  
- 100: Insufficient balance
- 200: Unknown error. Possibly invalid exchange rate


## Individual Position [/users/{user_id}/accounts/{account_id}/positions/{position_id}]
## Get the position information [GET]

+ Response 200 (application/json)

        {
            "status": true,
            "position": {
                "id": 2,
                "open_rate_id": 1,
                "close_rate_id": null,
                "position_type": "long",
                "position_status": "open",
                "volume": 123.3
                "value" : 12345 #Updated only on close for now 
            }
        }

## Close the position [PUT]

+ Request Body (application/json)

        {
            "close_rate_time": 2018-10-10 11:11:11,
            "open_rate_id": 1
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully closed position"
        }


## Exchange Rates Related

## Getting Exchange Rate Data [/exchangerates/currency_from/{currency_from}/currency_to/{currency_to}/from_time/{from_time}/to_time/{to_time}]
An API endpoint for getting all the exchange rates that are within `from_time` and `to_time` time frame.  These arguments should be in the format of `year-month-day_hour:minute:second`.  For example, `2018-11-11_11:00:00`.

+ Response 200 (application/json)

        {
            "status": true,
            "currency_from": 'usd',
            "currency_to": 'gbp',
            "from_time": 2018-01-01 11:11:11,
            "to_time": 2018-01-10 11:11:11,
            "exchange_rates": [
                {
                    "id": 0,
                    "bid": 13.0,
                    "ask": 14.0,
                    "time": 2018-01-01 12:00:00
                },
                {
                    "id": 1,
                    "bid": 13.0,
                    "ask": 14.0,
                    "time": 2018-01-02 12:00:00
                },
                {
                    "id": 2,
                    "bid": 13.0,
                    "ask": 14.0,
                    "time": 2018-01-03 12:00:00
                },
            ]
        }
