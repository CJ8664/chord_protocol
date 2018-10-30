# Adding to case 2 everything is stable and global information is correct
# Drop the last node 3, now explicit stab dropped node's predecessor
# Fix Finger table that has node 3 in it
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
list
show 0
show 1
show 2
fix 1
show 1
# Stab 2 shall fix the No predecessor for 0
stab 2
show 0
end
