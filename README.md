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
用户主页 | /user/<userid>
管理员登录 | /manage/login

#### 动作
动作 | 接口
--- | ---
投稿作品 | /post
关注用户 | /follow
取消关注 | /unfollow
参与活动 | /sign_activity
评论作品 | /add_comment
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