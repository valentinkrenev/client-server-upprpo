import socket

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

def register_user(name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    client_socket.send(f"register:{name}".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "Имя пользователя занято":
        print("Ошибка: Имя пользователя уже занято. Пожалуйста, выберите другое.")
        client_socket.close()
        return None
    else:
        print(f"Регистрация прошла успешно. Ваш id: {response}")
        client_socket.close()
        return response

def send_message(sender_id, receiver_name, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    hamming_message = generate_hamming_code(message)
    client_socket.send(f"send:{sender_id}:{receiver_name}:{hamming_message}".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print("Ответ сервера:", response)
    client_socket.close()

if __name__ == "__main__":
    name = input("Введите ваше имя: ")
    user_id = None
    while user_id is None:
        user_id = register_user(name)
        if user_id is None:
            name = input("Введите другое имя: ")
    while True:
        receiver_name = input("Введите имя получателя (или 'выход' для выхода): ")
        if receiver_name == 'выход' or receiver_name == 'выход ':
            break
        message = input("Введите сообщение: ")
        send_message(user_id, receiver_name, message)
