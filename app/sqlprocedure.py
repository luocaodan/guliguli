#user
t_query_user_username = "call query_user_username('{name}')"
t_query_user_userid = "call query_user_userid({id})"
t_query_countuser_username = "call query_countuser_username('{name}')"

t_insert_user = "call insert_user('{name}', '{pwd}', '{nick}', '{photo}', '{birth}', '{reg_date}', '{signa}', {fol}, {fan}, '{sex}')"

t_update_user = "call update_user('{id}', '{pwd}', '{nick}', '{photo}', '{birth}', '{reg_date}', '{signa}', {fol}, {fan}, '{sex}')"

t_query_follows = "call query_follows({id})"
t_query_fans = "call query_fans({id})"

#relation
t_query_relationship = "call query_relationship({uid_1}, {uid_2})"
t_insert_follow_user = "call insert_follow_user({uid_1}, {uid_2}, '{d_follow}')"
t_delete_unfollow_user = "call delete_unfollow_user({uid_1}, {uid_2})"

#works
t_query_nworks = "call query_nworks({n})"
t_query_works = "call query_works({w_id})"

t_insert_works = "call insert_works({u_id}, '{w_name}', '{cont}', '{img}', '{d_post}', {p_id})"

#activity
t_query_nactivity = "call query_nactivity({n})"

t_insert_activity = "call insert_activity('{cont}', '{d_release})"

t_update_sign_ac = "call update_sign_ac({a_id}, {u_id}, '{d_sign}')"

#comment
t_query_comment = "call query_comment({w_id})"

t_insert_comment = "call insert_comment({c_id}, '{txt}', {w_id}, {u_id}, '{d_post})"

#plate
t_insert_plate = "call insert_plate('{intro}')"