# Python Mini-Project

Runs queries on imdb dataset.


## Usage

cli.py is the main script for driving the application. Run
`python cli.py help`
for general usage.

To load data into a database, run
`python cli.py load-data`.

To rank movie genres by average profitability, run
`python cli.py rank-genre [num_genres]`.

To rank actors/directors by average profitablity, run
`python cli.py rank-personnel [num_persons]`.


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


## Todo

Given the constraints of time, not all features are implemented yet.

- Implement a small rest service. This would mostly just be a new type of views
using the same controller but returning json responses instead.

- Testing. Unit testing for the business logic and integration/user acceptance
testing for the views. The controller may need to be refactored a bit to be
more friendly to unit testing though.

- More stat queries for actors, movies, and directors.
Maybe a regression model or something fun.

- Load facebook likes for the actors/directors. Right now those fields are
getting dropped.

- Replace the query in rank-personnel with an aggregation query. Right now
the aggregation is done in code, which is very slow as it has to keep loading
the movie records.