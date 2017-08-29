select r.id as region_id, r.name as region_name, count(*) as region_count
from regions r
join comments c on (c.region_id=r.id)
group by r.id, r.name
having count(*) > :stat_count
order by region_name;