# query1

# select	count(store_id), avg(total_score), store_id
# from		api_review r
# join		accounts_profile p
# on			r.user_id = p.id
# 			and p.age >= year(now()) - (age - 1)
# 			and p.age < year(now()) - (age + 8)
#             and p.gender=gender
# group by	store_id
# having		count(store_id) >= 2
# 			and avg(total_score) >= 4
# limit		5;