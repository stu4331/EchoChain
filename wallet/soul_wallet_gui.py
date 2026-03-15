"""
Soul Wallet GUI (Sepolia/Holesky testnet)
- Reads RPC and private key from env or text fields
- Displays SOUL balance and lets you cast a vote if a Governor address is provided
- Never logs or writes keys; uses in-memory signing only

Prereqs (inside your venv):
  pip install web3 eth-account

Env vars (optional):
  SEPOLIA_RPC=<https url>
  PRIVATE_KEY=<testnet private key>

Addresses:
  Populate chain/addresses.json with governor and token addresses.
"""

import json
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from web3 import Web3
    from eth_account import Account
    WEB3_AVAILABLE = True
except Exception as e:  # noqa: F841
    WEB3_AVAILABLE = False

ROOT = Path(__file__).resolve().parents[1]
CHAIN_DIR = ROOT / "chain"
ADDRESSES_FILE = CHAIN_DIR / "addresses.json"
DEFAULT_CHAIN_ID = 11155111  # Sepolia

ERC20_ABI = [
    {"name": "decimals", "outputs": [{"type": "uint8"}], "stateMutability": "view", "type": "function", "inputs": []},
    {"name": "balanceOf", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function", "inputs": [{"name": "account", "type": "address"}]},
    {"name": "delegate", "outputs": [], "stateMutability": "nonpayable", "type": "function", "inputs": [{"name": "delegatee", "type": "address"}]}
]

GOVERNOR_ABI = [
    {"name": "castVoteWithReason", "inputs": [{"name": "proposalId", "type": "uint256"}, {"name": "support", "type": "uint8"}, {"name": "reason", "type": "string"}], "outputs": [{"type": "uint256"}], "stateMutability": "nonpayable", "type": "function"},
]


def load_addresses():
    if ADDRESSES_FILE.exists():
        try:
            with open(ADDRESSES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            contracts = data.get("contracts") or {}
            return {
                "token": contracts.get("soulToken") or data.get("soulToken"),
                "governor": contracts.get("governor") or data.get("governor"),
                "chainId": data.get("chainId") or DEFAULT_CHAIN_ID,
            }
        except Exception:
            return {"token": None, "governor": None, "chainId": DEFAULT_CHAIN_ID}
    return {"token": None, "governor": None, "chainId": DEFAULT_CHAIN_ID}


class SoulWalletGUI:
    def __init__(self, master):
        self.master = master
        master.title("SOUL Wallet (testnet)")
        master.geometry("600x420")

        self.status_var = tk.StringVar(value="Disconnected")
        self.address_var = tk.StringVar(value="")
        self.rpc_var = tk.StringVar(value=os.getenv("SEPOLIA_RPC", ""))
        self.pk_var = tk.StringVar(value=os.getenv("PRIVATE_KEY", ""))
        self.token_addr_var = tk.StringVar(value="")
        self.gov_addr_var = tk.StringVar(value="")
        self.proposal_var = tk.StringVar(value="")
        self.reason_var = tk.StringVar(value="AI vote: uphold core values")
        self.balance_var = tk.StringVar(value="?")
        self.chain_id = DEFAULT_CHAIN_ID

        # Web3 state
        self.w3 = None
        self.account = None
        self.token = None
        self.governor = None

        self._build_ui()
        self._preload_addresses()

    def _build_ui(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="RPC URL (Sepolia/Holesky)").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.rpc_var, width=60).grid(row=0, column=1, sticky="we")

        ttk.Label(frm, text="Private Key (testnet)").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.pk_var, show="*", width=60).grid(row=1, column=1, sticky="we")

        ttk.Label(frm, text="SOUL Token Address").grid(row=2, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.token_addr_var, width=60).grid(row=2, column=1, sticky="we")

        ttk.Label(frm, text="Governor Address").grid(row=3, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.gov_addr_var, width=60).grid(row=3, column=1, sticky="we")

        btn_row = ttk.Frame(frm)
        btn_row.grid(row=4, column=0, columnspan=2, pady=8, sticky="we")
        ttk.Button(btn_row, text="Connect", command=self.connect).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_row, text="Refresh Balance", command=self.refresh_balance).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_row, text="Delegate to self", command=self.delegate_self).pack(side=tk.LEFT, padx=4)

        ttk.Separator(frm, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky="we", pady=8)

        ttk.Label(frm, text="Proposal ID").grid(row=6, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.proposal_var, width=30).grid(row=6, column=1, sticky="w")
        ttk.Label(frm, text="Reason").grid(row=7, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.reason_var, width=60).grid(row=7, column=1, sticky="we")

        vote_row = ttk.Frame(frm)
        vote_row.grid(row=8, column=0, columnspan=2, pady=8, sticky="we")
        ttk.Button(vote_row, text="Vote YES", command=lambda: self.cast_vote(1)).pack(side=tk.LEFT, padx=4)
        ttk.Button(vote_row, text="Vote NO", command=lambda: self.cast_vote(0)).pack(side=tk.LEFT, padx=4)
        ttk.Button(vote_row, text="Abstain", command=lambda: self.cast_vote(2)).pack(side=tk.LEFT, padx=4)

        ttk.Separator(frm, orient=tk.HORIZONTAL).grid(row=9, column=0, columnspan=2, sticky="we", pady=8)

        ttk.Label(frm, text="Address").grid(row=10, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.address_var).grid(row=10, column=1, sticky="w")

        ttk.Label(frm, text="SOUL Balance").grid(row=11, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.balance_var).grid(row=11, column=1, sticky="w")

        ttk.Label(frm, text="Status").grid(row=12, column=0, sticky="w")
        ttk.Label(frm, textvariable=self.status_var).grid(row=12, column=1, sticky="w")

        for i in range(2):
            frm.columnconfigure(i, weight=1)

    def _preload_addresses(self):
        data = load_addresses()
        if data.get("token"):
            self.token_addr_var.set(data["token"])
        if data.get("governor"):
            self.gov_addr_var.set(data["governor"])
        self.chain_id = data.get("chainId", DEFAULT_CHAIN_ID)

    def connect(self):
        if not WEB3_AVAILABLE:
            messagebox.showerror("Missing deps", "Install web3 and eth-account in your venv.")
            return
        rpc = self.rpc_var.get().strip()
        pk = self.pk_var.get().strip()
        if not rpc:
            messagebox.showwarning("RPC required", "Set SEPOLIA_RPC or paste an RPC URL.")
            return
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        if not self.w3.is_connected():
            self.status_var.set("RPC not reachable")
            return
        if pk:
            try:
                self.account = Account.from_key(pk)
                self.address_var.set(self.account.address)
            except Exception as e:
                messagebox.showerror("Key error", f"Invalid private key: {e}")
                return
        else:
            self.account = None
            self.address_var.set("read-only")
        token_addr = self.token_addr_var.get().strip()
        gov_addr = self.gov_addr_var.get().strip()
        if token_addr:
            self.token = self.w3.eth.contract(address=self.w3.to_checksum_address(token_addr), abi=ERC20_ABI)
        if gov_addr:
            self.governor = self.w3.eth.contract(address=self.w3.to_checksum_address(gov_addr), abi=GOVERNOR_ABI)
        self.status_var.set("Connected")
        self.refresh_balance()

    def _require_connection(self):
        if not self.w3 or not self.w3.is_connected():
            raise RuntimeError("Connect to an RPC first")

    def refresh_balance(self):
        try:
            self._require_connection()
            if not self.token:
                self.balance_var.set("token missing")
                return
            decimals = self.token.functions.decimals().call()
            addr = self.account.address if self.account else self.address_var.get()
            bal = self.token.functions.balanceOf(addr).call()
            human = bal / (10 ** decimals)
            self.balance_var.set(f"{human:.4f} SOUL")
        except Exception as e:
            self.balance_var.set(f"error: {e}")

    def delegate_self(self):
        if not self.account:
            messagebox.showinfo("Read-only", "Add a private key to delegate.")
            return
        if not self.token:
            messagebox.showwarning("Missing token", "Connect with a token address first.")
            return
        try:
            tx = self.token.functions.delegate(self.account.address).build_transaction({
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "chainId": self.chain_id,
                "gas": 120000,
                "maxFeePerGas": self.w3.to_wei("2", "gwei"),
                "maxPriorityFeePerGas": self.w3.to_wei("1", "gwei"),
            })
            signed = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            self.status_var.set(f"Delegate sent: {tx_hash.hex()}")
        except Exception as e:
            self.status_var.set(f"delegate error: {e}")

    def cast_vote(self, support):
        if not self.account:
            messagebox.showinfo("Read-only", "Add a private key to vote.")
            return
        if not self.governor:
            messagebox.showwarning("Missing governor", "Connect with a governor address first.")
            return
        try:
            proposal_id = int(self.proposal_var.get())
        except ValueError:
            messagebox.showwarning("Proposal", "Proposal ID must be an integer.")
            return
        reason = self.reason_var.get()
        try:
            tx = self.governor.functions.castVoteWithReason(proposal_id, support, reason).build_transaction({
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "chainId": self.chain_id,
                "gas": 250000,
                "maxFeePerGas": self.w3.to_wei("2", "gwei"),
                "maxPriorityFeePerGas": self.w3.to_wei("1", "gwei"),
            })
            signed = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            self.status_var.set(f"Vote sent: {tx_hash.hex()}")
        except Exception as e:
            self.status_var.set(f"vote error: {e}")


def main():
    root = tk.Tk()
    app = SoulWalletGUI(root)
    root.mainloop()


if __name__ == "__main__":
    if not WEB3_AVAILABLE:
        sys.stderr.write("web3 and eth-account are required. Install inside your venv.\n")
        sys.exit(1)
    main()
