Суть решения проста.

1. Сохраняю данные о болельщиках, стадионах и такси в словари: номер: [координата_х, координата_у]. T_coord - такси, P_coord - болельщики, Z_coord - фан-зоны.

2. Предрасчитываю расстояние от каждого такси до ближайщего болельщика, а также от болелбщика до ближайшего стадиона.
A_B_dist - функция, которая реализует этот рассчёт.

3. До тех пор, пока есть хоть один не развезённый болельщик, повторяю процесс:
    * нахожу такси, которому ближе всего лететь до болельщика.
    * нахожу такси, которыс с ним "по пути"
    * формирую вывод
    * такси с болельщиком летит до фон-зоны, если есть такси, которым "по пути", то они тоже смещающтся.
    * такси смещается на 1 или дальше (если занято) со стадиона, чтобы на следующем ходе не возникло проблем с парковкой
    следдующего такси.
    
    
Что можно было улучшить, но я не улучшил:

1. Запускать того такси, не которому ближе лететь до болельщика, а того, которому ближе до болельщика + стадиона.
2. Улучшить алгоритм выбора "попутных" такси.
3. Если "попутное" такси вылетает к тому же пассажиру, что и основное, то тогда нет смысла его сдвигать.
4. Общая оптимизация скорости работы.

На тесте это решение дало 174 результат с 5490 баллами.
В итоге это 175 место с 3954.05 баллами. У лидера 9844.13 баллов.
