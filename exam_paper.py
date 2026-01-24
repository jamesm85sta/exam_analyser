import json

class exam_paper:
    def __init__(self,paper_name=None):
        self.paper_name = paper_name
        self._questions = []
    
    def add_question(self, question):
        if not question:
            raise Exception("No part provided during add_question")
        if not isinstance(question,question_part):
            raise Exception("provided question is not of type question_part")
        self._questions.append(question)

    def remove_question(self, question):
        if not part in self_subparts:
            raise Excetption("Question  not found within question in remove sub question")
        self._question.remove(question)

    def from_file(self,fname):
        try:
            with open(f"exam_data/{fname}.json","r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"File could not be opened {e}")
        self.identifier = fname
        self.parse_exam_json(data)

    def parse_exam_json(self,data):
        for k,v in data.items():
            qp = question_part(k)
            qp.parse_json(v)
            self.add_question(qp)


    def print_paper(self):
        for item in self._questions:
            item.print_question()

    def get_length(self):
        return len(self._questions)
    
    def get_question(self, number):
        return self._questions[number]


class question_part:
    def __init__(self, identifier, marks = None, categories=[]):
        self.identifier = identifier
        self.marks = marks
        self.categories = categories
        self._subparts = []

    def add_subpart(self, part):
        if not part:
            raise Exception("No part provided during add_subpart")
        if not isinstance(part,question_part):
            raise Exception("provided question is not of type question_part")
        self._subparts.append(part)

    def remove_subpart(self, part):
        if not part in self_subparts:
            raise Excetption("Question part not found within question in remove sub part")
        self._subparts.remove(part)
    
    def parse_json(self,data):
        for k, v in data.items():
            if isinstance(v,dict) and "marks" in v:
                qp= question_part(k,v["marks"],v["categories"])
                self.add_subpart(qp)
            elif isinstance(v,dict):
                qp = question_part(k)
                qp.parse_json(v)
                self.add_subpart(qp)

    def print_question(self, level =0):
        if self.marks is not None:
            print("\t"*level + f"({self.identifier}) {self.marks} mark {self.categories}")
        else:
            print("\t"*level + self.identifier+":")

            for item in self._subparts:
                item.print_question(level + 1)
        
        