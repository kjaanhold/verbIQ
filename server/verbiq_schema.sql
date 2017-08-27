drop table if exists children;
create table children (
	id_child serial primary key,
	first_name text,
	last_name text,
	date_of_birth date,
	gender text
);

drop table if exists names;
create table names (
	name text
);

drop table if exists users;
create table users (
	id_user serial primary key,
	entity_type text,
	key_entity text,
	language text
);

drop table if exists parents;
create table parents (
	id_parent serial primary key,
	messenger_user_id text,
	first_name text,
	last_name text
);

drop table if exists families;
create table families (
	id_family serial primary key,
	messenger_user_id text,
	first_name text,
	last_name text
);

drop table if exists milestones;
create table milestones (
	id_milestone serial primary key,
	target_age numeric,
	type text,
	description text
);

drop table if exists test_blocks;
create table test_blocks (
	id_test_block serial primary key,
	key_test text,
	block_name text
);

drop table if exists tests;
create table tests (
	id_test serial primary key,
	channel text,
	block_name text	,
	description text,
	follow_up_question text
);

drop table if exists test_results;
create table test_results (
	id_test_result serial primary key,
	key_test integer,
	key_user integer,
	key_child  integer,
	lapse_eesnimi text,
	date_created date,
	result_type text,
	result_value text
);

drop table if exists milestone_tests;
create table milestone_tests (
	id_milestone_test serial primary key,
	key_test integer,
	key_milestone integer
);