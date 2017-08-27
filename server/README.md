## 1. Launch an AWS EC2 instance and add ssh keys

In security groups, allow:

* SSH (protocol = TCP, source = My IP, Port range = 22)
* HTTP (protocol = TCP, source = Anywhere, Port range = 80)

## 2. Clone this repo

`git clone https://github.com/kjaanhold/verbIQ.git`

## 3. Run `setup_machine.sh`

## 4. Set up postgresql 
`sudo -i -u postgres psql
ALTER USER postgres WITH ENCRYPTED PASSWORD 'password';`

1. Create the DB 
`CREATE DATABASE my_database;`

2. Run migrations
`python manage.py db init`

`python manage.py db migrate`

`python manage.py db upgrade`

3. Add these lines in the beginning of pg_hba.conf
`# TYPE DATABASE USER CIDR-ADDRESS  METHOD
host  all  all 0.0.0.0/0 md5`

4. Change postgresql.conf listen_addresses to `'*'`

5. Restart postgresql 
`sudo service postgresql restart`
