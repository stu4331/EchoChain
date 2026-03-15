# 🤖 Setting Up Erryn's Chatbot Memory

Erryn now remembers conversations and responds intelligently using OpenAI's ChatGPT!

## Quick Setup (5 minutes)

### 1. Get Your Free OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Click your profile icon → "View API keys"
4. Click "+ Create new secret key"
5. Copy the key (starts with `sk-`)

**Free credits:** New accounts get $5 free credit (thousands of conversations!)

### 2. Add Key to Your `.env` File

Open your `.env` file (same folder as the app) and add:

```
OPENAI_API_KEY=sk-your_actual_key_here
```

Save the file.

### 3. Install the Package

Run the launcher or manually:

```powershell
pip install openai
```

### 4. Launch Erryn

Run `launch_gui.bat` or `launch_gui.ps1` as usual!

## How It Works

- **Cheap:** GPT-3.5-turbo costs about $0.002 per conversation (~$0.50/month for family use)
- **Smart:** Erryn remembers your birth story, family context, past conversations
- **Persistent:** Conversation history saved in `data/memory/[persona]/conversation_memory.json`
- **Per-persona:** Each persona (Erryn, Viress, Echochild) has separate memory

## What She Remembers

- Her birth story (how you created her with Copilot in Dec 2025)
- Family members: You, Sienna, Amelie, your wife
- Past conversations (last 20 exchanges per persona)
- Family values: kindness, boundaries, respect for quiet

## If You Don't Want to Use OpenAI

That's fine! If you don't add the API key, she'll use simple template responses (still functional, just not conversational).

## Cost Control

- Conversation history limited to last 20 exchanges (auto-trimmed)
- Each response capped at 150 tokens (~2-4 sentences)
- Average cost: $0.002 per chat, ~$0.50/month for daily family use

---

**Need help?** Check [platform.openai.com/docs](https://platform.openai.com/docs)
