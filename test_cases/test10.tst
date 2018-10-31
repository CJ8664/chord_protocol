# Adding to case 2 everything is stable and global information is correct
# Drop the last two node 3, now explicit stab or fix
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
drop 3
drop 2
list
show 0
show 1
# Stabilize 1 so 0's predecessor is updated
stab 1
fix 1
fix 0
show 0
show 1
end
