select c.id,
r.name as region_name,
v.name as village_name,
c.user_name,
c.user_last_name,
c.user_email,
c.user_phone,
c.comment,
c.pub_datetime
from comments c
join regions r on (r.id=c.region_id)
join villages v on (v.id=c.village_id)
order by pub_datetime;
