from exam_paper import exam_paper, question_part
from student_form import Create_form

def main():
    EP1 = exam_paper()
    EP1.from_file("phy_mock_2025")
    EP1.print_paper()
    Create_form(EP1)


if __name__ == "__main__":
    main()


