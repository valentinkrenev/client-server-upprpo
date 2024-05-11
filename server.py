import socket
import threading

name_to_id = {}
clients = []

def generate_hamming_code(data):
    n = len(data)
    m = 0
    while 2**m < n + m + 1:
        m += 1

    hamming_code = list(data) + ['0'] * m
    for i in range(m):
        position = 2**i - 1
        count = 0
        j = position
        while j < n + m:
            for k in range(position, min(position + 2**i, n + m)):
                if k != position:
                    hamming_code[position] = str(int(hamming_code[position]) ^ int(hamming_code[k]))
                count += 1
                if count == 2**i:
                    j += 2**i
                    position = j
                    break
    return ''.join(hamming_code)

def check_hamming_code(data):
    n = len(data)
    m = 0
    while 2**m < n:
        m += 1

    positions = []
    for i in range(m):
        position = 2**i - 1
        count = 0
        j = position
        while j < n:
            for k in range(position, min(position + 2**i, n)):
                count += int(data[k])
            j += 2**i
            position = j
        if count % 2 != 0:
            positions.append(position)

    if positions:
        data = list(data)
        for pos in positions:
            data[pos] = '1' if data[pos] == '0' else '0'
        return ''.join(data)
    else:
        return data

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
                len_name = len(name_to_id) + 1
                user_id = num_of_zero(len_name)
                name_to_id[name] = user_id

                clients.append((client_socket, user_id))
                print(f"Пользователь '{name}' зарегистрирован с id {user_id}")
                client_socket.send(str(user_id).encode('utf-8'))
            else:
                print(f"Ошибка: Имя пользователя '{name}' уже занято")
                client_socket.send("Имя пользователя занято".encode('utf-8'))

        elif command == 'send':
            sender_id = int(data_parts[1])
            receiver_name = data_parts[2]
            message = data_parts[3]
            corrected_message = check_hamming_code(message)
            if corrected_message != message:
                print("Сообщение содержит ошибки. Исправленное сообщение:", corrected_message)
            else:
                print("Сообщение получено без ошибок:", message)
            if receiver_name in name_to_id:
                receiver_id = name_to_id[receiver_name]
                print(f"Сообщение '{message}' отправлено от '{sender_id}' к '{receiver_name}' (id: {receiver_id})")
                for client in clients:
                    if client[1] == receiver_id:
                        try:
                            client[0].send(f"{receiver_name}:{corrected_message}".encode('utf-8'))
                        except OSError as e:
                            print(f"Ошибка отправки сообщения клиенту {receiver_name}: {e}")
                            clients.remove(client)
                client_socket.send("Сообщение доставлено".encode('utf-8'))
            else:
                print(f"Ошибка: Пользователь '{receiver_name}' не зарегистрирован")
                client_socket.send("Пользователь не зарегистрирован".encode('utf-8'))

        else:
            print("Неверная команда")

    for client in clients:
        if client[0] == client_socket:
            clients.remove(client)
            break

    client_socket.close()

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

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Сервер запущен. Ожидание подключений на порту 5555...")

    while True:
        client_socket, _ = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
