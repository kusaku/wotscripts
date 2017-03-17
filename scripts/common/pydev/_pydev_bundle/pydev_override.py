# Embedded file name: scripts/common/pydev/_pydev_bundle/pydev_override.py


def overrides(method):
    """
    Initially meant to be used as
    
    class B:
        @overrides(A.m1)
        def m1(self):
            pass
            
    but as we want to be compatible with Jython 2.1 where decorators have an uglier syntax (needing an assign
    after the method), it should now be used without being a decorator as below (in which case we don't even check
    for anything, just that the parent name was actually properly loaded).
    
    i.e.:
    
    class B:
        overrides(A.m1)
        def m1(self):
            pass
    """
    pass


def implements(method):
    pass