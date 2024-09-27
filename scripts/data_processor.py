import os
from bs4 import BeautifulSoup
from typing import List, Dict
import json
HISTORY_COURSES=[
    "中国共产党历史",
    "社会主义发展史",
    "新中国史",
    "改革开放史"
]
ZZ_COURSES=["形势与政策","国家安全导论","军事理论"]

MATH_COURSE=["一元微积分","多元微积分与线性代数"]

class Course:
    def __init__(self, name: str, credits: float, type: str = '必修'):
        """
        初始化课程对象。

        :param name: 课程名称
        :param credits: 课程学分
        :param type: 课程类型（必修或选修）
        """
        self.name = name
        self.credits = credits
        self.type = type
        self.is_selected=False
        self.is_gen=False
        self.is_phy=False
    def __repr__(self):
        """
        用于打印课程的便捷显示。
        """
        return f"Course(Name: {self.name}, Credits: {self.credits}, Type: {self.type})"
    def is_selected_process(self ,major:str=""):
        input_string=self.name
        course_code = input_string.split('[')[1].split(']')[0]  # 获取[]中的内容
        course_name = input_string.split(']')[1]  # 获取]后的内容
        course_code_num=(int)(course_code[-4:])
        print(course_code_num)
        if(course_code.startswith("EDU")):
            self.is_selected=True
        if(course_code.startswith("GEN")):
            self.is_gen=True
        if(course_name=="博雅英语听说" or course_name=="通用英语进阶" or course_name=="思辨英语读写" or course_name=="人文通识课程群/学业用途英语课程群"):
            self.is_selected=True
        if(course_code_num>=1201 and course_code_num<=1250):
            self.is_phy=False
        for COURSE in ZZ_COURSES:    
            if(course_name.startswith(COURSE)):
                self.is_selected=True
        for COURSE in HISTORY_COURSES:    
            if(course_name.startswith(COURSE)):
                self.is_selected=True
        for COURSE in MATH_COURSE:    
            if(course_name.startswith(COURSE) and major=="教育技术学"):
                self.is_selected=True
class Score:
    def __init__(self, course_name: str, type: str, score: str) -> None:
        self.course_name = course_name
        self.type = type
        if score in ['及格', '不及格', '合格', '不合格']:
            self.score = score
        else:
            self.score = float(score)

    def __repr__(self) -> str:
        return f"Score(course_name: {self.course_name}, score: {self.score})"

class Student:
    def __init__(self, index: int, name: str, student_id: str) -> None:
        self.name = name
        self.id = student_id  # 这里应该是 student_id
        self.scores: List[Score] = []
        self.has_failed_course = False
        self.index = index

    def add_score(self, score: Score):
        self.scores.append(score)
        if isinstance(score.score, float) and score.score < 60 and score.score!=0:  # 假设60分为及格线
            self.has_failed_course = True

    def __str__(self) -> str:
        scores_str = '\n'.join([f"{score.course_name}: {score.score}" for score in self.scores])
        return (f"Student(index={self.index}, name={self.name}, student_id={self.id}, "
                f"scores=[{scores_str}], has_failed_course={self.has_failed_course})")

class Major:
    def __init__(self, grade: str, name: str, courses: List[Course],students:List[Student]):
        """
        初始化专业对象，包含课程列表。

        :param grade: 年级
        :param name: 专业名称
        :param courses: 课程列表
        """
        self.grade = grade
        self.name = name
        self.courses = courses
        self.students: List[Student] = students

    def add_student(self, student: Student):
        self.students.append(student)

    def to_json(self) -> dict:
        """将专业信息转换为 JSON 格式"""
        major_data = {
            'grade': self.grade,
            'name': self.name,
            'courses': [
                {
                    'name': course.name,
                    'credits': course.credits,
                    'type': course.type,
                    'is_selected': course.is_selected,
                    'is_gen': course.is_gen,
                    'is_phy': course.is_phy
                } for course in self.courses
            ],
            'students': [
                {
                    'index': student.index,
                    'name': student.name,
                    'student_id': student.id,
                    'has_failed_course': student.has_failed_course,
                    'scores': [
                        {
                            'course_name': score.course_name,
                            'type': score.type,
                            'score': score.score
                        } for score in student.scores
                    ]
                } for student in self.students
            ]
        }
        return major_data

    def __str__(self) -> str:
        courses_str = ', '.join([course.name for course in self.courses])
        students_str = '\n'.join([str(student) for student in self.students])
        return (f"Major(name={self.name}, grade={self.grade}, "
                f"courses=[{courses_str}], students=[{students_str}])")

