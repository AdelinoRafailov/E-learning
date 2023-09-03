from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from colorfield.fields import ColorField

# Create your models here.
MATERIAL_CHOICES = (
    ("PDF", "PDF"),
    ("IMAGE", "IMAGE"),
    ("VIDEO", "VIDEO"),
    ("TEMPLATE", "TEMPLATE"),
)

TEMPLATE_CHOICES = (
    ("image.html", "image"),
    ("video.html", "video"),
    ("header-text.html", "header-text"),
)

QUESTIONS_CHOICES = (
    ("singlechoices", "singlechoices"),
)


class UserProfileElearning(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfileElearning.objects.create(user=instance)
    # class Meta:
    #     verbose_name_plural = "1- User profile"


class Subjects(models.Model):
    name = models.CharField(null=True, blank=True, max_length=30)
    content = models.TextField()
    img = models.ImageField(
        upload_to='elerning_subjects/', default='default.png')
    # class Meta:
    #     verbose_name_plural = "2. Subjects"

    def __str__(self):
        return self.name


class Jobs(models.Model):
    name = models.CharField(max_length=30)
    # class Meta:
    #     verbose_name_plural = "3. Jobs"

    def __str__(self):
        return self.name


class Courses(models.Model):
    name = models.CharField(blank=True, null=True, max_length=40,
                            unique=True, help_text="Add course name example:Python advance")
    subject = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, help_text="Select subjects")
    relatedJobs = models.ManyToManyField(Jobs)
    shortdes = models.TextField(verbose_name="Short description",
        max_length=250, default="", help_text="Short description is 250 Char long max,its appear on top of the course card")
    longdes = models.TextField(verbose_name="Long description",max_length=2000, default="",
                               help_text="long description is 2000 Char long max,its appear on Course view page")
    feature = models.TextField(max_length=1000, default='<div>\n\
    <p><i class="fa fa-alarm"></i>feature one</p>\n\
    <p><i class="bi bi-alarm"></i>feature two</p>\n</div>', help_text="HTML view of feature page")
    img = models.ImageField(verbose_name="Image",
        upload_to='elerning_course_img/', default='default.png')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    name = models.CharField(blank=True, null=True, max_length=40)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    # class Meta:
    #     verbose_name_plural = "5. Lecture"

    def getMaterial(self):
        return LectureMaterial.objects.filter(lecture=self.id).order_by('order')


class LectureMaterial(models.Model):
    name = models.CharField(default="matial name", max_length=50)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    materialType = models.CharField(max_length=20,
                                    choices=MATERIAL_CHOICES,
                                    default='1')
    materialFiles = models.FileField(upload_to='elerning_material/')
    template = models.CharField(max_length=20,
                                choices=TEMPLATE_CHOICES,
                                default='N/A')
    value_1 = models.TextField(default="N/A", max_length=1000)
    value_2 = models.TextField(default="N/A", max_length=1000)
    value_3 = models.TextField(default="N/A", max_length=1000)
    value_4 = models.TextField(default="N/A", max_length=1000)
    value_5 = models.TextField(default="N/A", max_length=1000)
    value_6 = models.TextField(default="N/A", max_length=1000)
    value_7 = models.TextField(default="N/A", max_length=1000)
    value_8 = models.TextField(default="N/A", max_length=1000)
    value_9 = models.TextField(default="N/A", max_length=1000)
    value_10 = models.TextField(default="N/A", max_length=1000)
    value_11 = models.TextField(default="N/A", max_length=1000)

    # class Meta:
    #     verbose_name_plural = "6. LectureMaterial"


# Enroll lecture
class CourseEnroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    timedelta = models.IntegerField(default=30)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.courses.name

    # class Meta:
    #     verbose_name_plural = "7. CourseEnroll"

# to trac progress we will save each lecture matrial done by the user


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    LectureMaterial = models.ForeignKey(
        LectureMaterial, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, blank=True)


class LectureEnroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.user, self.lecture.course.name, self.lecture.name

    # class Meta:
    #     verbose_name_plural = "8. LectureEnroll"


class LectureMaterialEnroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lectureMaterial = models.ForeignKey(
        LectureMaterial, on_delete=models.CASCADE)

    # class Meta:
    #     verbose_name_plural = "9. LectureMaterialEnroll"


class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return self.payment_type


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    courses_enroll = models.OneToOneField(
        CourseEnroll, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

# qiuz and question parts


class Questions(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    question = models.TextField()
    question_type = models.CharField(max_length=20,
                                     choices=QUESTIONS_CHOICES,
                                     default='1')

    def __str__(self):
        return self.question

    # class Meta:
    #     verbose_name_plural = "10. Questions"


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.TextField(max_length=30)
    optionI = models.CharField(max_length=30)
    optionII = models.CharField(max_length=30)
    optionIII = models.CharField(max_length=30)
    optionIIII = models.CharField(max_length=30)


class QuestionsTaken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, default="")
    answerStatus = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class newspasper(models.Model):
    email = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)


class Achievements(models.Model):
    pass


class ThemeUI(models.Model):
    navbar_fontSize = models.IntegerField(default=25)
    profile_counters = ColorField(default='#FF0000')


class Information(models.Model):
    location_one = models.CharField(max_length=50, default="The Binary Tower")
    location_two = models.CharField(
        max_length=50, default="32 Marasi Drive Street - Business Bay - Dubai")
    contact_number = models.CharField(
        max_length=50, default="+971 56 651 0454")
    logo = models.ImageField(
        upload_to='elerning_course_img/', default='defaultlogo.png')
    facebook = models.CharField(max_length=50, default="#")
    twitter = models.CharField(max_length=50, default="#")
    instagram = models.CharField(max_length=50, default="#")
