# Twits Service
Pull twits from Twitter by Hashtag or Username

## Table of Contents

1. [API](#api)
2. [Run a Development Server](#run_development_server)
3. [Test](#test)

## <a name="api"></a> API

### /hashtags/\<hashtag\>

Description: search twits by the specified hashtag

Method: GET

Headers: None

Query Parameters:

| Parameter   | Requirement | Description                                        |
| ----------- | ----------- | -------------------------------------------------- |
| pages_limit | Optional    | Limit the number of twits in results. (default=10) |

Example Response:

```json
[
    {
        "account": {
            "fullname": "Twitter",
            "href": "/Twitter",
            "id": 783214,
        },
        "date": "2:54 PM - 8 Mar 2018",
        "hashtags": ["#InternationalWomensDay"],
        "likes": 287,
        "replies": 17,
        "retweets": 70,
        "text": "Powerful voices. Inspiring women.\n\n#InternationalWomensDay https://twitter.com/i/moments/971870564246634496"
    },
]
```

### /users/\<user\>

Description: search twits posted by the specified user

Method: GET

Headers: None

Query Parameters:

| Parameter   | Requirement | Description                                        |
| ----------- | ----------- | -------------------------------------------------- |
| pages_limit | Optional    | Limit the number of twits in results. (default=10) |

Example Response:

```json
[
    {
        "account": {
            "fullname": "Twitter",
            "href": "/Twitter",
            "id": 783214,
        },
        "date": "2:54 PM - 8 Mar 2018",
        "hashtags": ["#InternationalWomensDay"],
        "likes": 287,
        "replies": 17,
        "retweets": 70,
        "text": "Powerful voices. Inspiring women.\n\n#InternationalWomensDay https://twitter.com/i/moments/971870564246634496"
    },
]
```

## <a name="run_development_server"></a> Run a Development Server

To start a development server:
1. Create and activate a virtual environment with

```commandline
python3 -m venv .env
source .env/bin/activate
```

2. Install [requirements](requirements.txt)

```commandline
pip install -r requirements.txt
```

3. Start a flask app

```commandline
export FLASK_APP=twits_service/flask_app
flask run
```

## <a name="test"></a> Test

To run unit tests:
1. Create and activate a virtual environment with
```commandline
python3 -m venv .env
source .env/bin/activate
```

2. Install [test-requirements](test-requirements.txt)
```commandline
pip install -r test-requirements.txt
```

3. Run tests with
```commandline
nosetests
```