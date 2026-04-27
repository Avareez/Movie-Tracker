# Virtual Environment (venv) Setup

## Windows (PowerShell)

### Fix execution policy (one-time only)
If you see `cannot be loaded because running scripts is disabled`:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Create venv (one-time only)
```powershell
python -m venv venv
```

### Activate (every time you open the project)
```powershell
venv\Scripts\Activate.ps1
```

### Install dependencies (one-time only, after activating)
```powershell
pip install -r requirements.txt
```

### Deactivate
```powershell
deactivate
```

---

## macOS / Linux

### Create venv (one-time only)
```bash
python3 -m venv venv
```

### Activate (every time you open the project)
```bash
source venv/bin/activate
```

### Install dependencies (one-time only, after activating)
```bash
pip install -r requirements.txt
```

### Deactivate
```bash
deactivate
```

---

## How to know venv is active?
You will see `(venv)` at the beginning of your terminal line:
```
(venv) C:\projects\movieverse>
```