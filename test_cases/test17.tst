# Adding to case 2 everything is stable and global information is correct
# Drop one node from middle, now stab and fix to update finger_table
# Now add 1 again and call join, Node 3's finger table will be stale
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
list
drop 1
# drop 2
show 0
show 2
show 3
# Stab 0 will update the No pre for Node 2
stab 0
fix 0
fix 2
fix 3
add 1
join 1 3
show 0
show 2
show 3
end
