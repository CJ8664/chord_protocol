# Just adding and joining nodes and explicit stab fix cycles
# Now all predecessor, successor and finger table are valid
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
end
