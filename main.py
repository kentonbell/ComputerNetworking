
# hw1: CSCD 330, homework 1.
# author: Kenton Bell


from sys import argv
from random import seed, randint


def main():
    # Do not edit main.

    if len(argv) != 4:
        print("Usage:")
        print("\tpython3 hw1.py seed count max")
        exit(1)

    # Convert from string to int.
    seed_value, element_count, max_value = map(int, argv[1:])
    seed(seed_value)  # Output must be reproducible.

    values = []
    for _ in range(element_count):
        values += [randint(0, max_value)]

    sum_every_nth(values, randint(1, max_value))
    count_duplicates(values)

    text = ""
    line_count = 0
    with open("Frankenstein.txt", "r") as file:
        for line in file:  # Do not modify.
            text += line
            line_count += 1

    print_line_after(text, randint(0, line_count - 1),
                     randint(0, max_value))


def sum_every_nth(values, n):
    """
    Prints out the sum of every nth element of values, including
    the 0th element.
    For example:
        - ([1, 2, 3, 4], 2) => 4
        - ([3, 5], 7) => 3

    Inputs:
        - values (int[]): A list of ints.
        - n (int): An int to step by.
    Outputs:
        - None (Output is printed to STDOUT)
    """
    # TODO: Use a for loop and the range function.

    # print(sum(values[::n])) #this works too

    total = 0
    for i in range(0, len(values), n):
        total += values[i]
    print(total)

    pass


def count_duplicates(values):
    """
    Prints out a sorted list of [(value, occurence_count)] calculated
    from the input values.
    For example:
        - ([1, 2, 3]) => [(1, 1), (2, 1), (3, 1)]
        - ([1, 2, 3, 2, 1]) => [(1, 2), (2, 2), (3, 1)]

    Inputs:
        - values (int): A list of ints.
    Outputs:
        - None (Output is printed to STDOUT)
    """
    duplicates = {}
    # TODO: Use a dictionary and a for loop.

    for i in values:
        if i in duplicates:
            duplicates[i] += 1
        else:
            duplicates[i] = 1
    print(sorted(duplicates.items()))



def print_line_after(text, line, after):
    """
    Print the line from text starting at the index 'after'.
    For example:
        - ("Hello, world!", 0, 7) => world!
        - ("1\n2\n3", 1, 0) => 2
        - ("1\n2\n3", 1, 5) =>

    Inputs:
        - text (String): A string of characters.
        - line (int): An int selecting the line from the text as
                      separated by the new line character '\n'
        - after (int): An int selecting the starting index on the line
                       to print. Inclusive.
    Outputs:
        - None (Output is printed to STDOUT)
    """
    # TODO: Use the split function.

    lines = text.split('\n')
    print(lines[line][after:])

    pass


if __name__ == "__main__":
    main()
