# Adding to case 2 everything is stable and global information is correct
# Drop the first node 0, now no explicit stab or fix_finger_table
add 0
add 1
add 2
add 3
join 1 0
join 2 0
join 3 0
fix 0
fix 1
fix 2
fix 3
show 0
show 1
show 2
show 3
list
drop 0
list
show 1
show 2
show 3
end
