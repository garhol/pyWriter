from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings
import os
import Image

class AgkaniCoverWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        image_url = value.url
        file_name=str(value)

        # defining the size
        size='220x220'
        x, y = [int(x) for x in size.split('x')]
        #try :
            # defining the filename and the miniature filename
        filehead, filetail  = os.path.split(value.path)
        basename, format        = os.path.splitext(filetail)
        miniature                   = basename + '_' + size + format
        filename                        = value.path
        miniature_filename  = os.path.join(filehead, miniature)
        filehead, filetail  = os.path.split(value.url)
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

        output.append(u' <div><input style="display:none" type="checkbox" name="cover-clear" id="cover-clear_id"><a href="#" target="_blank"><img src="%s" alt="%s" />X</a></div>' % (miniature_url, miniature_url))
        #except:
        #    print "BANG"
        #   pass
        output.append(u'<input type="file" name="cover" id="id_cover">')
        return mark_safe(u''.join(output))