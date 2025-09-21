# BioGraph Data Migration Strategy

## 🚨 **Critical Compatibility Issue**

### Current Situation:
- **Existing BioGraph**: Phone number authentication (Twilio OTP)
- **BiographRenaissance**: Email-based authentication (JWT)
- **User Model Mismatch**: Different field structures and authentication methods

### Migration Goals:
1. **Preserve all existing user data**
2. **Maintain phone number authentication** (users expect this)
3. **Enable seamless content access** for existing users
4. **Support both authentication methods** during transition

## 🔄 **Migration Strategy Options**

### Option 1: Hybrid Authentication (Recommended)
**Keep both phone and email authentication**

#### Implementation:
1. **Extend BiographRenaissance User Model** to support phone numbers
2. **Add phone authentication endpoints** alongside email auth
3. **Create migration script** to map existing users
4. **Maintain backward compatibility**

#### Benefits:
- ✅ Existing users can login with phone numbers
- ✅ New users can use email or phone
- ✅ Gradual migration path
- ✅ No data loss

### Option 2: Phone-to-Email Mapping
**Convert phone numbers to email addresses**

#### Implementation:
1. **Generate email addresses** from phone numbers (e.g., `+1234567890@biograph.phone`)
2. **Update authentication** to use generated emails
3. **Migrate user data** with new email mapping

#### Benefits:
- ✅ Single authentication method
- ✅ Cleaner user model
- ❌ Users need to know their "email" (phone-based)

### Option 3: Dual User System
**Run both systems in parallel**

#### Implementation:
1. **Keep existing BioGraph** for phone auth
2. **Use BiographRenaissance** for new features
3. **Sync data** between systems
4. **Gradual user migration**

#### Benefits:
- ✅ Zero disruption to existing users
- ✅ Can test new features
- ❌ Complex data synchronization
- ❌ Higher maintenance cost

## 🛠️ **Recommended Implementation: Option 1**

### Step 1: Extend BiographRenaissance User Model

```python
# BiographRenaissance/core/models.py
class User(AbstractUser):
    # Existing fields...
    email = models.EmailField(unique=True, null=True, blank=True)  # Make nullable
    
    # Add phone number support
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    country_code = models.CharField(max_length=5, default="1")
    is_phone_verified = models.BooleanField(default=False)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_user_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Update USERNAME_FIELD to support both
    USERNAME_FIELD = 'email'  # Primary login field
    
    def get_login_field(self):
        """Return the field used for login (email or phone)"""
        return self.email if self.email else f"+{self.country_code}{self.phone_number}"
```

### Step 2: Add Phone Authentication Views

```python
# BiographRenaissance/core/views.py
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def phone_register(request):
    """Phone number registration (similar to existing BioGraph)"""
    serializer = PhoneRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Send OTP via Twilio
        send_otp_to_phone(user.phone_number)
        return Response({'message': 'OTP sent to phone'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def phone_verify_otp(request):
    """Verify OTP and complete registration/login"""
    serializer = PhoneOTPSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Step 3: Create Data Migration Script

```python
# BiographRenaissance/migration_script.py
import pymongo
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Migrate users from old BioGraph to BiographRenaissance'
    
    def handle(self, *args, **options):
        # Connect to existing MongoDB
        client = pymongo.MongoClient("mongodb://your-existing-mongodb")
        db = client["BioGraphDemo"]
        
        # Get existing users
        old_users = db.authapp_usermodel.find({})
        
        migrated_count = 0
        for old_user in old_users:
            try:
                # Create new user
                new_user = User.objects.create(
                    username=old_user['username'],
                    phone_number=old_user['phone_number'],
                    country_code=str(old_user['country_code']),
                    first_name=old_user.get('name', ''),
                    profile_picture=old_user.get('profile_pic_url', ''),
                    migrated_from_old_system=True,
                    old_user_id=str(old_user['_id']),
                    is_phone_verified=True,  # Assume verified in old system
                )
                
                # Migrate user profile data
                UserProfile.objects.create(
                    user=new_user,
                    profile_visibility=self.map_privacy_setting(old_user.get('profile_settings', 'F')),
                    email_notifications=old_user.get('email_notification', {}).get('all', True),
                    push_notifications=old_user.get('push_notification', {}).get('all', True),
                )
                
                migrated_count += 1
                self.stdout.write(f"Migrated user: {old_user['username']}")
                
            except Exception as e:
                self.stdout.write(f"Error migrating user {old_user['username']}: {e}")
        
        self.stdout.write(f"Migration complete: {migrated_count} users migrated")
```

### Step 4: Migrate Biograph Content

```python
# BiographRenaissance/migrate_biographs.py
def migrate_biographs():
    """Migrate biograph content from old system"""
    old_biographs = db.biographapp_biographmodel.find({})
    
    for old_biograph in old_biographs:
        try:
            # Find corresponding user in new system
            new_user = User.objects.get(old_user_id=str(old_biograph['user_id']))
            
            # Create new biograph (when biograph models are added)
            new_biograph = BiographModel.objects.create(
                user=new_user,
                title=old_biograph['title'],
                record_text=old_biograph['record_text'],
                record_time=old_biograph['record_time'],
                # Map other fields...
                migrated_from_old_system=True,
                old_biograph_id=str(old_biograph['_id']),
            )
            
        except Exception as e:
            print(f"Error migrating biograph: {e}")
```

## 📋 **Migration Checklist**

### Pre-Migration:
- [ ] **Backup existing database** (MongoDB Atlas)
- [ ] **Backup S3 files** (audio/video content)
- [ ] **Test migration script** on small dataset
- [ ] **Verify Twilio credentials** work in new system

### During Migration:
- [ ] **Run user migration script**
- [ ] **Migrate biograph content**
- [ ] **Update file URLs** in database
- [ ] **Test phone authentication**
- [ ] **Verify content accessibility**

### Post-Migration:
- [ ] **Test existing user login** with phone numbers
- [ ] **Verify all biographs** are accessible
- [ ] **Check file uploads** work correctly
- [ ] **Monitor for errors** and user feedback

## 🔧 **Implementation Steps**

### 1. Update BiographRenaissance User Model
```bash
# Add phone number fields to User model
# Update serializers for phone authentication
# Add phone authentication views
```

### 2. Add Twilio Integration
```bash
# Install twilio: pip install twilio
# Add Twilio settings to BiographRenaissance
# Create phone verification views
```

### 3. Create Migration Scripts
```bash
# User migration script
# Biograph content migration
# File URL update script
```

### 4. Test Migration
```bash
# Test with small dataset
# Verify phone authentication works
# Check content accessibility
```

## 🎯 **Expected Outcome**

After migration:
- ✅ **Existing users** can login with phone numbers
- ✅ **All biograph content** is accessible
- ✅ **File uploads** work correctly
- ✅ **Social features** (friends, subscribers) preserved
- ✅ **Premium subscriptions** maintained
- ✅ **New users** can use email or phone authentication

## 🚨 **Risk Mitigation**

### Data Loss Prevention:
- **Full database backup** before migration
- **S3 file backup** with versioning
- **Rollback plan** if migration fails
- **Gradual migration** (migrate users in batches)

### User Experience:
- **Maintain existing login flow** (phone + OTP)
- **Preserve all user data** and relationships
- **Keep existing file URLs** working
- **Test thoroughly** before going live

This strategy ensures your existing users can seamlessly access their content while providing a modern, scalable foundation for future development.
