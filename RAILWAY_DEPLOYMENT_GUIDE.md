# Railway Deployment Guide

## ✅ Environment Variables You Have (Keep These):

```
MONGODB_URI=mongodb+srv://admin:KiteFlyFour78*@biographrenaissance.zkfvhph.mongodb.net/BiographRenaissanceDB?retryWrites=true&w=majority
DEBUG=False
SECRET_KEY=django-insecure-!ner8+=ida8po7m^e!o8i_*zc^nduk)3o14(2ymx
```

## ❌ Environment Variables to DELETE:

```
DATABASE_URL=postgresql://postgres:veZWLgHJuvAZiLrTXuSmwApVHfOAWXuW@yamanote.proxy.rlwy.net:37817/railway
MONGO_CLONE_USERNAME=admin
MONGO_CLONE_PASSWORD=StrongerThan34$
MONGO_CLONE_CLUSTER=biographrenaissance.kmwgt23
MONGO_CLONE_DATABASE=biograph-preprod
```

## ✅ Environment Variables to ADD/UPDATE:

```
ALLOWED_HOSTS=*
```

## 🚀 Deployment Steps:

1. **Delete the PostgreSQL variables** (we're using MongoDB)
2. **Keep only the MongoDB variables** listed above
3. **Push your code to GitHub** (if not already done)
4. **Railway will auto-deploy** when you push changes

## 📱 After Deployment:

Your iOS app will connect to:
- **Production URL**: `https://biographrenaissance-production.up.railway.app/api/v1/biographs/migrated/`
- **Test endpoint**: `https://biographrenaissance-production.up.railway.app/api/v1/biographs/migrated/test/`

## 🔍 Test Your Deployment:

```bash
# Test the connection
curl https://biographrenaissance-production.up.railway.app/api/v1/biographs/migrated/test/

# Test user lookup
curl "https://biographrenaissance-production.up.railway.app/api/v1/biographs/migrated/find-user/?phone=8479873207"
```

## 📊 Expected Response:

```json
{
    "status": "connected",
    "database": "BiographRenaissanceDB",
    "users_count": 613,
    "biographs_count": 7060
}
```
