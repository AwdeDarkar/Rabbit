/*
Database Schema
====================================================================================================

For now, the database consists of two tables: predictons and outcomes.

Prediction
    text array in the form 'p0,p1,...,pn'
    text description
    timestamp

Outcome
    prediction id
    integer id of the prediction outcome
    timestamp
*/

drop table predictions;
drop table outcomes;

/*
Columns
    :id: primary key
    :created: timestamp of the creation of this prediction
    :description: description of the event this is predicting; first line is interpreted as name
*/
create table predictions (
    id integer primary key autoincrement,
    created timestamp not null default current_timestamp,
    description text
);

create table probabilities (
    id integer primary key autoincrement,
    pid integer not null,
    probability tinyint not null default 0,
    event text,
    foreign key (pid) references predictions (id)
);

/*
Columns
    :id: primary key
    :oid: id of the probability entry for the outcome that occured
    :created: timestamp of the creation of this prediction
    :description: description of the event this is predicting; first line is interpreted as name
*/
create table outcomes (
    id integer primary key autoincrement,
    pid integer not null,
    oid integer not null,
    created timestamp not null default current_timestamp,
    foreign key (pid) references predictions (id),
    foreign key (oid) references probabilities (id)
);
