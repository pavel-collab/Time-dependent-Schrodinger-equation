# TODO LIST

- [ ] Написать комментарии к функциям и методам
- [ ] Сделать нормировку графиков, там, где выводим несколько графиков на одном холсте. Например в моделях RampPotential или HarmonicOscilator. Или там, где нужно выводить и плотность вероятности и форму $\psi$ функции.
- [ ] ~~Зафигачить оптимизацию вчислений с помощью _numba_.~~
- [ ] ~~Попробовать ускорить исполнение кода путем компиляции python кода (см nuitka, cpython pypy etc)~~
- [X] Сделать правку параметров модели через json-конфиг. Для каждой можели в папке config создать json file и передавать его программе через параметры командной строки.
- [X] Можно сделать возможность ввода параметров через ключи запуска программы. Тогда можно будет написать скрипты, которые будут автоматически генерить визуализации с разными параметрами.
- [ ] Мы везде учитываем, что $\hbar = 1$ и $m = 1$, возможно нужно сделать эти величины параметрами структур.
- [X] Дописать в конфиг total_frames и fps
- [ ] Сделать еще несколько видов потенциальных барьеров (стенок)
- [ ] Попробовать сделать не последовательный, а параллельный запуск

# For developers

__ATTENTION!__
_Перед началом работы создайте в корневой дериктории проекта папку video._

На данный момент основная разработка ведется в папке models. Вся логика описывается в классах
в файлах ShrodingerEquation.py (класс волнового пакета и $\psi$- функции) и PotentialBarriers.py
(разные виды потенциальных барьеров).

Каждый файл модели является самодостаточным файлом, который можно исполнять.
```
python3 WavePackage.py
```

Кроме того, для автоматического тестирования большого количества моделей есть файл _run.py_. Этот 
файл автоматически поочередно запускает перечисленные в нем модели. Скрипт ждет завершение каждой 
модели, после чего сразу запускает следующую.

Результат работы сохраняется в папке _video_ в качестве файла _mp4_. Информация о времени работы
каждой модели можно посмотреть в _/models/info.log_.

### Структура json-конфига

```
[
    {
        "N" : 1000,
        "x_start" : -150,
        "x_end" : 210
    },

    {
        "x0" : -100,
        "sigma0" : 5.0,
        "E0" : 0.5
    },

    {
        "V_x0" : 70,
        "V0" : 0.55,
        "a" : 30
    }
]
```
Json-конфиг состоит из массива в котором находится 3 словаря. Первый словарь -- отвечает за параметры модели в целом: 
количество точек, на которые разделится пространственный интервал, начало и конец пространственного интервала. Второй словарь
содержит параметры волнового пакета: начальную координату, ширину и энергию. Последний словарь содержит параметры 
потенциального барьера: координату, высоту и ширину.

__NOTE:__ в конфигах для моделей HarmonicOscillator и RampPotential в параметрах потенциального 
барьера храняться обратные величины. Они помечены как _~k_ и _~omega_. То есть в коде нужно взять 
величины, обратные им _k = 1 / ~k_ и _omega = 1 / ~omega_.

# Тестирование на удаленном сервере

Формат конфига
```
host vs
   hostname <ip-address>
   user root
   IdentityFile <path-to-privet-key>
```

При использовании конфига, для ssh подключения достаточно ввести
```
ssh vs
```

# Time dependence Shrodinger equation

Численное решение временного уравнения Шрёдингера позволяет создать визуализацию движущегося 
волнового пакета. Модель позволяет пронаблюдать такие квантовые эффекты, как туннельный эффект,
прохождение потенциальнрго барьера, осциляцию пакета в параболическом потенциале и др.

Запишем общий вид уравнения Шрёдингера

$$H \langle \psi \rangle = E \psi$$

где $\psi$ -- волновая функция, $H$ -- оператор полной энергии (гамильтониан), $E$ -- полная энергия 
системы. Вид гамильтониана

$$H = - \frac{\hbar}{2m} \Delta + U(r)$$

где $\Delta$ -- оператор Лапласа.

Это запись для уравнения Шрёдингера, независимого от времени (стационарного состояния). При записи, 
фактически в правой части мы перешли от оператора, дающего зависимость по времени к величине полной 
энергии. Для того, чтобы записать уравнение, зависящее от времени перейдем к операторам в обеих частях.

$$H \langle \psi \rangle = E  \langle \psi \rangle$$

где $E$ теперь является оператором

$$E = i \hbar \frac{\partial}{\partial t}$$

Теперь уравнение имеет следующий вид

$$i \hbar \frac{\partial \psi(r, t)}{\partial t} = H \langle \psi(r, t) \rangle$$

В этом случае решение дифференциального уравнения можно выразить следующим образом

$$\psi(r, t) = \exp(-i H t) \psi(r, 0)$$

Будем рассматривать распространение волнового пакета вдоль оси $Ox$. Тогда гамильтониан запишем следующим 
образом

$$H = - \frac{\hbar}{2m} \frac{\partial^2}{\partial x^2} + U(x)$$

Для вычисления второй производной воспользуемся формулой вычислительной метематики

$$\frac{\partial^2 f}{\partial x^2} _{x = j \Delta x} = \frac{f_{j+1} - 2f_{j} + f_{j-1}}{dx^2}$$

Тогда, если $f$ представляет собой вектор дискретных значений

$$
\begin{pmatrix}
f_1 \\
f_2 \\
\dots \\
f_N
\end{pmatrix}
$$

То вектор значений вторых происзводных этой функции в узлах построенной сетки можно получить с помощью
трехдиагональной матрицы

$$
\begin{pmatrix}
f_1'' \\
f_2'' \\
\dots \\
f_N''
\end{pmatrix}
= \frac{1}{dx^2}
\begin{pmatrix}
-2 &  1 & 0 & 0     & \dots & 0 & 0 \\
1  & -2 & 1 & 0     & \dots & 0 & 0 \\
0  & 1  &-2 & 1     & \dots & 0 & 0 \\
   &    &   & \dots &       &   &   \\
0  & 0  & 0 & 0     & \dots &-2 & 1 \\
\end{pmatrix}
\begin{pmatrix}
f_1 \\
f_2 \\
\dots \\
f_N
\end{pmatrix}
$$

Значение потенциальной энергии $U$ так же можно представить в виде вектора значений в узлах сетки. Тогда
действие оператора $H$ на вектор значений волновой функции $\psi$ можно представить, как умножение вектора 
значений волновой функции на матрицу

$$
H =- \frac{\hbar}{2 m dx^2}
\begin{pmatrix}
-2 &  1 & 0 & 0     & \dots & 0 & 0 \\
1  & -2 & 1 & 0     & \dots & 0 & 0 \\
0  & 1  &-2 & 1     & \dots & 0 & 0 \\
   &    &   & \dots &       &   &   \\
0  & 0  & 0 &       & \dots &-2 & 1 \\
\end{pmatrix}
\begin{pmatrix}
V_1 &  0  & 0   & 0     & \dots & 0 & 0 \\
0   & V_2 & 0   & 0     & \dots & 0 & 0 \\
0   & 0   & V_3 & 0     & \dots & 0 & 0 \\
    &     &     & \dots &       &   &   \\
0   & 0   & 0   & 0     & \dots & 0 & V_N\\
\end{pmatrix}
$$

$$\langle f \rangle = \int \psi^* f \psi $$

в данном случае в правой части $f$ -- есть оператор. Таким образом

$$\langle x \rangle = \int \psi^* x \psi $$
