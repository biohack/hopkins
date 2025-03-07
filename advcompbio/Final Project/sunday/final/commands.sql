DROP TABLE IF EXISTS hits;
DROP TABLE IF EXISTS structural;
DROP TABLE IF EXISTS chemical;
DROP TABLE IF EXISTS functional;
DROP TABLE IF EXISTS charge;
DROP TABLE IF EXISTS hydrophobic;
DROP TABLE IF EXISTS dayhoff;
DROP TABLE IF EXISTS sneath;

create table hits(
id integer not null primary key auto_increment,
accession varchar(10) not null,
description varchar(30) not null,
length int(10) not null,
keywords varchar(50) null,
species varchar(25) not null,
type varchar(10) null,
version int(5) null,
primary_id int(20) null,
num_of_features int(5) null,
start_pos int(5) not null, 
stop_pos int(5) not null
);

create table structural(
id integer not null primary key auto_increment,
sequence text
);

create table chemical(
id integer not null primary key auto_increment,
sequence text
);

create table functional(
id integer not null primary key auto_increment,
sequence text
);

create table charge(
id integer not null primary key auto_increment,
sequence text
);

create table hydrophobic(
id integer not null primary key auto_increment,
sequence text
);

create table dayhoff(
id integer not null primary key auto_increment,
sequence text
);

create table sneath(
id integer not null primary key auto_increment,
sequence text
);

