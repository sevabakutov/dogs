# Сборка Rust проекта
FROM rust:latest AS rust-builder

WORKDIR /usr/src/cli_project
COPY cli_project ./cli_project

RUN cargo install --path ./cli_project

# Основной образ с Python
FROM python:3.13

WORKDIR /usr/src/ml_project
COPY ml_project ./ml_project

# Копируем скомпилированный бинарник из rust-builder
COPY --from=rust-builder /usr/local/cargo/bin/dogs /usr/src/ml_project/dogs

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r ./ml_project/requirements.txt

# Чистим ненужное (опционально)
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Делаем бинарник исполняемым
RUN chmod +x /usr/src/ml_project/dogs

# Запуск приложения
CMD ["/usr/src/ml_project/dogs"]