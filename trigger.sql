use guliguli;

DELIMITER //

drop trigger if exists t_before_del_on_users;
create trigger t_before_del_on_users
before delete on users
for each row
begin
    delete from comment
    where comment.userid = old.userid;
    delete from relationship
    where relationship.userid1 = old.userid or  relationship.userid2 = old.userid;
    delete from works
    where works.userid = old.userid;
end;

//