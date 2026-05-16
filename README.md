# AI Network Blocker for Windows

**Take back control. Decide when your AI-powered editors can talk to the cloud.**

## What is this?

AI Network Blocker is a simple, open-source Windows application that gives you an on/off switch to instantly cut internet access to all major AI coding assistants and their backend APIs. With one click, it prevents tools like VS Code with Copilot, Cursor, Windsurf, or Claude Desktop from sending your code, prompts, or data to external servers.

## Why is this necessary?

AI coding assistants have deep access to your files and system. When you stop using them, they often remain running in the background and can still communicate with the internet. This leaves an open channel you don't fully control.

AI Network Blocker was created to:
- **Ensure privacy** – block data exfiltration when you are not actively working with AI.
- **Prevent accidental sharing** – avoid unintentional uploads of sensitive code or information.
- **Give you peace of mind** – you decide the exact moment these tools are allowed to connect.
- **Be lightweight and transparent** – uses only the Windows hosts file. No background services, no complex firewall rules.

## How it works

When you click **"BLOCK AI"**, the application performs two actions in sequence:
1. Force-closes common AI editors (VS Code, Cursor, Windsurf, etc.).
2. Adds entries to the Windows hosts file that redirect all requests to the major AI providers (OpenAI, Anthropic, Google, GitHub Copilot, Meta, etc.) to `127.0.0.1`, effectively blocking them.

When you click **"UNBLOCK AI"**, it simply removes those specific entries from the hosts file, restoring normal internet access.

No data is sent anywhere. No telemetry. No network monitoring. Just a clean, deterministic kill switch.

## Supported targets

The default list blocks domains from:
- OpenAI (ChatGPT, API)
- Anthropic (Claude)
- GitHub Copilot & Microsoft Copilot
- Google Gemini & AI Studio
- Meta AI
- Mistral AI
- Perplexity, DeepSeek, Wordware, and more

You can easily modify the list by editing the `BLOCKLIST` dictionary at the top of the script.

## Usage

1. **Download** the latest `ai_blocker.exe` (or run the Python script directly).
2. **Run as Administrator** (right-click → "Run as administrator"). This is required to edit the hosts file.
3. Click the big button to toggle blocking on or off.

If you prefer to run from source:
```bash
python ai_blocker.py
```

## Requirements

- Windows 10/11
- Administrator privileges
- Python 3.x (only if running the script)

## Disclaimer

This tool modifies your system's hosts file. It only adds or removes lines containing the comment `# AI-Block` and will not touch other entries. Use at your own risk. Always make sure you have a backup of your hosts file before using any tool that edits it.

## Why open source?

Trust is everything. The code is deliberately short, fully commented, and easy to audit. No hidden surprises. You own your machine, you set the rules.

---

**Reclaim your sovereignty.**  
One click. Total control.
