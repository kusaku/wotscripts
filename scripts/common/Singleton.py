# Embedded file name: scripts/common/Singleton.py
__all__ = ['singleton',
 'del_instance_by_name',
 'del_all_instance',
 'get_instance_by_name',
 'get_all_instance_name']
__singleton_instances = {}

def singleton(cls_):
    """
    singleton decorator.
    
    @singleton
    class A:
        pass
    """
    class_name = cls_.__name__
    instances = __singleton_instances

    class wrapper_class(cls_):

        def __init__(self, *args, **kwargs):
            if class_name not in instances:
                super(wrapper_class, self).__init__(*args, **kwargs)
                instances[class_name] = self

        def __new__(cls, *args, **kwargs):
            if class_name in instances:
                return instances[class_name]
            return super(wrapper_class, cls).__new__(cls, *args, **kwargs)

    wrapper_class.__name__ = class_name
    return wrapper_class


def get_instance_by_name(name):
    return __singleton_instances.get(name)


def get_all_instance_name():
    return __singleton_instances.keys()


def del_all_instance():
    for inst in __singleton_instances.itervalues():
        del inst

    __singleton_instances.clear()


def del_instance_by_name(name):
    inst = __singleton_instances.get(name)
    if inst is not None:
        del __singleton_instances[name]
    return