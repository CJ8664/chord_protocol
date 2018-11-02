# Adding to case 2 everything is stable and global information is correct
# Drop one node from middle, now fix to update finger_table
# Now add 1 again, only stab
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

# First cycle of stab fix
stab 0
stab 1
stab 2
stab 3

fix 0
fix 1
fix 2
fix 3

# Second cycle of stab fix
stab 0
stab 1
stab 2
stab 3

fix 0
fix 1
fix 2
fix 3

# Third cycle of stab fix
stab 0
stab 1
stab 2
stab 3

fix 0
fix 1
fix 2
fix 3

# Fourth cycle of stab fix
stab 0
stab 1
stab 2
stab 3

fix 0
fix 1
fix 2
fix 3

show 0
show 1
show 2
show 3

drop 1

show 0
show 2
show 3

fix 0
fix 2
fix 3

show 0
show 2
show 3

add 1
join 1 0

show 0
show 1
show 2
show 3

stab 1
stab 0

show 0
show 1
show 2
show 3

end
