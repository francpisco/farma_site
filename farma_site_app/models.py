from PIL import Image, ImageOps
from django.db import models


class Servico(models.Model):
    """A Service offered by the farmacy"""
    title = models.CharField(max_length=75)
    image = models.ImageField(upload_to='imgs')
    text = models.TextField(max_length=200)
    position = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        """Override save method to resize image before saving to db."""

        super(Servico, self).save(*args, **kwargs)
        make_square_image(self.image)

    def __str__(self) -> str:
        return self.title


class Entry(models.Model):
    """A blog entry"""
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='imgs')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    text = models.TextField(max_length=1000)

    def save(self, *args, **kwargs):
        """Override save method in order to make images smaller and square."""
        super(Entry, self).save(*args, **kwargs)
        make_square_image(self.image)

    def __str__(self) -> str:
        return self.title



def make_square_image(image):
    """A function that takes an Imagefield and saves it square cropped and smaller"""
    try:
        with Image.open(image.path) as img:
            img = ImageOps.exif_transpose(img)
            w, h = img.size
            if w > h:
                cropped_img = _process_img(img, w, h, True)
            elif h > w:
                cropped_img = _process_img(img, h, w, False)
            else:
                return
            cropped_img.save(image.path)
    except IOError:
        print("Cannot open file", image.path)

def _process_img(img, larger, smaller, is_landscape):
        """A helper function to make images square and smaller."""
        excess = larger - smaller
        crop_value_1 = excess / 2
        crop_value_2 = crop_value_1 + smaller
        if is_landscape:
            cropped_img = img.crop((crop_value_1, 0, crop_value_2, smaller))
        else:
            cropped_img = img.crop((0, crop_value_1, smaller, crop_value_2))
        if smaller > 500:
            cropped_img = cropped_img.resize((500, 500), Image.ANTIALIAS)
        return cropped_img