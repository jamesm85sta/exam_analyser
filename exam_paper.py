class exam_paper:
    def __init__(self,paper_name):
        self.paper_name = paper_name
        self._questions = []
    
    def add_question(self, question):
        if not part:
            raise Exception("No part provided during add_question")
        if not isinstance(part,question_part) 
            raise Exception("provided question is not of type question_part")
        self._questions.append(question)

    def remove_question(self, question):
        if not part in self_subparts:
            raise Excetption("Question  not found within question in remove sub question")
        self._question.remove(question)

class question_part:
    def __init__(self, identifier, marks = None, categories=[]):
        self.identifier = identifier
        self.marks = marks
        self.categories = categories
        self._subparts = []

    def add_subpart(self, part):
        if not part:
            raise Exception("No part provided during add_subpart")
        if not isinstance(part,question_part) 
            raise Exception("provided question is not of type question_part")
        self._subparts.append(part)

    def remove_subpart(self, part):
        if not part in self_subparts:
            raise Excetption("Question part not found within question in remove sub part")
        self._subparts.remove(part)