def read_tables_from_folder(data_path: str) -> List[Dict[str, List[List[str]]]]:
    """
    读取指定文件夹中的所有 HTML 文件，解析每个文件中的表格项并返回。

    :param data_path: 文件夹路径
    :return: 一个包含所有表格项数据的列表，每个元素是一个字典，包含文件名和表格数据
    """
    tables_data: List[Dict[str, List[List[str]]]] = []  # 用于存储所有文件的表格数据

    # 获取文件夹中的所有文件
    files: List[str] = os.listdir(data_path)
    print(f"Files in the directory: {files}")

    # 遍历每个文件
    for filename in files:
        file_path: str = os.path.join(data_path, filename)

        # 确保是文件并且是HTML文件
        if os.path.isfile(file_path) and filename.endswith('.xls'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content: str = file.read()

            # 使用 BeautifulSoup 解析 HTML 文件
            soup = BeautifulSoup(content, 'lxml')
            table_data: List[List[str]] = []

            # 查找所有表格中的行
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])  # 包含表格单元格和表头
                    cell_data: List[str] = [cell.get_text(strip=True) for cell in cells]
                    table_data.append(cell_data)

            tables_data.append({
                'filename': filename,
                'table_data': table_data
            })

    return tables_data

def save_major_to_json(major: Major, filename: str):
    """将专业信息保存为 JSON 文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(major.to_json(), f, ensure_ascii=False, indent=4)
def table_process(table: List[List[str]]) -> Major:
    """
    处理表格数据，构建专业对象及其课程。

    :param table: 包含表格内容的二维列表
    :param major_name: 专业名称
    :return: Major 对象
    """
    # 提取表头和课程数据
    table_head = table[0:3]
    table_body = table[3:]
    [grade,school,major,class_name,student_number]=[table_head[0][i].split("：")[1] for i in range(0,5)]
    meta_data = {
    "grade": grade,
    "school": school,
    "major": major,
    "class_name": class_name,
    "student_number": student_number
}
    course_names=table_head[1][1:-4]
    course_credits=table_head[2]
    course_num=len(course_credits)
    courses:List[Course] = []
    for i in range(course_num):
        course_name=course_names[i]
        course_credit=(float)(course_credits[i].split("]")[-1])
        course_type=course_credits[i][1:3]
        course=Course(course_name,course_credit,course_type)
        courses.append(course)
    # 提取课程名称和学分信息
    course_names = table_head[1][1:]  # 假设从第二列开始是课程名称
    course_credits = table_head[2][1:]  # 假设从第二列开始是学分信息
    students:List[Student]=[]
    for row in table_body:
        [index_str,student_id,student_name]=row[:3]
        student=Student((int)(index_str),name=student_name,student_id=student_id)
        score_strs=row[3:-4]
        for i in range(course_num):
            score_str=score_strs[i]
            score=None
            if(score_str==''):
                score=Score(course_names[i],"考核","0")
                student.add_score(score)
            elif(score_str=='合格' or '不合格'):
                score=Score(course_names[i],"考察",score_str)
                student.add_score(score)
                if(score_str=="不合格"):
                    student.has_failed_course=True
            else:
                score=Score(course_names[i],"考核",score_str)
                if((float)(score_str)<60):
                    student.has_failed_course=True
                student.add_score(score)
        students.append(student)
    major=Major(grade,major,courses,students)
    return major
def major_process(major:Major):
    courses=major.courses
    for course in courses:
        course.is_selected_process(major)
    pass