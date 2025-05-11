# Eshu

A common-language platform for post-exploitation across multiple C2 frameworks (Sliver, Metasploit, and beyond).

---

## 📦 Installation

```bash
# Clone and install in editable mode (you can also pip install from PyPI once published)
git clone https://github.com/ProDefense/Eshu.git
cd Eshu
pip install -e .
````

Eshu requires:

* Python 3.7+
* `sliver-py`
* `pymetasploit3`
* `toml`

---

## 🔧 Configuration

Create a `config.toml` in your project root. Each C2 framework you want to orchestrate gets its own section.

```toml
# config.toml

# — Sliver instances
[[c2.sliver]]
name        = "red-team-sliver"
config_path = "/etc/sliver/red.yml"

[[c2.sliver]]
name        = "blue-team-sliver"
config_path = "/etc/sliver/blue.yml"

# — Metasploit RPC instances
[[c2.metasploit]]
name     = "msf-local"
host     = "127.0.0.1"
port     = 55552
password = "changeme"
```

* **`name`**: logical alias for filtering and output.
* **Sliver** needs `config_path` (YAML config for SliverClient).
* **Metasploit** needs `host`/`port`/`password`.

---

## 🚀 Quickstart CLI

After installing, Eshu exposes a `c2-orchestrator` script:

```bash
# Show help
c2-orchestrator --help

# List all sessions across every C2
c2-orchestrator config.toml --list-sessions

# List all beacons (Sliver only)
c2-orchestrator config.toml --list-beacons

# Run 'whoami' on every active session
c2-orchestrator config.toml --cmd whoami

# Increase verbosity
c2-orchestrator config.toml --list-sessions --log-level DEBUG
```

---

## 📚 Quickstart Library

Use Eshu programmatically in your own Python code:

```python
import logging
from eshu import C2Orchestrator

# optional: configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

# load your config
orch = C2Orchestrator("config.toml")

# get all sessions
sessions = orch.get_all_sessions()
for s in sessions:
    print(f"{s['c2']} | {s['session_id']} | {s.get('platform')}")

# run commands
results = orch.run_on_sessions(["uname", "-a"])
for key, output in results.items():
    print(f"== {key} ==")
    print("\n".join(output))
```

---

## 🛠️ Extension: Adding a New C2

1. **Create your C2 subclass** in `src/eshu/c2s/<yourc2>/yourc2.py`:

   ```python
   from eshu.base_C2 import BaseC2

   class MyC2(BaseC2):
       NAME = "myc2"

       @property
       def CLIENT(self):
           return self._client

       def __init__(self, host: str, token: str):
           self._client = MyC2Client(host, token)
           self._client.connect()

       def list_sessions(self):
           raw = self._client.list_sessions()
           return [
               {"session_id": r.id, "platform": r.os, "target_host": r.host}
               for r in raw
           ]

       def list_beacons(self):
           return []  # if unsupported

       def send_beacon_cmd(self, beacon_id, commands):
           raise NotImplementedError

       def send_session_cmd(self, session_id, commands):
           outputs = []
           for cmd in commands:
               outputs.append(self._client.run(session_id, cmd))
           return outputs
   ```

2. **Register in the map** in `eshu/orchestrator.py`:

   ```python
   from eshu.c2s.myc2.yourc2 import MyC2
   C2_CLASS_MAP["myc2"] = MyC2
   ```

3. **Extend your `config.toml`**:

   ```toml
   [[c2.myc2]]
   name = "foo"
   host = "c2.example.com"
   token = "abcdef123456"
   ```

4. **Reinstall** (if editable mode, just reload):

   ```bash
   pip install -e .
   ```

Now you can orchestrate your new C2 alongside Sliver and Metasploit.

---

## ⚙️ Logging & Debugging

* Use `--log-level DEBUG` on the CLI or configure `logging.basicConfig(level=logging.DEBUG)` in library code to see internal steps.
* Logs include: loaded frameworks, instantiation errors, per-session/beacon fetch, and per-command output.

---

## 📄 License

Eshu is GPL Licensed. See [LICENSE](LICENSE) for details.
