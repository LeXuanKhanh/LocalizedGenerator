class OutputModifyFile:
    language = ""
    paths: list[str] = []
    def __init__(self, dic: dict):
        self.language = dic["language"]
        self.paths = dic["paths"]