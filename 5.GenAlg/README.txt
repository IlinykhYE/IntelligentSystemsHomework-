0. Кодирование – выбор «генетического кода»
Особь – битовая последовательность размера n (кол-во грузов)
1. Начальная популяция – кол-во особей всегда = 200:
1.1 случайная генерация
2. Отбор особей для скрещивания:
2.1 выбор каждой особи пропорционально приспособленности (рулетка)
3. Скрещивание (кроссинговер) между выбранными особями. Каждая особь скрещивается 1 раз за 1 поколение, 1 пара дает 2 потомка:
3.1 многоточечный с 3мя точками
4. Мутация:
4.1 инвертирование всех битов у 1 особи
5. Формирование новой популяции (кол-во особей- константа)
5.1 замена не более 30% худших особей на потомков 
6. Оценка результата
Наступила сходимость (функция приспособленности лучшей особи в популяциях отличается не более, чем на 10%) или прошло 500 поколений.