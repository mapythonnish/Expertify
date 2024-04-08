from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
class MasterAdmin(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
   
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^\+?91\d{10}$', message='Phone number must be a valid Indian phone number.')])
    
 
from django.db import models
from django.core.validators import RegexValidator
from django.db import models
   # Import FCMDevice for push notifications
from django.db.models.signals import post_save
from django.dispatch import receiver
 
 
class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    overview = models.TextField()
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^\+?91\d{10}$', message='Phone number must be a valid Indian phone number.')])
    alternate_phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?91\d{10}$', message='Phone number must be a valid Indian phone number.')])
     
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100)
    
 
    
    languages_spoken = models.CharField(max_length=100, blank=True)  # No choices here
    class_location = models.CharField(max_length=100, blank=True)  # No choices here
    
    full_address = models.TextField()

 
    
    time_slots_available = models.CharField(max_length=255)
     
 

    # Additional fields
    FITNESS_SPORTS = 'Fitness & Sports Experts'
    EVENT_EXPERTS = 'Event Experts'
    MUSIC_EXPERTS = 'Music Experts'
    BUSINESS_PROFESSIONALS = 'Business Professionals'
    LESSONS_TRAINING = 'Lessons and Training'
    BEAUTY = 'Beauty'
    OTHERS = 'Others'

    EXPERT_CATEGORIES = [
        (FITNESS_SPORTS, 'Fitness & Sports Experts'),
        (EVENT_EXPERTS, 'Event Experts'),
        (MUSIC_EXPERTS, 'Music Experts'),
        (BUSINESS_PROFESSIONALS, 'Business Professionals'),
        (LESSONS_TRAINING, 'Lessons and Training'),
        (BEAUTY, 'Beauty'),
        (OTHERS, 'Others'),
    ]
    
    expert_category = models.CharField(max_length=100, choices=EXPERT_CATEGORIES)
    total_experience = models.CharField(max_length=100)
    certifications = models.TextField()
    fees = models.CharField(max_length=100)
    certifications_upload = models.FileField(upload_to='certificates/')
    expertise_video_upload = models.FileField(upload_to='expertise_videos/')
    profile_picture = models.FileField(upload_to='profile_pictures/')
    insta_id = models.CharField(max_length=100)
    fb_id = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6, default='000000')

    
    @property
    def subcategory_choices(self):
        return self.SUBCATEGORIES.get(self.expert_category, [])
    
    subcategory = models.CharField(max_length=100, choices=[])


    SUBCATEGORIES = {
        FITNESS_SPORTS: [
            ('Fitness Trainer', 'Fitness Trainer'),
            ('Yoga Instructor', 'Yoga Instructor'),
            ('Zumba Instructor', 'Zumba Instructor'),
            ('Aerobics Instructor','Aerobics Instructor'),
            ('Physiotherapist', 'Physiotherapist'),
            ('Pilates Trainer', 'Pilates Trainer'),
            ('Sports Nutritionist ','Sports Nutritionist'),
            ('Sports Dietician', 'Sports Dietician'),
            ('Martial Arts Teacher', 'Martial Arts Teacher'),
            ('Tennis Coach', 'Tennis Coach'),
            ('chess  coach', 'Chess Coach'),
            ('Football  Coach', 'Football Coach'),
            ('Basketball Coach', 'Basketball Coach'),
            ('Cricket Coach', 'Cricket Coach'),
        ],
        EVENT_EXPERTS: [
            ('Catering', 'Catering'),
            ('DJ', 'DJ'),
            ('Master of ceremonies', 'Master of Ceremonies'),
            ('Wedding Photographer', 'Wedding Photographer'),
            ('Events  Planner', 'Events Planner'),
            ('Magician', 'Magician'),
            ('Video Editing','Video Editing'),
            ('Rock Band', 'Rock Band'),
            ('Ghazal band', 'Ghazal Band'),
            ('Guitarist Solo', 'Guitarist Solo'),
            ('Pop band', 'Pop Band'),
            ('Hindi Music Band', 'Hindi Music Band')
            # Add other subcategories for Event Experts
        ],
        MUSIC_EXPERTS: [
            ('Guitar', 'Guitar'),
            ('Tabla', 'Tabla'),
            ('Violin', 'Violin'),
            ('Vocals', 'Vocals'),
            ('Kathak','Kathak'),
            ('Drums', 'Drums'),
            ('Piano', 'Piano'),
            # Add other subcategories for Music Experts
        ],
        BUSINESS_PROFESSIONALS: [
            ('Architect', 'Architect'),
            ('Pest Control', 'Pest Control'),
            ('Landscape/Gardening' , 'Landscape/Gardening'),
            ('House Cleaning', 'House Cleaning'),
            ('CCTV','CCTV'),
            ('Security Guards', 'Security Guards'),
            ('Carpenter', 'Carpenter'),
            ('Plumber', 'Plumber'),
            ('Electrician', 'Electrician'),
            ('Painter','Painter'),
            ('Laptop Repair', 'Laptop Repair'),
            ('CA','CA'),
            ('Accounts','Accounts'),
            ('Interior Design', 'Interior Design'),
            ('Insurance Agent', 'Insurance Agent'),
            ('Barter', 'Barter'),
            ('Animation','Animation'),
            ('Electronic Security', 'Electronic Security'),
            ('Solar panel', 'Solar panel'),
            ('Civil Contractor', 'Civil Contractor'),
            # Add other subcategories for Business Professionals
        ],
        LESSONS_TRAINING: [
            ('School Class tutions', 'School Class tutions'),
            ('Career Counselling', 'Career Counselling'),
            ('English Speaking','English Speaking'),
            ('GRE', 'GRE'),
            ('Singing', 'Singing'),
            ('Exam Coaching', 'Exam Coaching'),
            ('Art class','Art class'),
            ('Acting class', 'Acting class'),
            ('Languages', 'Languages'),
            # Add other subcategories for Lessons and Training
        ],
        BEAUTY: [
            ('Hair Cut', 'Hair Cut'),
            ('Pedicure', 'Pedicure'),
            ('Manicure', 'Manicure'),
            ('Facial', 'Facial'),
            ('Massage', 'Massage'),
            ('Make up Artist', 'Make up Artist'),
            # Add other subcategories for Beauty
        ],
        OTHERS: [
            ('Counselling', 'Counselling'),
            ('Life Coach', 'Life Coach'),
            ('Photography', 'Photography'),
            ('Parenting Coach', 'Parenting Coach'),
            ('Graphic  designing', 'Graphic designing'),
            ('Reiki', 'Reiki'),
            ('Digital Marketing','Digital Marketing'),
            ('Astrologer', 'Astrologer'),
            ('Lawyers', 'Lawyers'),
            ('Photography','Photography'),
            ('Movers and Packers', 'Movers and Packers'),
            ('Web Designing', 'Web Designing'),
            ('Vastu Consultant', 'Vastu Consultant')
            # Add other subcategories for Others
        ],
    }
    
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set choices for subcategory based on expert_category
        self._meta.get_field('subcategory').choices = self.get_subcategory_choices()

    def get_subcategory_choices(self):
        # Get the subcategories based on the selected expert_category
        return self.SUBCATEGORIES.get(self.expert_category, [])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Certification(models.Model):
    expert = models.ForeignKey(Expert, related_name='certifications_set', on_delete=models.CASCADE)
    file = models.FileField(upload_to='certifications/')
 
from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

# models.py
from django.db import models

class Notification(models.Model):
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, default=1)
    message = models.TextField(default="Default message")  # Set a default message
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

 

