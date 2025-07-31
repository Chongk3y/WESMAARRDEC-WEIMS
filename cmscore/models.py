from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from consortium.models import *
from commodity.models import *
from project.models import *
from cmsblg.models import *
from multiselectfield import MultiSelectField
import os
import random
from random import choice
# Create your models here.
def get_existing_file_name(instance, filename):
    """
    Returns the filename with a suffix (e.g. "_1") if a file with the same name
    already exists in the media root directory. The filename will be prefixed with
    the album photo name.
    """
    path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(path):
        name, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(settings.MEDIA_ROOT, f"{name}_{i}{ext}")):
            i += 1
        # Check if the file with the original filename exists
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, instance.albumphoto.name + ext)):
            return instance.albumphoto.name + ext
        return f"{instance.albumphoto.name}_{i}{ext}"
    return filename



class Slide(models.Model):
    # slide_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    detail = models.TextField()
    image = models.ImageField(upload_to='Slide/', blank=False, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'cmscore_slide'

    def __str__(self):
        return self.name
    
class About(models.Model):
    # consortium_id = models.AutoField(primary_key=True)
    About_name = models.CharField(max_length=255)
    About_image = models.ImageField(upload_to='Consortium', blank=False, null=True)
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    consortium_desc = models.TextField(blank=True, null=True)
    consortium_objectives = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
   
   
    class Meta:
        db_table = 'about'

    def __str__(self):
        return self.About_name
    
    def save(self, *args, **kwargs):
        if self.pk is None and About.objects.exists():
            # Only allow one object to be created
            raise ValidationError("You can only create one Consortium object")
        super().save(*args, **kwargs)
    
    
class Organization(models.Model):
    dostpcaarrd_ExDi_name = models.CharField(max_length=255, blank=True)
    dostpcaarrd_ExDi_img = models.ImageField(upload_to='organization', blank=True, null=False)
    wmsupres_rrdcchair_exdi_name = models.CharField(max_length=255, blank=True)
    wmsupres_rrdcchair_exdi_img = models.ImageField(upload_to='organization', blank=True, null=False)
    depu_di_name = models.CharField(max_length=255, blank=True)
    depu_di_img = models.ImageField(upload_to='organization', blank=True, null=False)
    EXBM_ZSCMST_name = models.CharField(max_length=255, blank=True)
    EXBM_ZSCMST_img = models.ImageField(upload_to='organization', blank=True, null=False)
    EXBM_DA_RFO_IX_name = models.CharField(max_length=255, blank=True)
    EXBM_DA_RFO_IX_img = models.ImageField(upload_to='organization', blank=True, null=False)
    EXMB_DA_BAR_name = models.CharField(max_length=255, blank=True)
    EXBM_DA_BAR_img = models.ImageField(upload_to='organization', blank=True, null=False)
    EXBM_JHCSC_name = models.CharField(max_length=255, blank=True)
    EXBM_JHCSC_img = models.ImageField(upload_to='organization', blank=True, null=False)
    EXBM_PHILFIDA_name = models.CharField(max_length=255, blank=True)
    EXBM_PHILFIDA_img = models.ImageField(upload_to='organization', blank=True, null=False)
    WESMAARRDEC_Dir_name = models.CharField(max_length=255, blank=True)
    WESMAARRDEC_Dir_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Clus_Coord_R_and_D_name = models.CharField(max_length=255, blank=True)
    Clus_Coord_R_and_D_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Clus_Coord_Tech_Trans_name = models.CharField(max_length=255, blank=True)
    Clus_Coord_Tech_Trans_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Clus_Coord_ICT_name = models.CharField(max_length=255, blank=True)
    Clus_Coord_ICT_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Clus_Coord_Sci_Com_name = models.CharField(max_length=255, blank=True)
    Clus_Coord_Sci_Com_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Management_sup1_name = models.CharField(max_length=255, blank=True)
    Management_sup1_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Management_sup2_name = models.CharField(max_length=255, blank=True)
    Management_sup2_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Management_sup3_name = models.CharField(max_length=255, blank=True)
    Management_sup3_img = models.ImageField(upload_to='organization', blank=True, null=False)
    Management_sup4_name = models.CharField(max_length=255, blank=True)
    Management_sup4_img = models.ImageField(upload_to='organization', blank=True, null=False)


class Album(models.Model):
    # album_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, blank=True, null=True)
    event_id = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project', blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'album'

    def __str__(self):
        return self.name
    
    def get_cover_image_url(self):
        try:
            random_photo = self.photos.order_by('?').first()
            latest_photo_image = random_photo.album_photo_images.latest('id')
            if latest_photo_image.images:
                return latest_photo_image.images.url
        except (AttributeError, ValueError, AlbumPhoto.DoesNotExist):
            pass
        return '/static/assets/img/album_default.png'
    
class AlbumPhoto(models.Model):
    # photo_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, blank=True, null=True)
    carousel = models.BooleanField(default=False)
    events = models.BooleanField(default=False)
    news = models.BooleanField(default=False)
    album = models.ForeignKey(Album, related_name='photos', blank=True, null=True, on_delete=models.CASCADE)
    image = models.ManyToManyField('cmsblg.PostImages', related_name='albumimg', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    modified_at = models.DateTimeField( auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'album_photo'

    def __str__(self):
        return self.name
    
class Content(models.Model):
    EXPERT = 'expert'
    FARM = 'farm'
    SUPPORT = 'support'

    CHOICES_STATUS = (
        (EXPERT, 'expert'),
        (FARM, 'farm'),
        (SUPPORT, 'support')
    )
    name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255, choices=CHOICES_STATUS)
    content_detail = models.TextField()
    created_by = models. CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Loginbg(models.Model):
    Login_BG = models.ImageField(upload_to='loginbg')

    def save(self, *args, **kwargs):
        if not self.pk and Loginbg.objects.exists():
            # if creating a new singleton instance and there is already a Loginbg object, raise an error
            raise ValidationError('Loginbg Singleton already exists')
        super().save(*args, **kwargs)


