import socket


def h_encode(data: str) -> str:
    bits = [int(bit) for bit in data]
    r = 0
    while 2 ** r < len(bits) + r + 1:
        r += 1

    result = [0] * (len(bits) + r)
    j = 0
    for i in range(len(result)):
        if i + 1 == 2 ** j:
            j += 1
        else:
            result[i] = bits.pop(0)

    for i in range(r):
        pos = 2 ** i - 1
        check = 0
        for j in range(pos, len(result), 2 * pos + 2):
            check ^= result[j:j + pos + 1].count(1) % 2
        result[pos] = check

    return ''.join([str(bit) for bit in result])


def string_to_binary(string):
    binary_string = ' '.join(format(ord(char), '08b') for char in string)
    return binary_string

def combine_binary_strings(binary_string):
    binary_list = binary_string.split()
    combined_string = ''.join(binary_list)
    return combined_string


def register_user(name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    client_socket.send(f"register:{name}".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "Username taken":
        print("Error: Username is already taken. Please choose a different one.")
        client_socket.close()
        return None
    else:
        print(f"Registered successfully. Your id is: {response}")
        client_socket.close()
        return response

def send_message(sender_id, receiver_name, message):

    acc = string_to_binary(message)
    acc2 = combine_binary_strings(acc)
    encoded_message = h_encode(acc2)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    client_socket.send(f"send:{sender_id}:{receiver_name}:{encoded_message}".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print("Server response:", response)
    client_socket.close()

if __name__ == "__main__":
    name = input("Enter your name: ")
    user_id = None
    while user_id is None:
        user_id = register_user(name)
        if user_id is None:
            name = input("Enter a different name: ")
    while True:
        receiver_name = input("Enter receiver's name (or 'exit' to quit): ")
        if receiver_name == 'exit' or receiver_name == 'exit ':
            break
        message = input("Enter message: ")
        send_message(user_id, receiver_name, message)