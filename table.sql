/* 
    创建数据库 guliguli
*/
create database if not exists guliguli default charset utf8 collate utf8_general_ci;
-- 选择数据库
use guliguli;
/*
    创建数据表 users(用户)
*/
create table if not exists users (
    userid int(8) not null auto_increment,
    username varchar(16) not null unique,
    password char(32) not null,
    nickname varchar(16) not null,
    profile_photo varchar(32) not null,         -- 用户头像url
    date_birth date not null,
    date_register date not null,
    signature varchar(32) not null,
    follow int(8) not null,
    fans int(8) not null,
    sex varchar(8) not null,
    primary key(userid),
    check(userid > 0),
    check(follow >= 0),
    check(fans >= 0)
)default charset=utf8;

/*
    创建数据表 manager(管理员表)
*/
create table if not exists manager (
    userid int(8) not null auto_increment,
    username varchar(16) not null unique,
    password char(32) not null,
    primary key(userid),
    check(userid > 0)
)default charset=utf8;

/*
    创建数据表 relationship(用户关系表)
*/
create table if not exists relationship (
    userid1 int(8) not null,
    userid2 int(8) not null,
    date_follow date not null,
    primary key(userid1, userid2),
    foreign key(userid1) references users(userid),
    foreign key(userid2) references users(userid),
    check(userid1 > 0),
    check(userid2 > 0)
)default charset=utf8;

/*
    创建数据表 plate(板块)
*/
create table if not exists plate (
    plateid int(8) not null auto_increment,
    introduction varchar(128) not null,
    primary key(plateid),
    check(plateid > 0)
)default charset=utf8;

/*
    创建数据表 works(作品表)
*/
create table if not exists works (
    worksid int(8) not null auto_increment,
    userid int(8) not null,
    works_name varchar(128) not null,           -- 作品名
    content varchar(256) not null,              -- 作品描述
    image varchar(128) not null,                 -- 作品图片url
    date_post date not null,
    plateid int(8) not null,
    primary key(worksid),
    foreign key(userid) references users(userid),
    foreign key(plateid) references plate(plateid),
    check(worksid > 0),
    check(userid > 0),
    check(plateid > 0)
)default charset=utf8;

/*
    创建数据表 comment(评论表)
*/
create table if not exists comment (
    commentid int(8) not null auto_increment,
    text varchar(128) not null,
    worksid int(8) not null,
    userid int(8) not null,
    date_post date not null,
    primary key(commentid),
    foreign key(worksid) references works(worksid),
    foreign key(userid) references users(userid),
    check(worksid > 0),
    check(commentid > 0)
)default charset=utf8;

/*
    创建数据表 activity(活动表)
*/
create table if not exists activity (
    activityid int(8) not null auto_increment,
    content varchar(256) not null,
    date_release date not null,
    primary key(activityid),
    check(activityid > 0)
)default charset=utf8;

/*
    创建数据表 sign_activity(报名活动)
*/
create table if not exists sign_activity (
    activityid int(8) not null,
    userid int(8) not null,
    date_sign date not null,
    primary key(activityid, userid),
    foreign key(activityid) references activity(activityid),
    foreign key(userid) references users(userid),
    check(activityid > 0),
    check(userid > 0)
)default charset=utf8;


/*
    创建数据表 replay(回复)
create table if not exists replay (
    userid int(8) not null,
    commentid int(8) not null,
    text varchar(128) not null,
    date_res date not null,
    primary key(userid, commentid),
    foreign key(userid) references users(userid),
    foreign key(commentid) references comment(commentid)
)default charset=utf8;
*/