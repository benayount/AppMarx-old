from django.forms import widgets
from django.template.defaultfilters import filesizeformat
from django.utils.safestring import mark_safe

class BlobWidget(widgets.FileInput):
    def render(self, name, value, attrs=None):
        try:
            blob_size = len(value)
        except:
            blob_size = 0

        blob_size = filesizeformat(blob_size)
        original = super(BlobWidget, self).render(name, value, attrs=None)
        return mark_safe('%s<p>Current size: %s</p>' % (original, blob_size))

class BlobField(models.Field):
    """
    A field for storing blobs of binary data.

    The value might either be a string (or something that can be converted to
    a string), or a file-like object.

    In the latter case, the object has to provide a ``read`` method from which
    the blob is read.
    """
    def get_internal_type(self):
        return 'BlobField'

    def formfield(self, **kwargs):
        # A file widget is provided, but use model FileField or ImageField
        # for storing specific files most of the time
        from django.forms import FileField
        defaults = {'form_class': FileField, 'widget': BlobWidget}
        defaults.update(kwargs)
        return super(BlobField, self).formfield(**defaults)

    def get_db_prep_value(self, value, connection, prepared=False):
        if hasattr(value, 'read'):
            return value.read()
        else:
            return str(value)

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        raise TypeError("BlobFields do not support lookups")

    def value_to_string(self, obj):
        return str(self._get_val_from_obj(obj))
