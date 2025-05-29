# pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
# pairs.sort(key=lambda pair: pair[1])
# print(pairs)
# pairs.sort(key=lambda pair: pair[1])

# def my_function():
#     """Do nothing, but document it.
#
#     No, really, it doesn't do anything.
#     """
#     pass
#
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
