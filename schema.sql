create table if not exists blacklist(
    id integer PRIMARY key autoincrement,
    idcard string not null UNIQUE ,
    name string not null,
    mac string not null,
    imsi string not null,
    imei string not null,
    passport string not null
);
create table if not exists blacklist3suo(
  id integer PRIMARY key autoincrement,
  idcard string unique
);
create table if not exists blacklist_helu(
  id INTEGER primary key autoincrement,
  idcard string unique
);
create table if not exists blacklist_jcz(
  id integer primary key autoincrement,
  idcard string unique
);
create table if not exists person(
  idcard string primary key UNIQUE,
  name string,
  sex string,
  birthday integer,
  nationality string,
  nation string,
  address string,
  passport_type string,
  passport_id string,
  score FLOAT,
  image string
);
create table if not exists idlist(
  idcard string primary key unique,
  name string,
  img string
);
