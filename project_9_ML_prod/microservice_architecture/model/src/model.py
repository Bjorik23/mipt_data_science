import pika
import pickle
import numpy as np
import json

# Читаем файл с сериализованной моделью
with open('model.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

try:
    # Создаём подключение по адресу rabbitmq:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очередь features
    channel.queue_declare(queue='features')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')

    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        # Парсим сообщение из очереди
        message = json.loads(body)
        message_id = message.get('id')
        features = np.array(message.get('body')).reshape(1, -1)

        if message_id is None or features.size == 0:
            print(f"Некорректное сообщение: {message}")
            return

        # Предсказание модели
        pred = regressor.predict(features)
        pred_value = pred[0]

        # Формируем сообщение с предсказанием
        message_y_pred = {
            'id': message_id,
            'body': pred_value
        }

        # Отправляем предсказание в очередь y_pred
        channel.basic_publish(
            exchange='',
            routing_key='y_pred',
            body=json.dumps(message_y_pred)
        )
        print(f"Предсказание отправлено в очередь y_pred: {message_y_pred}")

    # Извлекаем сообщение из очереди features
    # on_message_callback указывает, какую функцию вызвать при получении сообщения
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    # Запускаем режим ожидания прихода сообщений
    channel.start_consuming()
except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')