import pandas as pd
from datetime import date
import json, os


class CommonData:
    
    def __init__(self, csvfile_path, json_path):
        self.data = self.csv_df(csvfile_path)
        self.json_path = json_path
    
    def csv_df(self, csvfile_path):
        #Converting csv to DataFrame to dictionary
        df = pd.read_csv(csvfile_path)
        return df.to_dict("records")
    
    def calc_year_month(self, dob):
        #Calculating no.of months and years from given date
        today = date.today()
        try:
            dob_list = dob.split('/')
        except Exception:
            dob_list = today.strftime("%m/%d/%Y").split('/') 

        year = today.year - int(dob_list[2])   
        month = today.month - int(dob_list[0])
        if month < 0:
            month = -month

        Years = ' Yrs'
        Months = ' Months'

        if year == 1:
            Years = ' Yr'
        if month == 1:
            Months =' Month'
        return str(year) + Years + " " + str(month) + Months
    

    def convert_to_date(self, date):
        #Converting date to Day and month with leading Zeros
        date_list = date.split('/')
        if int(date_list[0]) < 10:
            date_list[0] = '0' + date_list[0]
        if int(date_list[1]) < 10:
            date_list[1] = '0' + date_list[1]
        return '/'.join(date_list)
    
    
    def converting_to_json_file(self, data, category):
        data = {category + "RecordCount": len(data), 'data': data}
        #creates directory if not exists
        if not os.path.exists(self.json_path):
            os.mkdir(self.json_path)
        file = open(os.path.join(json_path, category + ".json"), "w")
        file.write(json.dumps(data, indent=4))
        file.close()
    
    def common_data(self, data):
        result_data = {
            "id" : data["id"],
            "fullName" : data["firstname"].title() + " " + data["lastname"].title(),
            "gender" : "Male" if data["gender"] == "m" else "Female", 
            "dob" : self.convert_to_date(data["dob"]),
            "age" : self.calc_year_month(data["dob"]),
            "aadhar" : data["aadhar_number"],
            "city" : data["city"],
            "contactNumber" : str(data["contact_number"])
        }
        return result_data

class Teacher(CommonData):
    def rendering_teacher_to_json(self):
        records = []
        for sub_data in self.data:
            if sub_data["category"] == "teacher":
                result_data = CommonData.common_data(self, sub_data)
                result_data.update({
                    "empNo" : sub_data["emp_no"],
                    "classTeacher" : sub_data["class_teacher_of"],
                    "doj" : CommonData.convert_to_date(self, sub_data["doj"]),
                    "servicePeriod" : CommonData.calc_year_month(self, sub_data["doj"]) ,
                    "previousSchool" : sub_data['previous_school'],
                    "post" : sub_data["post"],
                    "salary" : ("{:,.0f}".format(sub_data["salary"]))
                    })
                # Appending teacher records to list
                records.append(result_data)
        CommonData.converting_to_json_file(self, records, "teacher")

class Student(CommonData):
    
    def grade(self, marks):
        if marks >= 90:
            return "A+"
        elif marks >= 80 & marks <= 89:
            return "A"
        elif marks >= 70 & marks <= 79:
            return "B+"
        elif marks >= 60 & marks <= 69:
            return "B"
        elif marks >= 50 & marks <= 59:
            return "C"
        elif marks >= 0 & marks <= 49:
            return "D"
    
    def rendering_student_to_json(self):
        records = []
        for sub_data in self.data:
            if sub_data["category"] == "student":
                result_data = CommonData.common_data(self, sub_data)
                result_data.update({
                    "rollNo" : int(sub_data["roll_no"]),
                    "className" : sub_data["class"],
                    "totalMarks" : int(sub_data["total_marks"]),
                    "grade" : self.grade(sub_data["total_marks"]),
                    "secPercent" : int(sub_data["sec_percent"]),
                    "hsStream" : sub_data["hs_stream"]
                    })
                # Appending student records to list
                records.append(result_data)
        CommonData.converting_to_json_file(self, records, "student")
        
json_path = input('Enter json path:')

student_obj = Student("D:\ADMIN\Desktop\CSV2JSON-Inheritence\csv\input.csv", json_path)
student_obj.rendering_student_to_json()

teacher_obj = Teacher("D:\ADMIN\Desktop\CSV2JSON-Inheritence\csv\input.csv", json_path)
teacher_obj.rendering_teacher_to_json()
