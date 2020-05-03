from django.db import models

from quiz.models import Student, Year_Level, User



class StudentProfile(models.Model):

    academic_level = [
        ('JHS', 'JHS'),
        ('SHS', 'SHS'),
    ]

    program = [
        ('ABM', 'ABM'),
        ('GAS', 'GAS'),
        ('ICT', 'ICT'),
        ('STEM', 'STEM')
    ]

    gender = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Choose your username')
    profile_picture = models.ImageField(verbose_name='Profile Picture', default='images/avatar.png', upload_to='profile_picture', blank=True)
    first_name = models.CharField(max_length=200, verbose_name='First Name', blank=False)
    middle_name = models.CharField(max_length=200, verbose_name='Middle Name', blank=False)
    last_name = models.CharField(max_length=200, verbose_name='Last Name', blank=False)
    birthday = models.DateField(auto_now_add=False, verbose_name='Birthday', blank=False, help_text='example : 01/20/2020')
    age = models.PositiveSmallIntegerField(verbose_name="Age", blank=False)
    address = models.CharField(max_length=200, verbose_name='Address', blank=False)
    mothers_name = models.CharField(max_length=200, verbose_name="Mother's Name", blank=False)
    fathers_name = models.CharField(max_length=200, verbose_name="Father's Name", blank=False)
    contact_no = models.IntegerField(verbose_name="Contact No", blank=False)
    email = models.CharField(max_length=200, verbose_name='Email Address', blank=False)
    section = models.ForeignKey(Year_Level, on_delete=models.CASCADE, verbose_name='Section')
    bio = models.CharField(max_length=3000, verbose_name='Your Bio', blank=False)
    academic_level = models.CharField(max_length=100, choices=academic_level, blank=False, verbose_name='Academic Level')
    program = models.CharField(max_length=100, choices=program, blank=False, verbose_name='Program')
    student_id = models.CharField(max_length=100, blank=False, verbose_name='Student ID')
    gender = models.CharField(max_length=100, choices=gender, blank=False, verbose_name='Gender')



    def __str__(self):
        return self.first_name
