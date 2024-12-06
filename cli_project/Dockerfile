FROM rust:latest

WORKDIR /usr/src/cli_project
COPY . .

RUN cargo install --path .

ENTRYPOINT ["dogs"]