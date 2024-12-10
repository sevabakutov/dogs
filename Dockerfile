FROM rust:latest AS rust-builder

WORKDIR /usr/src/cli_project
COPY cli_project ./cli_project

RUN cargo install --path ./cli_project

FROM python:3.13

WORKDIR /usr/src/ml_project
COPY ml_project ./ml_project

COPY --from=rust-builder /usr/local/cargo/bin/dogs /usr/src/ml_project/dogs

RUN pip install --no-cache-dir -r ./ml_project/requirements.txt

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod +x /usr/src/ml_project/dogs

ENTRYPOINT ["/usr/src/ml_project/dogs"]