# Just adding and joining nodes but no explicit stabilize or fix_finger_table
# predecessor and successor are valid by finger table is stale
add 0
add 1
add 2
add 3
join 1 0
join 2 0
join 3 0
list
show 0
show 1
show 2
show 3
end
