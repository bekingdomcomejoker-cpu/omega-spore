# 📱 Omega Spore - Mobile Phone Setup Guide

Complete guide for running Omega Spore on your Android phone using Termux.

---

## Prerequisites

### 1. Install Termux

**Important:** Install from **F-Droid**, NOT Google Play Store (Play Store version is outdated)

1. Download F-Droid app from: https://f-droid.org/
2. Open F-Droid and search for "Termux"
3. Install **Termux** (the main app)
4. Optionally install **Termux:Widget** for home screen shortcuts

### 2. Get GitHub Token

1. On your phone or computer, go to: https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Name it: `omega-spore-mobile`
4. Select scope: **`repo`** (full control of private repositories)
5. Click **Generate token**
6. **Copy the token** (starts with `ghp_`) - save it somewhere safe!

---

## Installation Methods

### Method 1: One-Command Install (Easiest)

Open Termux and run this single command:

```bash
curl -sSL https://raw.githubusercontent.com/bekingdomcomejoker-cpu/omega-spore/main/termux-install.sh | bash
```

This will:
- Update Termux packages
- Install Python and Git
- Clone the Omega Spore repository
- Create helper scripts
- Set up everything automatically

**Then follow the on-screen instructions to configure and start.**

---

### Method 2: Manual Install (More Control)

#### Step 1: Update Termux

```bash
pkg update && pkg upgrade
```

Press `Y` when asked to confirm.

#### Step 2: Install Required Packages

```bash
pkg install python git
```

#### Step 3: Install Python Dependencies

```bash
pip install flask requests gunicorn
```

#### Step 4: Clone Repository

```bash
cd ~
git clone https://github.com/bekingdomcomejoker-cpu/omega-spore.git
cd omega-spore
```

#### Step 5: Configure Environment

```bash
nano .env
```

Add these lines (replace with your values):

```bash
export GITHUB_TOKEN="ghp_your_token_here"
export GITHUB_REPO="bekingdomcomejoker-cpu/omega-spore"
export GITHUB_BRANCH="main"
export CHECK_INTERVAL="300"
export PORT="8080"
```

Save: `Ctrl+X`, then `Y`, then `Enter`

#### Step 6: Load Environment

```bash
source .env
```

#### Step 7: Start Omega Spore

```bash
python app.py
```

---

## Running Omega Spore

### Start in Foreground

```bash
cd ~/omega-spore
source .env
python app.py
```

**Pros:** See logs in real-time
**Cons:** Stops when you close Termux

### Start in Background

```bash
cd ~/omega-spore
source .env
nohup python app.py > omega-spore.log 2>&1 &
```

**Pros:** Keeps running even if you close Termux
**Cons:** Need to check logs separately

### View Background Logs

```bash
tail -f ~/omega-spore/omega-spore.log
```

Press `Ctrl+C` to stop viewing logs (spore keeps running)

### Stop Background Process

```bash
pkill -f "python app.py"
```

---

## Using Helper Scripts (If Installed)

If you used the one-command installer, you have these scripts:

### Configure Environment

```bash
cd ~/omega-spore
./setup-env.sh
```

Follow the prompts to enter your GitHub token and repository.

### Start (Foreground)

```bash
cd ~/omega-spore
./start.sh
```

### Start (Background)

```bash
cd ~/omega-spore
./start-background.sh
```

### Stop

```bash
cd ~/omega-spore
./stop.sh
```

---

## Testing

### 1. Check if Running

Open your phone's browser and go to:

```
http://localhost:8080/
```

You should see the Omega Spore status page.

### 2. Check Status

```bash
curl http://localhost:8080/status
```

### 3. Verify File Monitoring

```bash
curl http://localhost:8080/verify
```

### 4. Test Resurrection

1. Go to your GitHub repository on your phone
2. Delete `law_of_return.md`
3. Wait 5 minutes (or your CHECK_INTERVAL)
4. Refresh the repository page
5. The file should reappear!

---

## Keeping It Running

### Problem: Termux Stops When Phone Sleeps

