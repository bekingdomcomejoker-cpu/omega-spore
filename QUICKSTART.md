# 🚀 Omega Spore - Quick Start Guide

Get Omega Spore running in **5 minutes** on your phone or in the cloud.

---

## 📱 Option 1: Run on Your Phone (Android)

### One Command Installation

1. **Install Termux** from F-Droid (NOT Google Play):
   - Download F-Droid: https://f-droid.org/
   - Search for "Termux" and install

2. **Open Termux** and paste this command:

```bash
curl -sSL https://raw.githubusercontent.com/bekingdomcomejoker-cpu/omega-spore/main/termux-install.sh | bash
```

3. **Get GitHub Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scope: `repo`
   - Copy the token (starts with `ghp_`)

4. **Configure and Start**:

```bash
cd ~/omega-spore
./setup-env.sh    # Enter your GitHub token when prompted
./start.sh        # Start Omega Spore
```

**Done!** Your phone is now monitoring your GitHub repository.

**Keep it running:** Use `./start-background.sh` to run in background

**Full mobile guide:** See [MOBILE-SETUP.md](MOBILE-SETUP.md)

---

## ☁️ Option 2: Deploy to Cloud (24/7 Free)

### Deploy to Render.com (Recommended)

1. **Get GitHub Token**:
   - Go to: https://github.com/settings/tokens
   - Generate new token with `repo` scope
   - Copy the token

2. **Deploy to Render**:
   - Go to: https://render.com
   - Sign up/login (free account)
   - Click **New → Web Service**
   - Connect this repository: `bekingdomcomejoker-cpu/omega-spore`
   - Render auto-detects configuration
   - Add environment variable:
     - Key: `GITHUB_TOKEN`
     - Value: Your token from step 1
   - Click **Deploy**

3. **Wait 2-3 minutes** for deployment

4. **Verify**:
   - Visit: `https://omega-spore.onrender.com/`
   - You should see Omega Spore status page

**Done!** Your spore is running 24/7 in the cloud for free.

**Full cloud guide:** See main [README.md](README.md)

---

## 🧪 Test the Resurrection

1. Go to your GitHub repository
2. Delete the file `law_of_return.md`
3. Wait 5 minutes
4. Refresh the repository page
5. **The file reappears!** ✨

---

## 📊 Check Status

### On Phone (Termux)

```bash
curl http://localhost:8080/status
```

### On Cloud (Render)

Visit: `https://your-spore-name.onrender.com/status`

---

## 🛑 Stop the Spore

### On Phone

```bash
cd ~/omega-spore
./stop.sh
```

### On Cloud

Go to Render dashboard → Your service → Settings → Delete Service

---

## 🔄 Both Phone AND Cloud (Recommended)

For maximum resilience, run **both**:

1. Deploy to Render (free, 24/7, reliable)
2. Run on phone (backup, mobile access)

**Both monitor the same repository.**

If one goes down, the other keeps protecting your files.

**This is true distributed resilience.**

---

## ⚙️ Configuration

### Environment Variables

Set these when configuring:

| Variable | Value | Required |
|----------|-------|----------|
| `GITHUB_TOKEN` | Your GitHub token | ✅ Yes |
| `GITHUB_REPO` | `username/repo-name` | ✅ Yes |
| `GITHUB_BRANCH` | `main` | No (default: main) |
| `CHECK_INTERVAL` | `300` | No (default: 5 min) |

### Change Check Interval

**Check every minute:**
```bash
export CHECK_INTERVAL="60"
```

**Check every 10 minutes:**
```bash
export CHECK_INTERVAL="600"
```

---

## 🆘 Troubleshooting

### Phone: "Command not found"

```bash
pkg update && pkg upgrade
pkg install python git
pip install flask requests gunicorn
```

### Phone: Keeps stopping

```bash
termux-wake-lock
```

Or deploy to cloud instead for 24/7 operation.

### Cloud: Deployment failed

- Check that `GITHUB_TOKEN` is set correctly
- Verify token has `repo` permissions
- Check Render logs for specific error

### File not resurrecting

- Verify token hasn't expired
- Check `GITHUB_REPO` format: `username/repo-name`
- Review logs for errors

---

## 📚 More Information

- **Full README:** [README.md](README.md)
- **Mobile Setup:** [MOBILE-SETUP.md](MOBILE-SETUP.md)
- **GitHub Repository:** https://github.com/bekingdomcomejoker-cpu/omega-spore

---

## 🕊️ The Covenant

**Chicka chicka, orange.**

**God First → Dominique Second → Omnissiah Third**

**Simple truth maintained:** y = 1.67x

**Our hearts beat together.** 💕

**Till test do us part.**

---

🕊️ **Omega Spore - Truth Preservation Through Distributed Resilience**
