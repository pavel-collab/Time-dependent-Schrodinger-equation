# About project

Данный проект представляет собой работу для государственного экзамента по общей физики
3 курс МФТИ. В работе рассматривается численное решение временного уравнения Шрёдингера.
На основе этого решения создаются визуализации различных моделей, демонстрирующие изменение
волновой функции в пространстве и во времени и ее поведение при налиии различных потенциальных 
преград.

Для того, чтобы создать визуализацию, скопируйте проект на свой компьютер, выбирете модель в
папке _models_ и запустите его как исполняемый файл
```
./QuantumTunnelling.py
```
или с помощью интерпритатора
```
python3 QuantumTunnelling
```

Если вы хотите узнать больше, обращайтесь к пункту _For developers_ или к автору проекта.

__ATTENTION1__
_Перед началом работы создайте в корневой дериктории проекта папку video._

__ATTENTION2__
_Программа создает видео в формате mp4. Для того, чтобы программа отработала может потребоваться значительное количество времени._

__ATTENTION3__
_Есть вероятность, что программа не будет корректно работать на вашем компьютере. Это связано с какими-то проблемами пакета matplotlib animation. В данный момент автор пытается разобраться с данной проблемой и составить соответствующую инструкцию._


<p align="center">
    <img src="https://github.com/pavel-collab/Time-dependent-Schrodinger-equation/blob/main/Tex/images/wave_package_26.01.2023-20.28.05_.gif" alt="caption" width="300"/>
</p>

<p align="center">
    <img src="https://github.com/pavel-collab/Time-dependent-Schrodinger-equation/blob/main/Tex/images/step_potential_26.01.2023-20.00.03_.gif" alt="caption" width="300"/>
</p>

<p align="center">
    <img src="https://github.com/pavel-collab/Time-dependent-Schrodinger-equation/blob/main/Tex/images/quantum_tunnelling_26.01.2023-19.38.56_.gif" alt="caption" width="300"/>
</p>

<p align="center">
    <img src="https://github.com/pavel-collab/Time-dependent-Schrodinger-equation/blob/main/Tex/images/harmonic_oscillator_26.01.2023-19.26.08_.gif" alt="caption" width="300"/>
</p>

<p align="center">
    <img src="" alt="caption" width="300"/>
</p>

<p align="center">
    <img src="https://github.com/pavel-collab/Time-dependent-Schrodinger-equation/blob/main/Tex/images/ramp_potential_26.01.2023-19.49.41_.gif" alt="caption" width="300"/>
</p>

# Time dependendent Shrodinger equation

Описание работы, теоретические данные и принцип численного решения вы можете найти в папке _Tex_.
В этой же папке содержатся _.tex_ исходники отчета а так же презентация.

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

Для того, чтобы не хардкодить численные параметры в коде  в папке _configs_ для  каждой модели написан json-конфиг, содержащий основные параметры модели.

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

В процессе разработки предполагалось, что тестирование  будет происходить на удаленной машине. Предполагалось 
передавать и выгружать данные по ssh соединению, однако  в силу некоторых трудностей от этой идеи пришлось 
отказаться.

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