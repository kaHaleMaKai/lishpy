class SingletonMeta(type):

    INSTANCE = None

    def __call__(cls, *args, **kwargs):
        if cls.INSTANCE is None:
            instance = object.__new__(cls)
            instance.__init__(*args, **kwargs)
            cls.INSTANCE = instance
        return cls.INSTANCE
