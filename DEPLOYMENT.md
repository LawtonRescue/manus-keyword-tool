# MANUS Keyword Research Tool - Deployment Guide

This guide covers multiple deployment options for permanently hosting your keyword research tool.

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Why Railway?**
- Free tier available
- Automatic HTTPS
- Zero configuration needed
- GitHub integration
- Custom domain support

**Steps:**

1. **Push to GitHub** (if not already done):
```bash
cd /home/ubuntu/keyword-research-tool
git init
git add .
git commit -m "Initial commit"
gh repo create manus-keyword-tool --public --source=. --remote=origin --push
```

2. **Deploy to Railway**:
   - Visit https://railway.app
   - Sign up/Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy
   - Your app will be live at: `https://your-app.railway.app`

3. **Add Custom Domain** (Optional):
   - Go to Settings → Domains
   - Add your custom domain
   - Update DNS records as instructed

**Cost**: Free tier includes 500 hours/month ($5 credit)

---

### Option 2: Render

**Why Render?**
- Free tier with no credit card required
- Automatic SSL certificates
- Easy deployment from GitHub
- Good for production apps

**Steps:**

1. **Push to GitHub** (if not already done):
```bash
cd /home/ubuntu/keyword-research-tool
git init
git add .
git commit -m "Initial commit"
gh repo create manus-keyword-tool --public --source=. --remote=origin --push
```

2. **Deploy to Render**:
   - Visit https://render.com
   - Sign up/Login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will detect the `render.yaml` configuration
   - Click "Create Web Service"
   - Your app will be live at: `https://your-app.onrender.com`

3. **Custom Domain** (Optional):
   - Go to Settings → Custom Domain
   - Add your domain and configure DNS

**Cost**: Free tier available (spins down after inactivity)

---

### Option 3: Fly.io

**Why Fly.io?**
- Global edge deployment
- Free tier available
- Docker-based deployment
- Fast performance

**Steps:**

1. **Install Fly CLI**:
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login and Deploy**:
```bash
cd /home/ubuntu/keyword-research-tool
fly auth login
fly launch --name manus-keyword-tool
fly deploy
```

3. **Your app will be live at**: `https://manus-keyword-tool.fly.dev`

**Cost**: Free tier includes 3 shared VMs

---

### Option 4: Google Cloud Run

**Why Cloud Run?**
- Serverless and scalable
- Pay only for what you use
- Google infrastructure
- Free tier: 2 million requests/month

**Steps:**

1. **Install Google Cloud SDK**:
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

2. **Build and Deploy**:
```bash
cd /home/ubuntu/keyword-research-tool

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/keyword-tool

# Deploy to Cloud Run
gcloud run deploy keyword-tool \
  --image gcr.io/YOUR_PROJECT_ID/keyword-tool \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

3. **Your app will be live at the URL provided**

**Cost**: Free tier available, then pay-per-use

---

### Option 5: Heroku

**Why Heroku?**
- Well-established platform
- Easy deployment
- Many add-ons available

**Steps:**

1. **Install Heroku CLI**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Create Procfile**:
```bash
cd /home/ubuntu/keyword-research-tool
echo "web: python3 web_server.py" > Procfile
```

3. **Deploy**:
```bash
heroku login
heroku create manus-keyword-tool
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

4. **Your app will be live at**: `https://manus-keyword-tool.herokuapp.com`

**Cost**: Free tier discontinued, starts at $5/month

---

### Option 6: DigitalOcean App Platform

**Why DigitalOcean?**
- Simple deployment
- Predictable pricing
- Good documentation

**Steps:**

1. **Push to GitHub** (if not already done)

2. **Deploy via DigitalOcean**:
   - Visit https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Connect GitHub repository
   - Select branch and configure
   - Deploy

**Cost**: Starts at $5/month

---

### Option 7: Docker + VPS (Most Control)

**Why VPS?**
- Full control
- Best performance
- Can host multiple apps

**Steps:**

1. **Get a VPS** (DigitalOcean, Linode, Vultr, etc.)

2. **SSH into your server**:
```bash
ssh root@your-server-ip
```

