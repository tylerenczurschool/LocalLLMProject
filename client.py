import socket
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MoondreamChatHandler
from whisper_mic import WhisperMic


chat_handler = MoondreamChatHandler(clip_model_path="models\moondream2-mmproj-f16.gguf")
model_path = "models\moondream2-text-model-f16.gguf"

llm = Llama(
    model_path=model_path,
    chat_handler=chat_handler,
    n_gpu_layers =-1,
    n_ctx=2048,
    max_tokens=125
            )
messages = [
    {
        "role": "system", "content": "You are a helpful male assistant who answers questions and describes images."
    },
]


def start_client(host="75.102.217.105", port=12345):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    mic = WhisperMic()
    while True:
        packet = client_socket.recv(200)
        try:
            packet = packet.decode('utf-8')
            if (packet == 'true'):
                print("Waiting for picture.")
                data = b''
                while True:
                    try:
                        chunk = client_socket.recv(4096)
                        data += chunk
                        client_socket.settimeout(1)
                    except socket.timeout:
                        print("Finished recieving data.")
                        break

                with open('C:\q\picture.jpg', 'wb') as file:
                    file.write(data)
                    file.close()
            print("Wait 1 second then speak.")
            message = mic.listen()
            print(message)
            print("Stopped Listening")
            if (packet == 'true'):
                messages.append(
                    {"role": "user",
                    "content":[
                        {"type" : "text", "text": message},
                        {"type": "image_url", "image_url": {"url": "file:///C:/q/picture.jpg"} }
                        ]
                    }
                )
                client_socket.settimeout(1200)
            else:
                messages.append({"role": "user", "content": message})
            if len(messages) >= 4:
                messages.pop(1)
            response = llm.create_chat_completion(messages=messages)
            reply = response["choices"][0]["message"]["content"]
            print (reply)
            client_socket.send(reply.encode('utf-8'))
            messages.append({"role": "assistant", "content": reply})
        except ConnectionResetError:
            print ("Connection reset by host")
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()

