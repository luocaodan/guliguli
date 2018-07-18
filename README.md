# guliguli
A place for acger

## 前端工作计划
#### 视图
页面 | 接口
--- | ---
登录 | /login
注册 | /register
首页 | /index
活动页 | /activity
作品页（单个作品） | /works/<worksid>
用户主页 | /auth/space/<userid>
管理员登录 | /auth/adminLogin

#### 动作
动作 | 接口
--- | ---
投稿作品 | /works/post
关注用户 | /auth/api/follow
取消关注 | /auth/api/unfollow
参与活动 | /api/sign_activity
评论作品 | /works/api/postComment
管理员发起活动 | /add_activity
管理员添加板块 | /add_plate

## 后端工作计划（调用存储过程列表）
#### /login
+ login_user 返回昵称、头像、用户id
#### /register
+ find_user 检查用户是否存在
+ register 写入用户信息
#### /index
+ select_works(随机选取24个作品) 返回作品名，作品图，作品id
#### /activity
+ select_activity(随机选取三个活动) 返回活动图
#### /works/<worksid>
+ works 返回作品信息
+ comment 返回评论信息
#### /user/<userid>
+ user 返回用户信息
#### /manage/login
+ login_admin 
#### /post
+ add_works 添加作品信息
#### /follow
+ follow_user
#### /unfollow
+ unfollow_user
#### /sign_activity
+ sign_ac 参加活动
#### /add_comment
+ add_comment 添加评论
#### /add_activity
+ add_activity 添加活动
#### /add_plate
+ add_plate 添加板块

## 板块都有啥
+ 手绘
+ 板绘
+ PS
+ 厚涂
+ 水彩

## 系统功能结构设计图
![系统功能结构设计图](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/%E7%B3%BB%E7%BB%9F%E5%8A%9F%E8%83%BD%E7%BB%93%E6%9E%84%E8%AE%BE%E8%AE%A1.png)
## 数据流图
![数据流图顶层和第0层](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/guliguli%E6%95%B0%E6%8D%AE%E6%B5%81%E5%9B%BE%E9%A1%B6%E5%B1%82%E5%92%8C%E7%AC%AC0%E5%B1%82.png)
![数据流图第1层](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/guliguli%E6%95%B0%E6%8D%AE%E6%B5%81%E5%9B%BE%E7%AC%AC1%E5%B1%82.png)
## E-R图
![ER-图](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/ER-%E5%9B%BE.png)

## schema
```
/*
    创建数据表 users(用户)
*/
create table if not exists users (
    userid int(8) not null auto_increment,
    username varchar(16) not null unique,
    password char(32) not null,
    nickname varchar(16) not null,
    profile_photo varchar(128) not null,         -- 用户头像url
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
```
```
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

```
```
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
```
```
/*
    创建数据表 plate(板块)
*/
create table if not exists plate (
    plateid int(8) not null auto_increment,
    introduction varchar(128) not null,
    primary key(plateid),
    check(plateid > 0)
)default charset=utf8;

```
```
/*
    创建数据表 works(作品表)
*/
create table if not exists works (
    worksid int(8) not null auto_increment,
    userid int(8) not null,
    works_name varchar(128) not null,           -- 作品名
    content varchar(512) not null,              -- 作品描述
    image varchar(512) not null,                 -- 作品图片url
    date_post date not null,
    plateid int(8) not null,
    primary key(worksid),
    foreign key(userid) references users(userid),
    foreign key(plateid) references plate(plateid),
    check(worksid > 0),
    check(userid > 0),
    check(plateid > 0)
)default charset=utf8;
```
```
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
```
```
/*
    创建数据表 activity(活动表)
*/
create table if not exists activity (
    activityid int(8) not null auto_increment,
    content varchar(512) not null,
    date_release date not null,
    image varchar(256) not null,                 -- 作品图片url
    primary key(activityid),
    check(activityid > 0)
)default charset=utf8;
```
```
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
```
## 演示
![1](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/1.png)
![2](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/2.png)
![3](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/3.jpg)
![4](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/4.jpg)
![5](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/5.jpg)
![6](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/6.jpg)
![7](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/7.jpg)
![8](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/8.png)
![9](https://raw.githubusercontent.com/luocaodan/guliguli/master/show/9.png)
