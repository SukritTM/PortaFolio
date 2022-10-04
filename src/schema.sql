drop table if exists user;
drop table if exists artwork;

create table user (
	uid integer primary key autoincrement,
	name text not null,
	username text not null,
	email text unique not null,
	password text not null,
	dob text,
	bio text,
	contact text,

	unique(username, email)
);

create table artwork (
	aid integer primary key autoincrement,
	image text not null,
	caption text,
	uid integer not null,
	foreign key (uid) references user (uid)
);