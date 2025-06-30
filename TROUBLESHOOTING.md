# 🔧 GitHub Actions Deployment Troubleshooting

## ❌ Current Error: "No access token available"

This error occurs when the `FLY_API_TOKEN` secret is not properly configured in your GitHub repository.

## 🛠️ **STEP-BY-STEP FIX**

### Step 1: Get Your Fly.io API Token

1. **Open your terminal/command prompt**
2. **Login to Fly.io** (if not already logged in):
   ```bash
   flyctl auth login
   ```
3. **Get your API token**:
   ```bash
   flyctl auth token
   ```
4. **Copy the entire token** (it will look like `fly_api_token_...`)

### Step 2: Add Token to GitHub Repository Secrets

1. **Go to your GitHub repository** (in your browser)
2. **Click on "Settings"** (in the repository navigation bar)
3. **In the left sidebar**, click **"Secrets and variables"** → **"Actions"**
4. **Click "New repository secret"**
5. **Fill in the form**:
   - **Name**: `FLY_API_TOKEN` (exactly as shown, case-sensitive)
   - **Secret**: [paste your token from Step 1]
6. **Click "Add secret"**

### Step 3: Verify the Secret is Added

You should see `FLY_API_TOKEN` listed in your repository secrets. It will show as `FLY_API_TOKEN` with a note about when it was updated.

### Step 4: Test the Deployment

1. **Make a small change** to any file (like adding a comment)
2. **Commit and push** to the main branch:
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```
3. **Check GitHub Actions**:
   - Go to your repository
   - Click the "Actions" tab
   - Watch the workflow run

## 🔍 **Additional Troubleshooting**

### If You Don't Have Fly.io CLI Installed:

**Windows (PowerShell)**:
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**macOS/Linux**:
```bash
curl -L https://fly.io/install.sh | sh
```

### If You Haven't Created a Fly.io App Yet:

1. **In your project directory**:
   ```bash
   flyctl launch
   ```
2. **Follow the prompts** to configure your app
3. **Don't deploy yet** - just configure
4. **Then get your token** and add it to GitHub secrets

### If the Token is Already Set But Still Failing:

1. **Delete the old secret** in GitHub
2. **Get a fresh token**:
   ```bash
   flyctl auth token
   ```
3. **Add the new token** to GitHub secrets
4. **Try deploying again**

## 📋 **Checklist**

Before trying again, ensure:

- [ ] ✅ Fly.io CLI is installed: `flyctl version`
- [ ] ✅ You're logged into Fly.io: `flyctl auth whoami`
- [ ] ✅ You have a fly.toml file in your repository
- [ ] ✅ FLY_API_TOKEN secret is set in GitHub repository secrets
- [ ] ✅ The secret name is exactly `FLY_API_TOKEN` (case-sensitive)
- [ ] ✅ You're pushing to the main branch

## 🎯 **Expected Workflow**

Once everything is set up correctly, here's what should happen:

1. **You push to main branch** 📤
2. **GitHub Actions runs tests** 🧪
3. **If tests pass, deployment starts** 🚀
4. **Fly.io receives your app** ☁️
5. **Your app is live!** 🌐

## 🆘 **Still Having Issues?**

1. **Check the GitHub Actions logs** for more specific error messages
2. **Run flyctl commands locally** to ensure they work:
   ```bash
   flyctl status
   flyctl deploy
   ```
3. **Verify your fly.toml configuration** is correct

## 🔗 **Useful Commands**

```bash
# Check if you're logged in
flyctl auth whoami

# Get a new token
flyctl auth token

# Test local deployment
flyctl deploy

# Check app status
flyctl status

# View app logs
flyctl logs
```

Once you've added the `FLY_API_TOKEN` secret to your GitHub repository, the automatic deployment should work! 🎉
