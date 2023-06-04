def move_disk(n, source, destination, auxiliary):
    if n == 1:
        print(f"Move disk from peg {source} to peg {destination}")
        return

    move_disk(n - 1, source, auxiliary, destination)
    print(f"Move disk from peg {source} to peg {destination}")
    move_disk(n - 1, auxiliary, destination, source)

num_disks = 3
move_disk(num_disks, 0, 2, 1)
