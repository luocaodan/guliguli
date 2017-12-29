/*
    创建存储过程
*/
use guliguli;
delimiter //  -- 改变分隔符

/*
    query_by_username
    传入: 用户名
    根据用户名查找用户
*/
create procedure query_user_username(name varchar(16))
    begin
        select * from users 
        where username=name;
    end//
    
/*
    query_by_id
    传入: 用户id
    根据用户id查找用户
*/
create procedure query_user_userid(id int(8))
    begin
        select * from users 
        where userid=id;
    end//

/*
    query_countuser_username
    传入: 用户名
    检查用户是否存在
*/
create procedure query_countuser_username(name varchar(16))
    begin
        select count(*) from users
        where username=name;
    end//

/*
    insert_user 
    传入: username password nickname profile_photo \
    date_birth date_register signature follow fans
*/
create procedure insert_user(
    name varchar(16), 
    pwd char(32), 
    nick varchar(16),
    photo varchar(32),
    birth date,
    reg_date date,
    signa varchar(32),
    fol int(8),
    fan int(8),
    sex varchar(8)
    )
    begin
       insert into 
       users(username, password, nickname, profile_photo, date_birth, date_register, signature, follow, fans, sex) 
       values(name, pwd, nick, photo, birth, reg_date, signa, fol, fan, sex);
    end//

/*
    update_user 
    传入: password nickname profile_photo \
    date_birth date_register signature follow fans
*/
create procedure update_user(
    u_id int(8),
    pwd char(32), 
    nick varchar(16),
    photo varchar(128),
    birth date,
    reg_date date,
    signa varchar(32),
    fol int(8),
    fan int(8),
    sex varchar(8)
    )
    begin
       update users 
       set password = pwd, nickname=nick, profile_photo=photo, date_register=reg_date, signature=signa, follow=fol, fans=fan, sex=sex
       where userid=u_id;
    end//    

/*
    delete_user
    传入: 用户名
    根据id删除用户
*/
create procedure delete_user(u_id int(8))
    begin
        delete from users 
        where userid=u_id;
    end//

/*
    query_relationship
    传入: 用户1id, 用户2id
    查找用户关注关系
*/
create procedure query_relationship(uid_1 int(8), uid_2 int(8))
    begin
        select * from relationship
        where userid1=uid_1 and userid2=uid_2;
    end//    

/*
    insert_works
    传入: 作品信息
    添加作品信息
*/
create procedure insert_works(
    u_id int(8), 
    w_name varchar(128), 
    cont varchar(512),
    img varchar(512),
    d_post date,
    p_id int(8)
    )
    begin
        insert into
        works(userid, works_name, content, image, date_post, plateid)
        values(u_id, w_name, cont, img, d_post, p_id);
    end//

/*
    query_lastworks
    传入: 无
    查找最新添加的作品
*/
create procedure query_lastworks()
    begin
        select * from works
        order by worksid desc
        limit 1;
    end//

/*
    query_works
    传入: 作品id
    返回作品信息
*/
create procedure query_works(w_id int(8))
    begin
        select * from works
        where worksid=w_id;
    end//

/*
    query_nworks
    传入: n
    首页罗列作品，随机选取作品中的n条记录
*/
create procedure query_nworks(n int) 
    begin
        select * from works
        order by worksid desc 
        limit n;
    end//

/*
    query_usersworks
    传入: 用户id
    个人主页罗列该用户的作品
*/
create procedure query_usersworks(u_id int(8)) 
    begin
        select * from works
        where userid=u_id
        order by worksid desc;
    end//

/*
    query_nactivity
    传入: n
    活动页罗列活动(n个)
*/
create procedure query_nactivity(n int)
    begin
        select * from activity 
        order by activityid desc
        limit n;
    end//

/*
    query_activity
    传入: a_id
    查询活动内容
*/
create procedure query_activity(a_id int(8))
    begin
        select * from activity
        where activityid=a_id;
    end//

/*
    query_comment
    传入: 作品id
    返回评论信息及用户信息
*/
create procedure query_comment(w_id int(8))
    begin
        select commentid, text, worksid, comment.userid, date_post, nickname, profile_photo, sex 
        from comment, users 
        where users.userid = comment.userid and worksid=w_id
        order by commentid desc;
    end//

/*
    insert_comment
    传入: 评论信息
    添加评论
*/
create procedure insert_comment( 
    txt varchar(128), 
    w_id int(8),
    u_id int(8),
    d_post date
    )
    begin
        insert into comment(text, worksid, userid, date_post)
        values(txt, w_id, u_id, d_post);
    end//

/*
    query_follows
    传入: 用户id
    查询关注人
*/
create procedure query_follows(u_id int(8))
    begin
        select * from users
        where userid in (
            select userid2 from relationship
            where userid1=u_id
        );
    end//    

/*
    query_fans
    传入: 用户id
    查询粉丝
*/
create procedure query_fans(u_id int(8))
    begin
        select * from users
        where userid in (
            select userid1 from relationship
            where userid2=u_id
        );
    end//   
     
/*
    insert_follow_user
    传入: 用户1id, 用户2id
    添加关注信息
*/
create procedure insert_follow_user(uid1 int(8), uid2 int(8), d_follow date)
    begin
        insert into
        relationship(userid1, userid2, date_follow)
        values(uid1, uid2, d_follow);
    end//

/*
    delete_unfollow_user
    传入: 用户1id, 用户2id
    删除关注信息
*/
create procedure delete_unfollow_user(uid1 int(8), uid2 int(8))
    begin
        delete from relationship
        where userid1=uid1 and userid2=uid2;
    end//

/*
    insert_activity
    传入: 活动信息
    添加活动信息
*/
create procedure insert_activity(cont varchar(512), d_release date, img varchar(256))
    begin
        insert into activity(content, date_release, image)
        values(cont, d_release, img);
    end//

/*
    insert_sign_ac
    传入: 活动信息
    添加参加活动信息
*/
create procedure insert_sign_ac(a_id int(8), u_id int(8), d_sign date)
    begin
        insert into sign_activity(activityid, userid, date_sign)
        values(a_id, u_id, d_sign);
    end//

/*
    query_sign_ac
    传入: 作品id, 用户id
    查询是否参加活动
*/
create procedure query_sign_ac(a_id int(8), u_id int(8))
    begin
        select count(*) from sign_activity
        where activityid=a_id and userid=u_id;
    end//

/*
    delete_sign_ac
    传入: 作品id, 用户id
    删除参加活动信息
*/
create procedure delete_sign_ac(a_id int(8), u_id int(8))
    begin
        delete from sign_activity
        where activityid=a_id and userid=u_id;
    end//

/*
    insert_plate
    传入: 板块信息
    添加板块信息
*/
create procedure insert_plate(intro varchar(128))
    begin
        insert into plate(introduction)
        values(intro);
    end//

/*
    query_admin
    传入: 用户名和密码
    管理员登录
*/
create procedure query_admin(name varchar(16), pwd char(32))
    begin
        select * from manager
        where username=name and password=pwd;
    end//

delimiter ;