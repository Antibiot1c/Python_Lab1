import xml.etree.ElementTree as ET
import uuid

class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age

    def to_xml_element(self):
        student_element = ET.Element('Student')
        student_element.set('student_id', str(self.student_id))
        ET.SubElement(student_element, 'Name').text = self.name
        ET.SubElement(student_element, 'Age').text = str(self.age)
        return student_element

class Group:
    def __init__(self, group_id, name):
        self.group_id = group_id
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def to_xml_element(self):
        group_element = ET.Element('Group')
        group_element.set('group_id', str(self.group_id))
        ET.SubElement(group_element, 'Name').text = self.name
        students_element = ET.SubElement(group_element, 'Students')
        for student in self.students:
            students_element.append(student.to_xml_element())
        return group_element

def save_to_xml(groups, filename):
    root = ET.Element('EducationalDepartment')
    for group in groups:
        root.append(group.to_xml_element())
    tree = ET.ElementTree(root)
    tree.write(filename)

def load_from_xml(filename):
    groups = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for group_element in root.findall('Group'):
        group_id = int(group_element.get('group_id'))
        name = group_element.find('Name').text
        group = Group(group_id, name)
        for student_element in group_element.find('Students').findall('Student'):
            student_id = uuid.uuid4()  
            name = student_element.find('Name').text
            age = int(student_element.find('Age').text)
            student = Student(student_id, name, age)
            group.add_student(student)
        groups.append(group)
    return groups

if __name__ == "__main__":
    group1 = Group(1, "Group A")
    group1.add_student(Student(uuid.uuid4(), "John Doe", 20))
    group1.add_student(Student(uuid.uuid4(), "Jane Smith", 22))

    group2 = Group(2, "Group B")
    group2.add_student(Student(uuid.uuid4(), "Alice Johnson", 21))
    group2.add_student(Student(uuid.uuid4(), "Bob Brown", 23))

    save_to_xml([group1, group2], "educational_department.xml")

    loaded_groups = load_from_xml("educational_department.xml")
    for group in loaded_groups:
        print(f"Group ID: {group.group_id}, Name: {group.name}")
        for student in group.students:
            print(f"  Student ID: {student.student_id}, Name: {student.name}, Age: {student.age}")
