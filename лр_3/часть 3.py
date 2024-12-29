import threading
import time
import argparse

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
    elapsed_time = end_time - start_time
    
    final_value = counter.get_value() # Получение значения счетчика

    # Вывод результата
    print(f"Итоговое значение счетчика: {final_value}")
    print(f"Время выполнения: {elapsed_time:.4f} секунд")  # .4f кол-во знаков после запятой
    return final_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запускает многопоточные операции с инкрементом и декрементом счетчика.")
    parser.add_argument("n", type=int, help="Количество инкрементирующих потоков")
    parser.add_argument("m", type=int, help="Количество декрементирующих потоков")
    args = parser.parse_args()

    final_counter_value = run_threads(args.n, args.m)
    print(f"Полученное значение счетчика после всех операций: {final_counter_value}")