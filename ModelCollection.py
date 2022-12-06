



class ModelCollection():
    def get_value(d, key):
        for k, v in d.items():
            if k == key:
                return v
    def get_key(d, value):
        for k, v in d.items():
            if v == value:
                return k

