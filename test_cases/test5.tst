# Adding to case 2 everything is stable and global information is correct
# Drop the first node 0, now explicit stab dropped node's predecessor
# Fix Finger table that has node 0 in it
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
drop 0
list
show 1
show 2
show 3
fix 2
show 2
# Stab 3 shall fix the No predecessor for 1
stab 3
show 1
end
