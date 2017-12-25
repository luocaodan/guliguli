#user
t_query_user_username = u"call query_user_username('{name}')"
t_query_user_userid = u"call query_user_userid({id})"
t_query_countuser_username = u"call query_countuser_username('{name}')"

t_query_alluser = u"call query_alluser()"

t_insert_user = u"call insert_user('{name}', '{pwd}', '{nick}', '{photo}', '{birth}', '{reg_date}', '{signa}', {fol}, {fan}, '{sex}')"

t_update_user = u"call update_user('{id}', '{pwd}', '{nick}', '{photo}', '{birth}', '{reg_date}', '{signa}', {fol}, {fan}, '{sex}')"

t_query_follows = u"call query_follows({id})"
t_query_fans = u"call query_fans({id})"

t_delete_user = u"call delete_user({id})"

#admin
t_query_admin = u"call query_admin('{name}', '{pwd}')"

#relation
t_query_relationship = u"call query_relationship({uid_1}, {uid_2})"
t_insert_follow_user = u"call insert_follow_user({uid_1}, {uid_2}, '{d_follow}')"
t_delete_unfollow_user = u"call delete_unfollow_user({uid_1}, {uid_2})"

#works
t_query_nworks = u"call query_nworks({n})"
t_query_works = u"call query_works({w_id})"

t_insert_works = u"call insert_works({u_id}, '{w_name}', '{cont}', '{img}', '{d_post}', {p_id})"

#activity
t_query_nactivity = u"call query_nactivity({n})"

t_insert_activity = u"call insert_activity('{cont}', '{d_release})"

t_insert_sign_ac = u"call insert_sign_ac({a_id}, {u_id}, '{d_sign}')"

t_query_sign_ac = u"call query_sign_ac({a_id}, {u_id})"

t_delete_sign_ac = u"call delete_sign_ac({a_id}, {u_id})"


#comment
t_query_comment = u"call query_comment({w_id})"

t_insert_comment = u"call insert_comment('{txt}', {w_id}, {u_id}, '{d_post})"

#plate
t_insert_plate = u"call insert_plate('{intro}')"