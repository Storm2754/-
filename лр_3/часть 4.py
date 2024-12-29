import threading
import time
import argparse
import platform
import psutil  # для информации о процессоре и памяти
import os


#Представления общего счетчика
class Counter: 

    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()  # Блокировка для защиты от гонок

    #Инкрементирует счетчик
    def increment(self):
        
        with self.lock: # Блокировка для защиты от гонок
          self.value += 1

    #Декрементирует счетчик
    def decrement(self):
        
        with self.lock: # Блокировка для защиты от гонок
          self.value -= 1
    
    def get_value(self):
       """Получение значения счетчика."""
       with self.lock:
          return self.value


#Функция для потоков, инкрементирующих счетчик
def worker_increment(counter, iterations):

    for _ in range(iterations):
        counter.increment()

#Функция для потоков, декрементирующих счетчик
def worker_decrement(counter, iterations):
  
    for _ in range(iterations):
        counter.decrement()

#Запускает n инкрементирующих и m декрементирующих потоков
def run_threads(n, m, iterations=100000):

    counter = Counter()
    threads = []

    start_time = time.time()  # Засекаем время начала работы

    # Создание и запуск инкрементирующих потоков
    for _ in range(n):
        thread = threading.Thread(target=worker_increment, args=(counter, iterations))
        threads.append(thread)
        thread.start()

    # Создание и запуск декрементирующих потоков
    for _ in range(m):
        thread = threading.Thread(target=worker_decrement, args=(counter, iterations))
        threads.append(thread)
        thread.start()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    end_time = time.time()  # Засекаем время окончания работы
    elapsed_time_ms = (end_time - start_time) * 1000 # Время выполнения в миллисекундах
    
    final_value = counter.get_value() # Получение значения счетчика

    return final_value, elapsed_time_ms

def get_system_info():
    """Собирает информацию о системе."""
    system_info = {
        "Операционная система": platform.system() + " " + platform.release(),
        "Архитектура": platform.machine(),
        "Процессор": platform.processor(),
         "Количество ядер CPU": psutil.cpu_count(logical=False),
        "Количество потоков CPU": psutil.cpu_count(logical=True),
        "Объем RAM (ГБ)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        
    }
    return system_info

def save_system_info(filename="спецификация.txt"):
    """Сохраняет информацию о системе в файл."""
    info = get_system_info()
    with open(filename, "w", encoding="utf-8") as f:
        for key, value in info.items():
            f.write(f"{key}: {value}\n")


def save_results_table(results, filename="таблица.txt"):
    """Сохраняет результаты в виде текстовой таблицы."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("{:<15} {:<15} {:<15} {:<15}\n".format("Инкремент", "Декремент", "Счетчик", "Время (мс)"))
        for n, m, value, elapsed_time_ms in results:
            f.write("{:<15} {:<15} {:<15} {:<15.2f}\n".format(n, m, value, elapsed_time_ms))


if __name__ == "__main__":
    
    save_system_info() # Сохраняем системную спецификацию
    
    thread_sets = [1, 2, 4, 8] # Наборы потоков
    results = []

    for num_threads in thread_sets:
        final_value, elapsed_time_ms = run_threads(num_threads, num_threads)
        results.append((num_threads, num_threads, final_value, elapsed_time_ms))
        
    save_results_table(results) # Сохраняем результаты в таблицу
    print("Результаты сохранены в таблицу.txt")
    print("Спецификация системы сохранена в спецификация.txt")