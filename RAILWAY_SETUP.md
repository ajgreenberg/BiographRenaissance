# 🚂 Railway Setup Guide for BiographRenaissance

## 📋 Prerequisites
- Railway account (free at [railway.app](https://railway.app))
- GitHub account (to connect your repository)

## 🚀 Step-by-Step Deployment

### 1. **Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Verify your email

### 2. **Create New Project**
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select your BiographRenaissance repository

### 3. **Add PostgreSQL Database**
1. In your Railway project dashboard
2. Click "New" → "Database" → "PostgreSQL"
3. Wait for database to be created
4. Railway will automatically provide `DATABASE_URL` environment variable

### 4. **Configure Environment Variables**
Add these environment variables in Railway dashboard:

```
RAILWAY_ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app
```

### 5. **Deploy**
1. Railway will automatically deploy when you push to GitHub
2. Or click "Deploy" button in Railway dashboard
3. Wait for deployment to complete

## 💰 **Cost Breakdown**

### Railway Pricing:
- **PostgreSQL Database**: $5/month (1GB storage)
- **Web Service**: $5/month (512MB RAM)
- **Total**: **$10/month** (vs MongoDB Atlas $57/month)

### Savings: **$47/month** (564% cheaper!)

## 🔧 **Local Development**

Your app automatically detects environment:
- **Local**: Uses SQLite (`db.sqlite3`)
- **Railway**: Uses PostgreSQL (via `DATABASE_URL`)

## 📊 **Migration Commands**

Once deployed, run migrations:
```bash
# In Railway console or locally with Railway CLI
python manage.py migrate
python manage.py createsuperuser
```

## 🌐 **Access Your App**

After deployment:
- **App URL**: `https://your-app-name.railway.app`
- **Admin**: `https://your-app-name.railway.app/admin/`
- **API**: `https://your-app-name.railway.app/api/v1/`
- **Swagger**: `https://your-app-name.railway.app/swagger/`

## 🔄 **Database Migration from SQLite**

To migrate your existing SQLite data to Railway PostgreSQL:

1. **Export from SQLite**:
```bash
python manage.py dumpdata --natural-foreign --natural-primary > data.json
```

2. **Import to PostgreSQL** (after Railway deployment):
```bash
python manage.py loaddata data.json
```

## 🚨 **Important Notes**

- Railway automatically handles SSL certificates
- Database backups are included
- Auto-scaling based on traffic
- Zero-downtime deployments
- Built-in monitoring and logs

## 🆘 **Troubleshooting**

### Common Issues:
1. **Database connection**: Check `DATABASE_URL` environment variable
2. **Migration errors**: Run `python manage.py migrate` in Railway console
3. **Static files**: Add `whitenoise` for static file serving
4. **Environment variables**: Ensure all required vars are set

### Railway CLI (Optional):
```bash
npm install -g @railway/cli
railway login
railway link
railway up
```

## 🎯 **Next Steps After Deployment**

1. ✅ Test API endpoints
2. ✅ Migrate user data from MongoDB clone
3. ✅ Test phone authentication
4. ✅ Set up custom domain (optional)
5. ✅ Configure monitoring alerts

---

**Total Setup Time**: ~15 minutes
**Monthly Cost**: $10 (vs $57 for MongoDB Atlas)
**Savings**: $564/year! 🎉
