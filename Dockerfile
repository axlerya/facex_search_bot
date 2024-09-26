# Используем официальный образ CUDA от NVIDIA с версией 11.8 и cuDNN8
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Устанавливаем переменные окружения для автоматической настройки часового пояса
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    tzdata \
    software-properties-common \
    && apt-get clean

# Устанавливаем Python 3.10
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-dev python3.10-distutils && \
    ln -sf /usr/bin/python3.10 /usr/bin/python3

# Устанавливаем pip для Python 3.10
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && rm get-pip.py

# Устанавливаем PyTorch и Torchvision с поддержкой CUDA 11.7
RUN pip install torch==2.2.2+cu118 torchvision==0.17.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

# Устанавливаем PyAV
RUN pip install av

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем наш скрипт в контейнер
COPY . /app

# Указываем рабочую директорию
WORKDIR /app

# Обновляем PATH для корректной работы Python
ENV PATH="/usr/local/bin:/usr/bin/python3.10:$PATH"
ENV PYTHONPATH="/app"

# Указываем точку входа
CMD ["python3", "bot/main.py", "polling"]
