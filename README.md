# Origin Backend Assignment

This is an API that implements a very simplified version of one part of Origin's "Advice Layer". It is a simple [Flask](http://flask.pocoo.org/) application that applies a risk scoring algorithm, defined by Origin's stakeholders, to some user provided data (previously collected through a form on Origin's website).

The API contains a single endpoint `/risk_profile` to which one can POST a JSON payload containing the answers to some personal information questions—the "user data"—and it will return the risk profile for that user (also in JSON format). The "risk profile" is simply a human readable matching of the user's risk aversion across Origin's insurance lines.

## Structure of the source code

The interesting files to look at are inside the `riskprofiler` folder and the `tests` folder.

- The `riskprofiler/api.py` file contains the code for the actual Flask endpoint.
- The `riskprofiler/risk_policies.py` file contains the code that represents the various policies defined by the stakeholders.
- The `riskprofiler/risk_scoring.py` file contains the code that implements the point-based scoring mechanism under the hood.
- The `riskprofiler/risk_profile_calculator.py` file contains the code that binds many classes together to actually output a Python dictionary that represents the risk profile.

The rest of the files are pretty self-explanatory. There are many things I don't like about this code but I just didn't have the time to finish it. I'm looking forward to having a interesting discussion about them with you!

## How to run

In case you want to run the tests, clone the repo; `cd` into its directory and then: 

    $ pip install -e
    $ export FLASK_ENV=development
    $ export FLASK_APP=riskprofiler
    $ pytest

To see the test coverage report:

    $ coverage run -m pytest
