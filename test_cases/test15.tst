# Adding to case 2 everything is stable and global information is correct
# Drop the all node except first and last node, now stab
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
drop 2
show 0
show 3
stab 0
stab 3
show 0
show 3
end
