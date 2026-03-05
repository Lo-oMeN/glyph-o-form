# Security Protocol - Glyphobetics Protection Layer
## Security-Guardian Classification: LEVEL ALPHA

**Last Updated:** 2026-03-06  
**Encryption Standard:** AES-256-CBC with PBKDF2 (100,000 iterations)  
**Status:** 🔒 PROTECTION LAYERS ACTIVE

---

## 📋 Contents

1. [Encrypted Assets Inventory](#1-encrypted-assets-inventory)
2. [Decryption Procedures](#2-decryption-procedures)
3. [Dead Man's Switch (DMS)](#3-dead-mans-switch-dms)
4. [Security Checklist](#4-security-checklist)
5. [Emergency Protocols](#5-emergency-protocols)

---

## 1. Encrypted Assets Inventory

### Files Encrypted at Rest

All sensitive files are encrypted with AES-256-CBC and stored with `.enc` extension:

| Original File | Encrypted File | Size | Classification |
|--------------|----------------|------|----------------|
| `memory/2026-03-05.md` | `memory/2026-03-05.md.enc` | 4 KB | Memory Log |
| `glyphobetics_specification_v2.0.md` | `glyphobetics_specification_v2.0.md.enc` | 8.9 KB | Core Spec |
| `english_to_glyph_o_form_protocol.md` | `english_to_glyph_o_form_protocol.md.enc` | 14.7 KB | Protocol Spec |
| `thundering_grace_engine_map.md` | `thundering_grace_engine_map.md.enc` | 17 KB | Engine Map |
| `spirit_driven_language_research_synthesis.md` | `spirit_driven_language_research_synthesis.md.enc` | 47.2 KB | Research |
| `pattern_sower_output.md` | `pattern_sower_output.md.enc` | 20.9 KB | Output |
| `glyph_weaver_output.md` | `glyph_weaver_output.md.enc` | 8.3 KB | Output |
| `value_alchemist_output.md` | `value_alchemist_output.md.enc` | 72 KB | Output |

### Unencrypted Files (Safe to Remain)

These files remain unencrypted as they contain no sensitive research:

- `AGENTS.md` - General agent guidelines
- `BOOTSTRAP.md` - Bootstrap instructions
- `HEARTBEAT.md` - Heartbeat configuration
- `IDENTITY.md` - Public identity information
- `SOUL.md` - Core identity (non-sensitive)
- `TOOLS.md` - Tool notes
- `USER.md` - User preferences
- `glyphobetics_PUBLIC_README.md` - Public readme

---

## 2. Decryption Procedures

### 🔐 Location of Encryption Key

**Passphrase File:** `/root/.openclaw/workspace/.secure/passphrase.key`  
**Permissions:** 600 (owner read/write only)  
**Format:** Base64-encoded 48-byte random string

### Decryption Command

To decrypt a single file:

```bash
openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 \
  -in filename.md.enc \
  -out filename.md \
  -pass file:/root/.openclaw/workspace/.secure/passphrase.key
```

### Batch Decryption Script

```bash
#!/bin/bash
WORKSPACE="/root/.openclaw/workspace"
PASSPHRASE=$(cat "$WORKSPACE/.secure/passphrase.key")

cd "$WORKSPACE"

# Decrypt all .enc files
for enc_file in *.enc memory/*.enc; do
    if [ -f "$enc_file" ]; then
        output_file="${enc_file%.enc}"
        openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 \
            -in "$enc_file" -out "$output_file" -pass pass:"$PASSPHRASE"
        echo "Decrypted: $enc_file → $output_file"
    fi
done
```

### Re-encryption After Use

**IMPORTANT:** Always re-encrypt files after viewing/editing:

```bash
# Encrypt a single file
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 \
  -in filename.md -out filename.md.enc \
  -pass file:/root/.openclaw/workspace/.secure/passphrase.key

# Securely delete original
shred -vfz -n 3 filename.md
rm -f filename.md
```

### Verification

Verify decryption was successful:

```bash
# Check file type
file decrypted_file.md
# Should output: "ASCII text" or similar

# Check first few lines
head -5 decrypted_file.md
```

---

## 3. Dead Man's Switch (DMS)

### Overview

The Dead Man's Switch is designed to automatically publish all research to GitHub if there is no contact for **7 days**.

**Status:** ⚠️ DISARMED (prepared but not activated)

### Location

- **Script:** `/root/.openclaw/workspace/.secure/dead_mans_switch.sh`
- **Log:** `/root/.openclaw/workspace/.secure/dms.log`
- **Status Flag:** `/root/.openclaw/workspace/.secure/DMS_ARMED` (exists = armed)
- **Heartbeat:** `/root/.openclaw/workspace/.secure/last_heartbeat`

### How to Arm the DMS

**⚠️ WARNING:** Once armed, the switch will trigger after 7 days of silence unless manually aborted.

```bash
# Set GitHub configuration (required)
export GITHUB_REPO="username/repository"
export GITHUB_TOKEN="ghp_your_personal_access_token"
export GITHUB_BRANCH="main"

# Arm the switch
/root/.openclaw/workspace/.secure/dead_mans_switch.sh arm
```

### How to Abort/Reset the DMS

To prevent trigger and reset the 7-day timer:

```bash
# Option 1: Simple abort (resets timer)
/root/.openclaw/workspace/.secure/dead_mans_switch.sh abort

# Option 2: Full disarm (disables DMS entirely)
/root/.openclaw/workspace/.secure/dead_mans_switch.sh disarm
```

### How to Check Status

```bash
/root/.openclaw/workspace/.secure/dead_mans_switch.sh status
```

### How to Send Heartbeat (Prevent Trigger)

```bash
/root/.openclaw/workspace/.secure/dead_mans_switch.sh heartbeat
```

### What Happens When Triggered

1. DMS checks for `DMS_ARMED` flag
2. Compares current time with `last_heartbeat`
3. If elapsed time ≥ 7 days:
   - Decrypts all `.enc` files
   - Creates release package with all specs, code, and research
   - Publishes to configured GitHub repository
   - Logs all actions to `dms.log`
   - Automatically disarms after publication

---

## 4. Security Checklist

### Daily

- [ ] Verify `.secure/` directory permissions are 700
- [ ] Verify `passphrase.key` permissions are 600
- [ ] Confirm no plaintext sensitive files exist

### Weekly

- [ ] Review `dms.log` for any activity
- [ ] Verify heartbeat is current (if DMS armed)
- [ ] Check encrypted file integrity

### Monthly

- [ ] Rotate passphrase (decrypt all, re-encrypt with new key)
- [ ] Review and update GitHub token (if DMS armed)
- [ ] Audit access logs

---

## 5. Emergency Protocols

### Scenario: Compromised Passphrase

1. **Immediate:** Disarm DMS if armed
   ```bash
   /root/.openclaw/workspace/.secure/dead_mans_switch.sh disarm
   ```

2. **Regenerate passphrase:**
   ```bash
   openssl rand -base64 48 > /root/.openclaw/workspace/.secure/passphrase.key.new
   ```

3. **Decrypt all with old key, re-encrypt with new:**
   ```bash
   # Decrypt all
   for f in *.enc memory/*.enc; do
       openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
         -in "$f" -out "${f%.enc}" -pass file:/root/.openclaw/workspace/.secure/passphrase.key
   done
   
   # Re-encrypt with new key
   for f in *.enc; do
       plaintext="${f%.enc}"
       openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 \
         -in "$plaintext" -out "$f" -pass file:/root/.openclaw/workspace/.secure/passphrase.key.new
       shred -vfz -n 3 "$plaintext"
       rm -f "$plaintext"
   done
   
   # Replace old key
   mv /root/.openclaw/workspace/.secure/passphrase.key.new /root/.openclaw/workspace/.secure/passphrase.key
   chmod 600 /root/.openclaw/workspace/.secure/passphrase.key
   ```

### Scenario: Lost Passphrase

**⚠️ CRITICAL:** Without the passphrase, encrypted files are unrecoverable.

- Check for backups in secure offline storage
- If DMS is armed and triggered, files will be published to GitHub
- No recovery method exists from encrypted files alone

### Scenario: Unauthorized Access Detected

1. Disarm DMS immediately
2. Change GitHub token
3. Rotate passphrase
4. Review all encrypted files for tampering
5. Consider triggering DMS early if data must be preserved

### Scenario: Need Emergency Publication

To manually trigger the DMS:

```bash
# Set timestamp to 7+ days ago
echo $(( $(date +%s) - 604800 )) > /root/.openclaw/workspace/.secure/last_heartbeat

# Trigger check (will publish)
/root/.openclaw/workspace/.secure/dead_mans_switch.sh check
```

---

## 🔒 Security Contacts & Escrow

- **Passphrase Storage:** `/root/.openclaw/workspace/.secure/passphrase.key`
- **DMS Script:** `/root/.openclaw/workspace/.secure/dead_mans_switch.sh`
- **This Protocol:** `/root/.openclaw/workspace/SECURITY_PROTOCOL.md`

---

## Appendix: Technical Details

### Encryption Parameters

- **Algorithm:** AES-256-CBC
- **Key Derivation:** PBKDF2
- **Iterations:** 100,000
- **Salt:** Random 8-byte salt (automatically generated)
- **Passphrase Length:** 48 bytes (Base64 encoded)

### DMS Trigger Logic

```
IF armed AND (current_time - last_heartbeat) >= 604800 seconds (7 days):
    decrypt_all_files()
    prepare_package()
    publish_to_github()
    disarm()
```

---

*Document maintained by Security-Guardian cultivar*  
*Protocol Version: 1.0*
