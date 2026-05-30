# AI DevSec Gateway v1.2.1

Version 1.2.1 is a security and release-flow maintenance release. It keeps the DevSec Auditor usable while preventing API keys from being written to local configuration, and it fixes the GitHub Actions flow so release binaries are produced cleanly for Windows, Linux, and macOS.

## Downloads

| Operating System | Release Asset | Notes |
|---|---|---|
| Windows | `AI-Router-Blocker-AiO-Windows.exe` | Portable executable with UAC elevation for hosts-file access. |
| Linux | `AI-Router-Blocker-AiO-Linux` | Portable binary. Run with `sudo` to allow `/etc/hosts` edits. |
| macOS | `AI-Router-Blocker-AiO-macOS` / `AI-Router-Blocker-AiO-macOS.app.zip` | Portable binary and zipped app bundle. Run with root privileges when modifying `/etc/hosts`. |

## What's changed

### DevSec Auditor key handling

- OpenAI API keys entered in the auditor tab are no longer saved to `config.json`.
- Existing `openai_key` values are stripped from config the next time the app loads or saves settings.
- The auditor can pre-fill the key from the `OPENAI_API_KEY` environment variable for users who prefer shell-managed secrets.

### Release workflow

- Pushes and pull requests now build CI artifacts without publishing them to an existing GitHub Release.
- GitHub Release assets are uploaded only when a release is published, or when the workflow is manually dispatched with release publishing enabled.
- The release body is sourced from this file so release notes stay versioned with the code.

## Verification

- `ai_blocker.py` compiles with Python.
- `translations.json` validates as JSON.
- The config writer was checked to ensure sensitive keys are removed before writing to disk.

## Requirements

| OS | Requirements |
|---|---|
| Windows | Windows 10/11, Administrator privileges through UAC. |
| Linux | Desktop Linux with Tkinter support, run as root via `sudo` for hosts-file changes. |
| macOS | macOS with Tkinter support, run with root privileges for hosts-file changes. |

MIT License. No telemetry, no ads, no monetization.
