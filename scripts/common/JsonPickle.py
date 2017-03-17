# Embedded file name: scripts/common/JsonPickle.py
import Math
import inspect
import json

def classNameFormatter(ob):
    """Get unique class name of ob including module name."""
    cls = inspect.isclass(ob) and ob or ob.__class__
    return '%s.%s' % (cls.__module__, cls.__name__)


def mathVectorArgs(ob):
    """Returns list of args to init ob of Math.Vector's types."""
    return ob.list()


DEFAULT_CLASSES_ENCODER = {Math.Vector3: {'__class__': classNameFormatter,
                'args': mathVectorArgs},
 Math.Vector4: {'__class__': classNameFormatter,
                'args': mathVectorArgs},
 Math.Vector2: {'__class__': classNameFormatter,
                'args': mathVectorArgs},
 tuple: {'__class__': classNameFormatter,
         'args': lambda ob: [list(ob)]},
 dict: {'__class__': classNameFormatter,
        'args': lambda ob: [[ [key, ob[key]] for key in ob ]]},
 set: {'__class__': classNameFormatter,
       'args': lambda ob: [list(ob)]}}
DEFAULT_CLASSES_DECODER = dict([ (DEFAULT_CLASSES_ENCODER[cls]['__class__'](cls), cls) for cls in DEFAULT_CLASSES_ENCODER ])
C_TO_PY_CLASSES_MATCH = {'PyFixedDictDataInstance': dict,
 'PyArrayDataInstance': list}

def object_hook(dct):
    """Convert special dicts with '__class__' key to Python objects using DEFAULT_CLASSES_DECODER
    settings and args and kw to init object."""
    if '__class__' in dct:
        return DEFAULT_CLASSES_DECODER[dct['__class__']](*dct['args'], **dct.get('kw', {}))
    return dct


def __searchcusomobject(ob, cls = None):
    """Convert object ob to JSON ready structure using DEFAULT_CLASSES_ENCODER settings."""
    if not isinstance(ob, dict) or '__class__' not in ob:
        cls = cls or ob.__class__
        if cls in DEFAULT_CLASSES_ENCODER:
            return dict([ (key, f(ob)) for key, f in DEFAULT_CLASSES_ENCODER.get(cls).items() ])
    return ob


def convertDumps(ob):
    """Converts object ob before calling by json.dumps."""
    ob = __searchcusomobject(C_TO_PY_CLASSES_MATCH.get(ob.__class__.__name__, lambda x: x)(ob))
    if isinstance(ob, dict):
        ob = {k:convertDumps(v) for k, v in ob.iteritems()}
    elif isinstance(ob, list):
        ob = [ convertDumps(item) for item in ob ]
    return ob


def str_scanstring(s):
    """Encodes string s from utf-8 after json loads"""
    if isinstance(s, basestring):
        s = s.encode('utf-8')
    return s


def convertLoads(ob):
    """Converts object ob return by json.loads. In fact recursively search strings and call str_scanstring"""
    if isinstance(ob, dict):
        ob = dict(((convertLoads(k), convertLoads(v)) for k, v in ob.iteritems()))
    elif isinstance(ob, list):
        ob = [ convertLoads(item) for item in ob ]
    elif isinstance(ob, tuple):
        ob = tuple((convertLoads(item) for item in ob))
    return str_scanstring(ob)


def loads(s, *args, **kw):
    """ Convert string to python object."""
    return convertLoads(json.loads(s, object_hook=object_hook))


def dumps(ob, *args, **kw):
    """Convert Python object to string."""
    return json.dumps(convertDumps(ob), separators=(',', ':'))