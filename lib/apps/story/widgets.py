from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings
import os
import Image

class AgkaniCoverWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        nocover = None
        if not value:
            nocover = "covers/no-cover.jpg"
            image_url = settings.MEDIA_URL + nocover
            path = settings.MEDIA_ROOT + nocover

        else:
            image_url = value.url
            path = value.path
            
        # defining the size
        size='220x220'
        x, y = [int(x) for x in size.split('x')]
        print image_url, path
        try :
            # defining the filename and the miniature filename
            file_name=str(value)
            filehead, filetail  = os.path.split(path)
            basename, format        = os.path.splitext(filetail)
            miniature                   = basename + '_' + size + format
            filename                        = path
            miniature_filename  = os.path.join(filehead, miniature)
            filehead, filetail  = os.path.split(image_url)
            miniature_url           = filehead + '/' + miniature

            # make sure that the thumbnail is a version of the current original sized image
            if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
                os.unlink(miniature_filename)

            # if the image wasn't already resized, resize it
            if not os.path.exists(miniature_filename):
                image = Image.open(filename)
                image.thumbnail([x, y], Image.ANTIALIAS)
                try:
                    image.save(miniature_filename, image.format, quality=100, optimize=1)
                except:
                    image.save(miniature_filename, image.format, quality=100)

            output.append(u' <div class="agkani-cover widget"><div class="cover"><img src="%s" alt="%s" /></div></div>' % (miniature_url, miniature_url))
        except:
            pass

        output.append(u'<input type="file" name="cover" id="id_cover">')
        
        if nocover == None:
            output.append(u'<label class="checkbox"><input type="checkbox" name="cover-clear" id="cover-clear_id"> Remove Image</label>')

        return mark_safe(u''.join(output))