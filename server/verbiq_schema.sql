drop table if exists children;
create table children (
	id_child integer primary key not null,
	first_name text,
	last_name text,
	date_of_birth date,
	gender text
);

drop table if exists users;
create table users (
	id_user integer primary key not null,
	entity_type text,
	key_entity text,
	language text
);

drop table if exists parents;
create table parents (
	id_parent integer primary key not null,
	messenger_user_id text,
	first_name text,
	last_name text
);

drop table if exists families;
create table families (
	id_family integer primary key not null,
	messenger_user_id text,
	first_name text,
	last_name text
);

drop table if exists milestones;
create table milestones (
	id_milestone integer primary key not null,
	target_age text,
	name text,
	description text
);

drop table if exists tests;
create table tests (
	id_test integer primary key not null,
	target_age text not null,
	name text not null,
	description text not null,
	block_name text
);

drop table if exists test_results;
create table test_results (
	id_test_result integer primary key not null,
	key_test integer not null,
	key_user integer not null,
	key_child  integer not null,
	date_created  date not null,
	result_type text,
	result_value text
);

drop table if exists milestone_tests;
create table milestone_tests (
	id_milestone_test integer primary key not null,
	key_test integer not null,
	key_milestone integer not null
);