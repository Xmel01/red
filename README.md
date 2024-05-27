# Before running

1. Edit .env.compose in `/postgres` dir
2. Edit `.env` file in root dir
3. Run docker-compose by 
```
docker-compose --env-file .env.compose up -d
```
4. Set up environment
```bash
pyton3 -m venv venv
source venv/bin/activate
pip install -r req.txt
```
5. Run script
```bash
pythim main.py
```

# Script commands
1. "Connect" - use for connect to VM
    Arguments: Login, Password, VM id

2. "Disconnect" - use for disconnect from VM
3. "Create" - use for create VM
    Arguments: ram, cpu_cores, vincesters (list of hard volumes)
4. "ls" - list all VM
5. "lsa" - list all active VM
6. "lsc" - list all authored VM
