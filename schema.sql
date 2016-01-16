drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null,
  email text not null,
  pw_hash text not null
);

drop table if exists apps;
create table apps (
    appId integer primary key autoincrement,
    name text not null,
    description text not null,
    url text not null,
    imageurl text,
    color text
);
