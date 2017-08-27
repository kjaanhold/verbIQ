## Launch an AWS EC2 instance

In security groups, allow:

* SSH (protocol = TCP, source = My IP, Port range = 22)
* HTTP (protocol = TCP, source = Anywhere, Port range = 80)

## Clone this repo

`git clone https://github.com/kjaanhold/verbIQ.git`

## Run `setup_machine.sh`

## Set up postgresql 
`sudo -i -u postgres psql
ALTER USER postgres WITH ENCRYPTED PASSWORD 'password';`

### Create the DB 
`CREATE DATABASE my_database;`

### Run migrations
`python manage.py db init
python manage.py db migrate
python manage.py db upgrade`

### Add these lines in the beginning of pg_hba.conf
`# TYPE DATABASE USER CIDR-ADDRESS  METHOD
host  all  all 0.0.0.0/0 md5`

### Change postgresql.conf listen_addresses to `'*'`

### Restart postgresql 
`sudo service postgresql restart`
