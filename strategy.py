import sys
import subprocess
import importlib.util

def pip_install(*packages):
    """Install packages into the current Python environment."""
    subprocess.run([sys.executable, "-m", "pip", "install", *packages], check=True)

def ensure_installed(package_spec, import_name=None):
    """
    Install the given package_spec (e.g. 'cpz-ai==1.2.3') if it's not already installed.
    If import_name is different from the PyPI name, pass it explicitly.
    """
    name = import_name or package_spec.split("==")[0].split(">=")[0].split("~=")[0]
    if importlib.util.find_spec(name) is None:
        print(f"📦 Installing {package_spec} ...")
        pip_install(package_spec)
    else:
        print(f"✅ {name} already installed.")

if __name__ == "__main__":
    ensure_installed("cpz-ai")  # Pin version if needed: cpz-ai==x.y.z
    import cpz  # Use the actual import name
    print(f"cpz-ai version: {getattr(cpz, '__version__', 'unknown')}")
#!/usr/bin/env python3
# Place a single KO market buy order using CPZ AI keys from environment.

import os
import sys
from cpz.clients.sync import CPZClient

# --- Set credentials ---
os.environ["CPZ_AI_API_KEY"] = "cpz_key_586ad67be2c54f36a7df466b"
os.environ["CPZ_AI_SECRET_KEY"] = "cpz_secret_5g3q3c6s3a5z4f1u342m3325b3q1n5f1j113f692o4473464"
os.environ["CPZ_STRATEGY_ID"] = "93e41f1f-60f0-4460-a805-c048cb95951c"

# --- Direct argument values ---
qty = 1
strategy_id = os.getenv("CPZ_STRATEGY_ID")
env = "paper"         # choose "paper" or "live"
broker = "alpaca"     # choose broker name
# --- Validation ---
if not os.getenv("CPZ_AI_API_KEY") or not os.getenv("CPZ_AI_SECRET_KEY"):
    print("CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment", file=sys.stderr)
    sys.exit(2)

if not strategy_id:
    print("--strategy-id (or CPZ_STRATEGY_ID) is required", file=sys.stderr)
    sys.exit(2)

# --- Execute order ---
client = CPZClient()
client.execution.use_broker(broker, account_id="account_ID")

order = client.execution.order(
    symbol="AA",
    qty=qty,
    side="buy",
    order_type="market",
    time_in_force="DAY",
    strategy_id=strategy_id,
)

print(order.model_dump_json())
