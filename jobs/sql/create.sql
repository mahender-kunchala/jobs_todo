drop table if exists openings;
drop table if exists job_status;
drop table if exists crawl_status;

create table crawl_status(
       crawled_on timestamp);
create table job_status (
       id serial primary key,
       name text,
       flag boolean
);


insert into job_status(name,flag) values('crawled',FALSE);
insert into job_status(name,flag) values('applied',FALSE);
insert into job_status(name,flag) values('ignored',FALSE);
insert into job_status(name,flag) values('selected',FALSE);
insert into job_status(name,flag) values('rejected',FALSE);

create table openings (
       id serial primary key,
       title text,
       job_id text,
       company_name text,
       jd_text text,
       jd_url text,
       status serial references job_status(id),
       crawled_on date


);

