
with open('input.txt') as f:
    buffer = f.readline().strip()
    start_of_packet = 0
    start_of_message = 0
    for i in range(0, len(buffer)):
        if not start_of_packet and len(set(buffer[i:i+4])) == 4:
            start_of_packet = i+4
        if not start_of_message and len(set(buffer[i:i+14])) == 14:
            start_of_message = i+14
            break

    print(start_of_packet)
    print(start_of_message)
