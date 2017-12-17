
class Version:
    ANCESTOR = "ancestor"
    MINE = "mine"
    YOURS = "yours"

    @classmethod
    def iter_any(cls):
        yield cls.ANCESTOR
        yield cls.MINE
        yield cls.YOURS
