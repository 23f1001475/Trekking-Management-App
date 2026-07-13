# create and activate env

```bash
python -m venv env
env/scripts/activate
```

# install requiremnets

```bash
pip install -r requirements.txt
``` 

# wsl create and actiavate env

```bash
python3 -m venv env
source env/bin/activate
```

# Redis install 

```bash
sudo apt update

sudo apt install -y redis-server
```

# Start redis server

```bash
redis-server
```

# To stop redis server

```bash
sudo systemctl stop redis
```

# Install MailHog

```bash
sudo apt update
sudo apt install -y golang-go
go install github.com/mailhog/MailHog@latest
```

# To run MailHog

```text
~/go/bin/MailHog
```

# To check MailHog result (MialHog UI)

```text
http://localhost:8025
```

# Run Flask app (in wsl)
```bash
python3 app.py
```

# run celery worker

```bash
celery -A celery_worker.celery_app worker --loglevel=info

```

# Run celery beat

```bash
celery -A celery_worker.celery_app beat --loglevel=info
```


