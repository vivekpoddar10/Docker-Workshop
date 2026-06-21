create project using :uv init workshop --python-3.13
add pandas and pyarrow: uv add pandas pyarrow

to build image:
docker build -t test:pandas .

to run image:
docker run -it --entrypoint=bash --rm test:pandas

uv run pgcli -h localhost -p 5432 -u root -d ny_taxi