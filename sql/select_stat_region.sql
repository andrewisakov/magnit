select v.id as village_id, v.name as village_name, count(*) as village_count
from villages v
join comments c on (c.village_id=v.id)
where v.region_id=:region_id
group by v.id, v.name
having count(*) > :stat_count
order by village_name;