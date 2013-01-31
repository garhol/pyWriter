from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pyWriter.lib.apps.story.models import Story, Chapter, Scene, Character, Artifact, Location, Getfeed 

import os
import shutil
import zipfile
from django.template import loader, Context

@login_required
def print_epub(request, story=None):
    context = {}
    if story:
        st = get_object_or_404(Story, pk=story, user=request.user)
        context['story'] = st
 
        ebookpath = os.path.join(settings.STATIC_ROOT, "media", "epub", str(st.pk))
        filename  = "%s.epub" % st.title
        zippath = os.path.join(ebookpath, filename)
        if os.path.exists(ebookpath):
            shutil.rmtree(ebookpath)
        
        os.makedirs(ebookpath)
        myfile = os.path.join(ebookpath, "index.html")
        f = file(myfile, "w")
        content = "\
        <html xmlns=\"http://www.w3.org/1999/xhtml\"> \
        <head>\
           <title>%s</title>\
        </head>\
        <body> \
        <h1>%s</h1> \
        <h3>%s</h3> \
        </body>\
        </html>" % (st.title, st.title, st.author)
        f.write(content)
        f.close()      
                   
        filename  = "%s.epub" % st.title
        zippath = os.path.join(ebookpath, filename)
        epub = zipfile.ZipFile(zippath, 'w')

        # The first file must be named "mimetype"
        epub.writestr("mimetype", "application/epub+zip")


        if st.cover:
            coverimage = os.path.abspath(st.cover.path)
        else:
            nocoverpath = os.path.join(settings.STATIC_ROOT, "library/images/icons/no-cover.jpg")           
            coverimage = os.path.abspath(nocoverpath)

        mycover = os.path.join(ebookpath, "cover.html")           
        coverimagepath = os.path.join(ebookpath, "cover.jpg")
        shutil.copy(coverimage, coverimagepath)
            
        f = file(mycover, "w")
        content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> \
                    <html xmlns="http://www.w3.org/1999/xhtml"> \
                    <head> \
                    <title>Cover</title> \
                    <style type="text/css"> img { max-width: 100%%; } </style> \
                    </head> \
                    <body> \
                    <div id="cover-image"> \
                    <img src="cover.jpg" alt="%s"/> \
                    </div> \
                    </body> \
                    </html>' % (st.title)
        f.write(content)
        f.close()   

        html_files = []

        html_files.append(myfile)

        counter = 0
        if st.get_chapters:
            for c in st.get_chapters:
                if c.get_scenes:
                    counter = counter+1
                    myfile = os.path.join(ebookpath, "%s.html" % str(counter))
                    f = file(myfile, "w")
                    content = "\
                    <html xmlns=\"http://www.w3.org/1999/xhtml\"> \
                    <head>\
                       <title>%s</title>\
                    </head>\
                    <body> \
                    <h1>%s</h1> \
                    </body>\
                    </html>" % (c, c)
                    f.write(content)
                    f.close()
                    html_files.append(myfile)
                    
                    for sc in c.get_scenes:
                        counter = counter+1
                        myfile = os.path.join(ebookpath, "%s.html" % str(counter))
                        f = file(myfile, "w")
                        content = "\
                        <html xmlns=\"http://www.w3.org/1999/xhtml\"> \
                        <head>\
                           <title>%s</title>\
                        </head>\
                        <body> \
                        <h1>%s</h1> \
                        %s \
                        </body>\
                        </html>" % (sc, sc, sc.content)
                        f.write(content)
                        f.close()
                        html_files.append(myfile)
                                
        # We need an index file, that lists all other HTML files
        # This index file itself is referenced in the META_INF/container.xml
        # file
        epub.writestr("META-INF/container.xml", '''<container version="1.0"
                   xmlns="urn:oasis:names:tc:opendocument:xmlns:container"> 
          <rootfiles>
            <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
          </rootfiles>
        </container>''');

        # The index file is another XML file, living per convention
        # in OEBPS/Content.xml
        index_tpl = '''<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="bookid" version="2.0"> 
          <metadata>
            <dc:title>%(title)s</dc:title>
            <dc:creator>%(author)s</dc:creator>
            <dc:identifier id="bookid">urn:isbn:%(uniqueid)s</dc:identifier>
            <dc:language>en-GB</dc:language>
            <meta name="cover" content="cover-image"/>
          </metadata>
          <manifest>
            %(manifest)s
          </manifest>
          <spine toc=\"ncx\">
            %(spine)s
          </spine>
          %(guide)s
        </package>'''

        manifest = ""
        spine = ""
        navmapcontent = ""

        toccontent = '''<?xml version='1.0' encoding='utf-8'?>
        <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                         "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
          <head>
            <meta name="dtb:uid"
        content="%(uniquething)s"/>
            <meta name="dtb:depth" content="1"/>
            <meta name="dtb:totalPageCount" content="0"/>
            <meta name="dtb:maxPageNumber" content="0"/>
          </head>
          <docTitle>
            <text>%(toctitle)s</text>
          </docTitle>
          <navMap>
          %(navmap)s
          </navMap>
        </ncx>
        '''
    
        manifest += '<item id="cover" href="cover.html"  media-type="application/xhtml+xml" />'
        manifest += '<item id="cover-image" href="cover.jpg" media-type="image/jpeg"/>'
        spine += '<itemref idref="cover" linear="no"/>'
        epub.write(coverimagepath, 'OEBPS/cover.jpg')
        mycoverpath = os.path.join(ebookpath, "cover.html")
        epub.write(mycoverpath, 'OEBPS/cover.html')
        guide = '''
            <guide> 
                <reference type="cover" title="Cover Image" href="cover.html" /> 
            </guide>
          '''
        navmapcontent += '''
        <navPoint id="navpoint-1" playOrder="1">
          <navLabel>
            <text>Book cover</text>
          </navLabel>
          <content src="cover.html"/>
        </navPoint>
        '''

        # Write each HTML file to the ebook, collect information for the index
        for i, html in enumerate(html_files):
            basename = os.path.basename(html)
            manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
                          i+1, basename)
            spine += '<itemref idref="file_%s" />' % (i+1)
            navmapcontent += '''
            <navPoint id="navpoint-%s" playOrder="%s">
              <navLabel>
                <text>%s</text>
              </navLabel>
              <content src="%s"/>
            </navPoint>
            ''' % (i+2, i+2, i+2, basename)
            
            epub.write(html, 'OEBPS/'+basename)

        uniquestring = "%s%s" % (st.title, st.author)
        
         # todo TOC
        mytoc = os.path.join(ebookpath, "toc.ncx")
        f = file(mytoc, "w")
        f.write(toccontent % {
          'toctitle': st.title,
          'navmap': navmapcontent,
          'uniquething' : uniquestring,
        })
        f.close()
        epub.write(mytoc, 'OEBPS/toc.ncx')
        #f = file(mytoc, "r")
        #s = f.read()
        #assert 0, s
        
        tocmanifest = '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'
        manifest += tocmanifest
        
        # Finally, write the index
        epub.writestr('OEBPS/Content.opf', index_tpl % {
          'uniqueid': uniquestring,
          'title': st.title,
          'author': st.author,
          'manifest': manifest,
          'spine': spine,
          'guide' : guide,
        })
        
            
        

    context['booklink'] = zippath

    template = 'printing/print_epub.html'
    return render_to_response(template, context, context_instance=RequestContext(request))  
