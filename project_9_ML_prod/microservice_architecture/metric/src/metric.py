import pika
import json
import os
import pandas as pd

# Проверяем, существует ли папка для логов, если нет — создаём
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)

# Файл для логирования метрик
metric_log_path = f'{log_dir}/metric_log.csv'

# Инициализация файла с заголовками, если файл еще не создан
if not os.path.exists(metric_log_path):
    with open(metric_log_path, 'w') as f:
        f.write('id,y_true,y_pred,absolute_error\n')
        
# Хранилище сообщений по их ID
message_store = {}

try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
   
    # Объявляем очередь y_true
    channel.queue_declare(queue='y_true')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')
    
    # Функция для записи метрики в CSV
    def log_metric_to_csv(message_id, y_true, y_pred):
        absolute_error = abs(y_true - y_pred)
        log_entry = {
            'id': message_id,
            'y_true': y_true,
            'y_pred': y_pred,
            'absolute_error': absolute_error
        }
        # Используем pandas для добавления новой строки в CSV
        df = pd.DataFrame([log_entry])
        df.to_csv(metric_log_path, mode='a', header=False, index=False)
        
    # Функция callback для обработки сообщений из очередей
    def callback(ch, method, properties, body):
        message = json.loads(body)
        message_id = message.get('id')
        message_body = message.get('body')

        if message_id is None:
            print(f"Сообщение без ID было проигнорировано: {message}")
            return

        # Сохраняем сообщение в хранилище
        if message_id not in message_store:
            message_store[message_id] = {}

        # Сохраняем данные в зависимости от очереди
        if method.routing_key == 'y_true':
            message_store[message_id]['y_true'] = message_body
        elif method.routing_key == 'y_pred':
            message_store[message_id]['y_pred'] = message_body

        # Проверяем, есть ли обе метрики для вычисления абсолютной ошибки
        if 'y_true' in message_store[message_id] and 'y_pred' in message_store[message_id]:
            y_true = message_store[message_id]['y_true']
            y_pred = message_store[message_id]['y_pred']

            # Логируем метрику в CSV
            log_metric_to_csv(message_id, y_true, y_pred)
            print(f"Метрика записана в лог: ID={message_id}, y_true={y_true}, y_pred={y_pred}")

            # Удаляем обработанный ID из хранилища
            del message_store[message_id]
    
    # Извлекаем сообщение из очереди y_true
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )
    # Извлекаем сообщение из очереди y_pred
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )
 
    # Запускаем режим ожидания прихода сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
    
except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')