3. **Install Docker**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

4. **Clone and Deploy**:
```bash
git clone https://github.com/yourusername/manus-keyword-tool.git
cd manus-keyword-tool
docker-compose up -d
```

5. **Setup Nginx Reverse Proxy** (for custom domain):
```bash
apt install nginx certbot python3-certbot-nginx

# Create Nginx config
cat > /etc/nginx/sites-available/keyword-tool << 'EOF'
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/keyword-tool /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Get SSL certificate
certbot --nginx -d yourdomain.com
```

**Cost**: $5-10/month for VPS

---

## 🔧 Environment Variables

For production deployments, you may want to set:

```bash
PORT=5000                    # Server port
PYTHON_VERSION=3.11.0       # Python version
```

---

## 🌐 Custom Domain Setup

### General Steps:

1. **Purchase a domain** (Namecheap, GoDaddy, Google Domains, etc.)

2. **Add DNS records**:
   - For Railway/Render/Fly: Add CNAME record pointing to their URL
   - For VPS: Add A record pointing to your server IP

3. **Configure in platform**:
   - Add custom domain in platform settings
   - Wait for DNS propagation (5-60 minutes)

---

## 📊 Monitoring & Maintenance

### Health Checks

All deployments include a health check endpoint:
```bash
curl https://your-domain.com/health
```

### Logs

**Railway**: View in dashboard
**Render**: View in dashboard
**Fly.io**: `fly logs`
**Cloud Run**: `gcloud run logs`
**Docker**: `docker logs manus-keyword-tool`

### Updates

To update your deployed app:

1. Make changes locally
2. Commit and push to GitHub
3. Platform will auto-deploy (if configured)

Or manually:
```bash
git push origin main
# Platform-specific deploy command
```

---

## 🔒 Security Considerations

### Production Checklist:

- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Set up rate limiting (if needed)
- [ ] Configure CORS if accessed from other domains
- [ ] Monitor for abuse
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Regular backups (if storing data)
- [ ] Keep dependencies updated

### Rate Limiting (Optional)

Add to `web_server.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| Railway | 500 hrs/month | $5/month | Quick deployment |
| Render | Yes (sleeps) | $7/month | Free hosting |
| Fly.io | 3 shared VMs | $1.94/month | Global edge |
| Cloud Run | 2M requests | Pay-per-use | Scalability |
| Heroku | No | $5/month | Established apps |
| DigitalOcean | No | $5/month | Predictable cost |
| VPS | No | $5-10/month | Full control |

---

## 🎯 Recommended Setup

**For Quick Start**: Railway or Render
**For Production**: Cloud Run or VPS
**For Learning**: Railway (easiest)
**For Scale**: Cloud Run or Kubernetes

---

## 🆘 Troubleshooting

### App won't start
- Check logs for errors
- Verify Python version (3.11+)
- Ensure all dependencies installed
- Check PORT environment variable

### Slow response
- Check server location (choose closer region)
- Enable caching
- Upgrade to paid tier

### Domain not working
- Wait for DNS propagation (up to 48 hours)
- Verify DNS records are correct
- Check platform domain settings

---

## 📞 Support

For deployment issues:
1. Check platform documentation
2. Review error logs
3. Search platform community forums
4. Contact platform support

---

## ✅ Post-Deployment Checklist

- [ ] App is accessible via HTTPS
- [ ] Health check endpoint works
- [ ] All API endpoints functional
- [ ] Web UI loads correctly
- [ ] Custom domain configured (if applicable)
- [ ] Monitoring set up
- [ ] Backups configured (if needed)
- [ ] Documentation updated with live URL

---

## 🎉 Success!

Once deployed, your keyword research tool will be permanently available at your chosen URL. Share it with your team or clients!

**Example URLs:**
- Railway: `https://manus-keyword-tool.railway.app`
- Render: `https://manus-keyword-tool.onrender.com`
- Fly.io: `https://manus-keyword-tool.fly.dev`
- Custom: `https://keywords.yourdomain.com`

Enjoy your permanently deployed keyword research tool! 🚀