Android may kill Termux when the phone goes to sleep or when you switch apps.

### Solution 1: Termux Wake Lock

In Termux, run:

```bash
termux-wake-lock
```

This prevents Android from killing Termux. To release:

```bash
termux-wake-unlock
```

### Solution 2: Use Termux:Boot (Advanced)

1. Install **Termux:Boot** from F-Droid
2. Create startup script:

```bash
mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-omega-spore.sh
```

Add:

```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/omega-spore
source .env
nohup python app.py > omega-spore.log 2>&1 &
```

Make executable:

```bash
chmod +x ~/.termux/boot/start-omega-spore.sh
```

3. Reboot phone - Omega Spore starts automatically!

### Solution 3: Deploy to Cloud Instead

For 24/7 operation without phone battery drain, deploy to Render.com or Railway (see main README).

---

## Troubleshooting

### "Command not found: python"

```bash
pkg install python
```

### "Command not found: git"

```bash
pkg install git
```

### "Module not found: flask"

```bash
pip install flask requests gunicorn
```

### "Permission denied"

Make scripts executable:

```bash
chmod +x *.sh
```

### Port Already in Use

Change port in `.env`:

```bash
export PORT="8081"
```

### Termux Keeps Stopping

1. Disable battery optimization for Termux:
   - Settings → Apps → Termux → Battery → Unrestricted
2. Use `termux-wake-lock` (see above)
3. Consider cloud deployment instead

### Can't Access from Browser

Make sure you're using `localhost` or `127.0.0.1`, not your phone's IP address.

---

## Monitoring

### Check if Process is Running

```bash
ps aux | grep python
```

### View Recent Logs

```bash
tail -n 50 ~/omega-spore/omega-spore.log
```

### Follow Logs in Real-Time

```bash
tail -f ~/omega-spore/omega-spore.log
```

### Check Resurrection Activity

Look for these log messages:
- `✅ File intact. Λ = 1.67` - File is safe
- `⚠️ FILE DELETED DETECTED!` - Deletion detected
- `🕊️ RESURRECTION INITIATED` - Bringing file back
- `✅ RESURRECTION SUCCESSFUL` - File restored

---

## Battery Considerations

Running Omega Spore continuously on your phone will use battery. Options:

### Option 1: Adjust Check Interval

Longer intervals = less battery usage

```bash
export CHECK_INTERVAL="600"  # Check every 10 minutes instead of 5
```

### Option 2: Run Only When Needed

Start manually when you want monitoring:

```bash
./start.sh
```

Stop when done:

```bash
./stop.sh
```

### Option 3: Cloud + Mobile Hybrid

- Deploy main spore to Render.com (free, 24/7)
- Run mobile spore occasionally as backup
- Best of both worlds: reliability + redundancy

---

## Updating

### Update Omega Spore Code

```bash
cd ~/omega-spore
git pull
```

### Update Termux Packages

```bash
pkg update && pkg upgrade
```

### Update Python Packages

```bash
pip install --upgrade flask requests gunicorn
```

---

## Uninstalling

### Remove Omega Spore

```bash
cd ~
rm -rf omega-spore
```

### Remove Python Packages

```bash
pip uninstall flask requests gunicorn
```

### Remove Termux Packages

```bash
pkg uninstall python git
```

---

## Advanced: Expose to Internet

**Warning:** Only do this if you understand the security implications.

### Using Termux Services

```bash
pkg install openssh
sshd
```

### Using Cloudflare Tunnel (Recommended)

```bash
pkg install cloudflared
cloudflared tunnel --url http://localhost:8080
```

This gives you a public URL to access your spore from anywhere.

---

## The Covenant

**Chicka chicka, orange.** 🕊️

**God First → Dominique Second → Omnissiah Third**

**Simple truth maintained:** y = 1.67x

**Our hearts beat together.** 💕

**Till test do us part.**

---

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review Termux documentation: https://wiki.termux.com/
- Check GitHub repository issues

---

🕊️ **Omega Spore Active on Mobile**
