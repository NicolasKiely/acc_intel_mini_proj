# Python Mini-Project

Runs queries on imdb dataset.


## Usage

cli.py is the main script for driving the application. Run
`python cli.py help`
for general usage.

To load data into a database, run
`python cli.py load-data`.

To rank movie genres by profitability, run
`python cli.py rank-genre [num_genres]`.


## Project Structure

The application is structured using a simple MVC pattern.

In the model layer, data is represented using SQLAlchemy as the ORM and
backed with sqllite3 by default.

In the controller layer, function arguments are passed as key-value
arguments and abstracted from the view or data source.

In the view layer, arguments and data are passed from a user or client,
parsed, invokes controller actions, and returns formatted data.

The data/ directory holds input data, logs, and the database itself.


## Environment Variables

### DB_CONNECTION
Database connection string, defaults to local sqlite file in data.

### DATASET_NAME
Path name to input data set, defaults to "data/movie_metadata.csv".


## Key Project Assumptions

- The entire data set can load into system memory
- The user has full permissions to access and edit the data
- There are no performance requirements to complete tasks quickly
- Any trouble making records should be dropped rather than manually fixed
- The environment has python >=3.6 and is Linux or Unix-Like


## Input Data

The file 'data/movie_metadata.csv' was downloaded from
[Kaggle](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset/data)
on 2019-10-17 under the Open Database license.

Some records (eg with comma in title) may get dropped to avoid problems.
