import socket
import threading

name_to_id = {}
clients = []



def num_of_zero(len_name):
    if len_name > 10000:
        return "0" + str(len_name)
    elif len_name > 1000:
        return ("0" * 2) + str(len_name)  
    elif len_name > 100:
        return ("0" * 3) + str(len_name)  
    elif len_name > 10:
        return ("0" * 4) + str(len_name)
    else:
        return ("0" * 5) + str(len_name)

def is_name_unique(name):
    return name not in name_to_id







def is_power_of_two(n):
    """Проверяет, является ли число n степенью двойки."""
    return (n & (n - 1)) == 0 and n != 0


def h_decode(data: str) -> tuple[str, int | None]:
    bits = [int(bit) for bit in data]
    r = 0
    while 2 ** r < len(bits):
        r += 1

    error_pos = 0

    # Вычисляем позицию ошибки.
    check_bits = [2 ** i for i in range(r)]
    check_bits.reverse()
    for i, check_bit in enumerate(check_bits):
        check = 0
        for j in range(check_bit - 1, len(bits), check_bit * 2):
            check += sum(bits[j:j + check_bit])
        if check % 2 == 1:
            error_pos += check_bit

    # Исправляем ошибку.
    if error_pos > 0:
        bits[error_pos - 1] = 1 - bits[error_pos - 1]

    # Убираем биты проверки.
    decoded_data = ''.join(
        str(bit)
        for i, bit in enumerate(bits)
        if not is_power_of_two(i + 1)
    )

    return (
        decoded_data,
        error_pos - 1 if error_pos > 0 else None,
    )


def split_binary_string(binary_string, chunk_size=8):
    # Разбиваем строку на части заданного размера
    chunks = [binary_string[i:i+chunk_size] for i in range(0, len(binary_string), chunk_size)]
    # Объединяем части в строку с пробелами
    result = ' '.join(chunks)
    return result


def binary_to_string(binary_string):
    binary_values = binary_string.split()
    ascii_string = ''.join(chr(int(binary, 2)) for binary in binary_values)
    return ascii_string













def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        data_parts = data.split(':')
        command = data_parts[0]

        if command == 'register':
            name = data_parts[1]
            if is_name_unique(name):
                
                len_name = len(name_to_id)+1                
                
                # user_id = ('0'*(5-len_name))+str(len_name)

                user_id = num_of_zero(len_name)
                name_to_id[name] = user_id

                clients.append((client_socket, user_id))
                print(f"Registered user '{name}' with id {user_id}")
                client_socket.send(str(user_id).encode('utf-8'))
            else:
                print(f"Error: Username '{name}' is already taken")
                client_socket.send("Username taken".encode('utf-8'))

        elif command == 'send':
            sender_id = int(data_parts[1])
            receiver_name = data_parts[2]
            encoded_message = data_parts[3]
            
            acc3 = h_decode(encoded_message)[0]
            acc4 = split_binary_string(acc3)
            message = binary_to_string(acc4)





            if receiver_name in name_to_id:
                receiver_id = name_to_id[receiver_name]
                print(f"Message '{message}' sent from '{sender_id}' to '{receiver_name}' (id: {receiver_id})")
                for client in clients:
                    if client[1] == receiver_id:
                        try:
                            client[0].send(f"{receiver_name}:{message}".encode('utf-8'))
                        except OSError as e:
                            print(f"Error sending message to client {receiver_name}: {e}")
                            clients.remove(client)
                client_socket.send("Message delivered".encode('utf-8'))
            else:
                print(f"Error: User '{receiver_name}' not registered")
                client_socket.send("User not registered".encode('utf-8'))

        else:
            print("Invalid command")

    for client in clients:
        if client[0] == client_socket:
            clients.remove(client)
            break

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server started. Listening on port 5555...")

    while True:
        client_socket, _ = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()


