/* 插入五个板块 */

call insert_plate("手绘");
call insert_plate("板绘");
call insert_plate("PS");
call insert_plate("厚涂");
call insert_plate("水彩");

INSERT INTO
manager(username, password)
VALUES('admin', 'ea1891b266fa569efb8852199e40a57c');

call insert_user('malxi', '96e79218965eb72c92a549dd5a330112', 'malxi', '/static/image/no_photo.png', '2004/3/13', '2017/12/26', '呵呵', 0, 0, 'male');
call insert_user('luocaodan', 'e10adc3949ba59abbe56e057f20f883e', 'luocaodan', '/static/image/no_photo.png', '2010/3/13', '2017/12/26', '好啊好啊', 0, 0, 'male');