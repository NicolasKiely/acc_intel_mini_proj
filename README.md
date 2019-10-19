# Python Mini-Project

Runs queries on imdb dataset.


## Project Structure

The application is structured using a simple MVC pattern.

In the model layer, data is represented using SQLAlchemy as the ORM and
backed with sqllite3 by default.

In the controller layer, function arguments are passed as key-value
arguments and abstracted from the view or data source


## Environment Variables

### DB_CONNECTION
Database connection string, defaults to local sqlite file in data.


## Key Project Assumptions

- The entire data set can load into system memory
- The user has full permissions to access and edit the data
- There are no performance requirements to complete tasks quickly


## Input Data

The file 'data/movie_metadata.csv' was downloaded from
[Kaggle](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset/data)
on 2019-10-17 under the Open Database license.
