from recruitment_post import RecruitmentPost

class BaseParser():

    def __init__(self):
        pass

    def parse(self, source : str, message : str) -> list[RecruitmentPost]:
        return []