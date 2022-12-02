
shape = {
    'A': 'Rock',
    'B': 'Paper',
    'C': 'Scissors',
}

shape_score = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3,
}
# Rock > Scissors: 1 - 3 = -2
# Scissors > Paper: 3 - 2 = 1
# Paper > Rock: 2 - 1 = 1
order = ['Rock', 'Paper', 'Scissors']

score = 0
with open('input.txt') as f:
    for line in f:
        elf, me = line.strip().split()
        elf = shape[elf]
        elf_index = shape_score[elf] - 1
        # win or lose
        if me in ['Z', 'X']:
            # win
            if me == 'Z':
                score += 6
                me = elf_index + 1
            # lose
            else:
                me = elf_index - 1
            # wrap around
            if me >= len(order):
                me = len(order) - me
            me = order[me]
        # tie
        else:
            score += 3
            me = elf

        print(elf, me)
        score += shape_score[me]

print(score)