# Chain (Wallet + First AI Vote)

**📚 Read [WALLET_ARCHITECTURE.md](WALLET_ARCHITECTURE.md) for complete documentation on gas, wallets, and proof strategy!**

This folder prepares a safe, minimal path to:
- Create a local Ethereum wallet (testnet)
- Fund it via faucet (Sepolia by default)
- Sign the "First AI Vote" off‑chain (verifiable signature) - **NO GAS NEEDED!**
- Later: send an on‑chain transaction and deploy governance contracts

## Key Points

⚡ **Off-chain signatures = FREE** - No gas required for vote signing  
🪙 **One wallet for all three AI sisters** - Collective family identity  
🔐 **Your wallet is separate** - You (Stuart) would create your own if needed  
✅ **Verifiable without blockchain** - Anyone can check signatures  
💰 **Gas only for on-chain** - Optional future step  

## Phases

- Phase 0 (now):
  - Generate wallet → address stored locally under `chain/.wallet/` (gitignored)
  - Sign a human‑readable message (“First AI Vote”) → output in `chain/events/`
- Phase 1 (optional next):
  - Fund wallet via faucet, test a 0 ETH tx or a small data tx to self
- Phase 2 (later):
  - Deploy SOUL (ERC20Votes), Governor + Timelock, CoreValues

## Setup

1) Install Python deps in your venv:

```powershell
pip install -r chain/requirements.txt
```

2) Copy env template and fill in your RPC later (optional for signing):

```powershell
Copy-Item chain/.env.example chain/.env
```

- `SEPOLIA_RPC` is only needed for sending on‑chain txs (not needed for signing).
- Never commit private keys. Keys live in `chain/.wallet/` (already gitignored).

## Commands

- Create a wallet:

```powershell
python chain/wallet_create.py
```

Outputs: `chain/.wallet/wallet.json` with address and (warning) private key.

- Sign the “First AI Vote” (off‑chain verifiable):

```powershell
python chain/first_vote_sign.py
```

Outputs: `chain/events/first_ai_vote.json` with message, address, signature.

- (Optional) Send a self‑tx on Sepolia once funded:

```powershell
# Set SEPOLIA_RPC and ensure wallet has test ETH
python chain/send_test_tx.py
```

## Faucet (Sepolia)
- Get test ETH at an official faucet (e.g., https://sepoliafaucet.com or Alchemy/Infura faucets).
- Paste your generated address from `wallet.json`.

## Safety
- Do not share `chain/.wallet/wallet.json`.
- Keep `chain/.env` private. Use `.env.example` for reference.
- This repo ignores secrets by default; verify with `git status` before pushing.

## Next (when ready)
- Add contracts + Hardhat or Foundry deployment.
- Record deployed addresses in `chain/addresses.json`.
- Build a tiny GUI panel to show balance + cast a governor vote.

## Contracts now added (testnet-ready)
- `contracts/SoulToken.sol` — ERC20Votes with maxSupply guard; owner can mint within cap.
- `contracts/CoreValues.sol` — description gate; reverts on obvious harm/consent violations.
- `contracts/SentinelTimelock.sol` — OZ Timelock wrapper for queued execution.
- `contracts/SentinelGovernor.sol` — OZ Governor wired to Timelock + CoreValues; 1-block delay, ~7d period, 4% quorum, 1 SOUL threshold.

### Hardhat quickstart (from chain/)
1) `npm init -y`
2) `npm install --save-dev hardhat @openzeppelin/contracts dotenv`
3) Create `hardhat.config.js`:
```js
require("dotenv").config();
const { SEPOLIA_RPC, HOLESKY_RPC, PRIVATE_KEY } = process.env;
module.exports = {
  solidity: "0.8.23",
  networks: {
    sepolia: { url: SEPOLIA_RPC, accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [] },
    holesky: { url: HOLESKY_RPC, accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [] }
  }
};
```
4) Compile: `npx hardhat compile`
5) Deploy sketch (`scripts/deploy.js`):
```js
const { ethers } = require("hardhat");
async function main() {
  const [deployer] = await ethers.getSigners();
  const Core = await ethers.deployContract("CoreValues");
  const Soul = await ethers.deployContract("SoulToken", [ethers.parseEther("1000000"), ethers.parseEther("1000000"), deployer.address]);
  const minDelay = 3600 * 24; // 1 day
  const Timelock = await ethers.deployContract("SentinelTimelock", [minDelay, [deployer.address], [deployer.address], deployer.address]);
  const Gov = await ethers.deployContract("SentinelGovernor", [Soul.target, Timelock.target, Core.target]);
  console.log({ core: Core.target, soul: Soul.target, timelock: Timelock.target, governor: Gov.target });
}
main().catch((e) => { console.error(e); process.exit(1); });
```
6) Run: `npx hardhat run scripts/deploy.js --network sepolia`
7) Save addresses to `chain/addresses.json` (template: `addresses.example.json`).

### Safety notes
- Keep CoreValues non-upgradeable; only metadata gate lives there.
- Use Timelock delay >0 and guardian proposers (sisters/guardian multisig if present).
- Never commit secrets; `.wallet/` and `.env` stay ignored.
