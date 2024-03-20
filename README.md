# Project: Build A Cloud Data Warehouse On AWS RedShift

This project builds an **ELT pipeline** that extracts data from **S3**, stages them in **Redshift**, and transforms data into a set of **dimensional tables** for Sparkify analytics team to continue finding insights in what songs their users are listening to.

## Problem statement

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Usage
### Configuration

To use the SDK notebooks, you'll have to create access keys for AWS. If these keys are unavailable, you can manually create these assets via the AWS Management Console. Once these assets are available, complete the information for your Redshift cluster and IAM-Role that can manage your cluster and read S3 buckets.

### ETL pipeline instructions

Once your Redshift cluster is created, ensure you have the appropriate virtual environment set-up and activated. Then, run the following commands in the terminal.

To create the tables in Redshift cluster
```
python create_tables.py
```
To load the data into the Redshift cluster
```
python etl.py
```

## Project Structure

```
Cloud Data Warehouse
|____my_create_tables.py    # database/table creation script 
|____my_etl.py              # ELT builder
|____my_sql_queries.py      # SQL query collections
|____dwh.cfg             # AWS configuration file
|____test.ipynb          # testing by running analytics 
```


## ELT Pipeline
### etl.py
ELT pipeline builder

1. `load_staging_tables`
	* Load raw data from S3 buckets to Redshift staging tables
2. `insert_tables`
	* Transform staging table data to dimensional tables for data analysis

### create_tables.py
Creating Staging, Fact and Dimension table schema

1. `drop_tables`
2. `create_tables`

### sql_queries.py
SQL query statement collecitons for `create_tables.py` and `etl.py`

1. `*_table_drop`
2. `*_table_create`
3. `staging_*_copy`
3. `*_table_insert`


## Database Schema
### Staging tables
```
staging_events
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender CHAR(1),
    itemInSession INT,
    lastName VARCHAR,
    length FLOAT,
    level VARCHAR,
    location TEXT,
    method VARCHAR,
    page VARCHAR,
    registration VARCHAR,
    sessionId INT,
    song VARCHAR,
    status INT,
    ts BIGINT,
    userAgent TEXT,
    userId INT

staging_songs
    artist_id VARCHAR,
    artist_latitude FLOAT,
    artist_location TEXT,
    artist_longitude FLOAT,
    artist_name VARCHAR,
    duration FLOAT,
    num_songs INT,
    song_id VARCHAR,
    title VARCHAR,
    year INT
```

### Fact table
```
songplays
    songplay_id INT IDENTITY(0,1),
    start_time TIMESTAMP,
    user_id INT,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT,
    location TEXT,
    user_agent TEXT
```

### Dimension tables
```
users
    user_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR(1),
    level VARCHAR

songs
    song_id VARCHAR,
    title VARCHAR,
    artist_id VARCHAR,
    year INT,
    duration FLOAT

artists
    artist_id VARCHAR,
    name VARCHAR,
    location TEXT ,
    latitude FLOAT ,
    longitude FLOAT

time
    start_time TIMESTAMP,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday VARCHAR
```

### Solution discussion

Sparkify, a music streaming startup, has been amassing significant amounts of user activity and song metadata. This information, currently stored as JSON logs in an S3 bucket, is immensely valuable for gaining insights into user behavior and preferences, which in turn can drive key business decisions.

1. Structured Data: Raw logs and metadata often contain a lot of extraneous information that is not immediately useful for analysis. By extracting the data from S3 and staging in Redshift, we can start structuring this data and filter out the noise.

2. Insights and Analytics: Sparkify's ultimate goal is to understand user behavior. The analytics team will be able to query these tables to answer questions such as:

- What songs are users listening to the most?
- What artists are trending?
- How are different user demographics interacting with the app?
- What are the peak times for usage?

3. Scalability and Performance: Redshift is designed for high-performance analysis and can handle large volumes of data. As Sparkify grows, the data volume will grow as well. Redshift can scale quickly to accommodate this growth, ensuring the data engineering and analytics operations can keep up with the expanding user base and data size.

Overall, the goal of this database solution should be to optimize Sparkify's data for analysis, allowing the company to derive insights that could drive business growth, user engagement, and user experience improvements.

### Database Schema Design

I've proposed a star schema for the database design, centered around the songplays table as the fact table. This design decision was based on the needs of the analysis team and the nature of the questions they'll be asking.

The fact table contains the records in a log of song plays, which is the core focus of Sparkify's analysis efforts, and keys to the four dimension tables: users, songs, artists, and time. By organizing our data this way, we ensure that:

- It's simple to understand: Even those with a modest understanding of the database will be able to make sense of the model and write effective queries.
- It's optimized for aggregation: The star schema is excellent for handling common analytical operations, like COUNT, SUM, AVG, MIN, MAX, etc., which are central to your business queries.
- It's fast: The star schema reduces the number of joins required to answer a query, which greatly improves query performance.
  
The four dimension tables have been chosen to provide additional context to the facts recorded in songplays.

### ETL Pipeline

Our ETL pipeline has been designed to automate the data flow from raw logs in the S3 bucket to structured, queryable tables in Redshift. The pipeline is constructed as follows:

1. Extract data from Sparkify's S3 bucket: This is the source of Sparkify's raw JSON logs for user activity and song metadata.
2. Stage the extracted data in Redshift: The data is loaded into staging tables in Redshift, enabling fast, SQL-based analysis. Staging the data in Redshift also provides a buffer to Sparkify's raw data and adds an extra layer of security.
3. Transform and Load data into dimensional and fact tables: This involves transforming the data into a suitable format for the star schema and then loading it into our fact and dimension tables. Redshift's columnar storage and massively parallel processing (MPP) architecture ensure this process is fast, even with a growing volume of data.

This ETL pipeline is effective because it automates the transformation of raw, semi-structured data into a structured, analyzable format. Furthermore, it's designed with scalability in mind, ensuring Sparkify can continue to obtain the same high-quality insights as Sparkify's user base grows.
