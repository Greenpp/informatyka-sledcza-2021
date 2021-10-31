# Informatyka śledcza

## Email proxy, skanujące pod kątem złośliwych wiadomości

## Installation
```
poetry install
```
## How to run

To start proxy

```
poetry run python run_proxy.py
```

To start receiver

```
poetry run python run_receiver.py
```

To start quarantine

```
poetry run python run_quarantine.py
```

To send emails

```
poetry run python run_sender.py
```

## Settings

All settings can be set in the `email_proxy.settings` file.
