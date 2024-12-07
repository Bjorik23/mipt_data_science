import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

# Путь к папке с логами внутри контейнера
log_dir = '/usr/src/app/logs'

# Путь к файлу с метриками
metric_log_path = os.path.join(log_dir, 'metric_log.csv')

# Путь к файлу с гистограммой
output_image_path = os.path.join(log_dir, 'error_distribution.png')

print("Сервис plot запущен. Ожидание новых данных...")

while True:
    try:
        # Проверяем, существует ли файл metric_log.csv
        if os.path.exists(metric_log_path):
            # Читаем данные из файла
            df = pd.read_csv(metric_log_path)

            if 'absolute_error' in df.columns:
                # Создаем фигуру
                plt.figure(figsize=(10, 6))
                
                # Строим гистограмму
                sns.histplot(
                    df['absolute_error'],
                    bins=40,
                    color='green',
                    edgecolor='black',
                    alpha=0.75
                )
                               
                plt.title('Распределение абсолютной ошибки')
                plt.xlabel('Absolute Error')
                plt.ylabel('Frequency')
                plt.grid(True)

                # Сохраняем график
                plt.savefig(output_image_path)
                plt.close()

                print(f"Гистограмма с кривой распределения сохранена в {output_image_path}")
            else:
                print("В таблице metric_log.csv отсутствует столбец 'absolute_error'.")
        else:
            print(f"Файл {metric_log_path} не найден. Ожидание...")
    except Exception as e:
        print(f"Ошибка при построении графика: {e}")

    # Ждём 10 секунд перед следующей итерацией
    time.sleep(10)
