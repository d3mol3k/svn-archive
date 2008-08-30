from django.http import HttpResponse
from django.conf import settings
from tah.tah_intern.models import Layer
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control
from django.views.generic.simple import direct_to_template

#---------------------------------------------------------------------
# a simple view that does nothing but showing the t@h homepage

@cache_control(max_age=36000)
def homepage(request):
  return  direct_to_template(request, template= 'homepage.html');


#---------------------------------------------------------------------
# Show the last 10 lines out of the logfile

@cache_control(no_cache=True)
def show_log(request):
  read_size=1200
  #TODO use a setting for the log file location?
  f = open(settings.LOGFILE, 'rU')
  offset = read_size
  f.seek(0, 2)
  file_size = f.tell()
  if file_size < offset:
    offset = file_size
  f.seek(-1*offset, 2)
  read_str = f.read(offset)
  # Remove newline at the end
  if read_str[offset - 1] == '\n':
    read_str = read_str[:-1]
  lines = read_str.split('\n')
  f.close()
  return HttpResponse("\n".join(lines[-10:]), mimetype="text/plain")


#---------------------------------------------------------------------
# currently unused function that returns the image data. It has bitrotted
def show(request,layer,x,y,z):
  retcode = 0
  file=("/var/www/osm/Tiles/Gfx/unknown.png","/var/www/osm/Tiles/Gfx/sea.png","/var/www/osm/Tiles/Gfx/sea.png","/var/www/osm/Tiles/Gfx/error.png")
  try:
    l = Layer.objects.get(name=layer)
  except ObjectDoesNotExist:
    retcode = 3

  image_data = open(file[retcode], "rb").read()
  return HttpResponse(image_data, mimetype="image/png")