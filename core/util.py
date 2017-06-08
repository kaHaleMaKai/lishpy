class SingletonMeta(type):

    INSTANCE = None

    def __call__(cls, base_class=object, *args, **kwargs):
        if cls.INSTANCE is None:
            instance = base_class.__new__(cls, *args, **kwargs)
            instance.__init__(*args, **kwargs)
            cls.INSTANCE = instance
        return cls.INSTANCE
