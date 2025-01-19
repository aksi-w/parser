# main.py
import openpyxl
from psycopg2 import connect, sql
from psycopg2.extras import execute_values

class Titular:
    def __init__(self, profile, beginning_year, fgos, program):
        self.profile = profile
        self.beginning_year = beginning_year
        self.fgos = fgos
        self.program = program

    def __repr__(self):
        return f"{self.profile} ({self.program})"

class Competention:
    def __init__(self, sub_index, index, description, type_):
        self.sub_index = sub_index
        self.index = index
        self.description = description
        self.type = type_

    def __repr__(self):
        return f"{self.index}: {self.description}"

class Plan:
    def __init__(self, count_in_plan, index, name, exam, midterm, kp, coursework, controlwork, midtermwithmark,
                 expert, factual, expert_hour, plan, controlwork_hour, aud, sr, control, preparation,
                 courses_semesters, faculty_code, faculty_name):
        self.count_in_plan = count_in_plan
        self.index = index
        self.name = name
        self.exam = exam
        self.midterm = midterm
        self.kp = kp
        self.coursework = coursework
        self.controlwork = controlwork
        self.midtermwithmark = midtermwithmark
        self.expert = expert
        self.factual = factual
        self.expert_hour = expert_hour
        self.plan = plan
        self.controlwork_hour = controlwork_hour
        self.aud = aud
        self.sr = sr
        self.control = control
        self.preparation = preparation
        self.courses_semesters = courses_semesters
        self.faculty_code = faculty_code
        self.faculty_name = faculty_name

PLAN_NAMES = {
    "Экзамен": "exam",
    "Зачет": "midterm",
    "Зачет с оц.": "midtermwithmark",
    "КП": "kp",
    "КР": "coursework",
    "Контр.": "controlwork",
}

def parse_titular(workbook):
    sheet = workbook["Titul"]
    return Titular(
        sheet.cell(row=20, column=3).value,
        int(sheet.cell(row=30, column=21).value),
        sheet.cell(row=32, column=21).value,
        sheet.cell(row=21, column=3).value
    )

def parse_competentions(workbook):
    sheet = workbook["Comp"]
    competention_list = []
    i = 2
    while i <= sheet.max_row:
        row = sheet[i]
        sub_index = row[0].value or ""
        index = row[1].value or ""
        description = row[4].value or ""
        type_ = row[5].value or ""
        if description:
            competention_list.append(Competention(sub_index, index, description, type_))
        i += 1
    return competention_list

def parse_plans(workbook, program_type):
    sheet = workbook["PlanSvod"]
    semester_amount = {"бакалавриата": 8, "магистратуры": 4, "специалитета": 12}.get(program_type, 0)
    plans = []

    for i in range(6, sheet.max_row + 1):
        row = sheet[i]
        if row[0].value in ("+", "-"):
            courses_semesters = [
                row[19 + semester].value for semester in range(semester_amount)
            ]
            plans.append(
                Plan(
                    count_in_plan=row[0].value == "+",
                    index=row[1].value,
                    name=row[2].value,
                    exam=row[3].value,
                    midterm=row[4].value,
                    kp=row[5].value,
                    coursework=row[6].value,
                    controlwork=row[7].value,
                    midtermwithmark=row[8].value,
                    expert=row[9].value,
                    factual=row[10].value,
                    expert_hour=row[11].value,
                    plan=row[12].value,
                    controlwork_hour=row[13].value,
                    aud=row[14].value,
                    sr=row[15].value,
                    control=row[16].value,
                    preparation=row[17].value,
                    courses_semesters=courses_semesters,
                    faculty_code=row[19 + semester_amount].value,
                    faculty_name=row[20 + semester_amount].value,
                )
            )
    return plans

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS titulars, competentions, plans CASCADE")
        cur.execute("""
            CREATE TABLE titulars (
                profile VARCHAR,
                beginning_year BIGINT,
                fgos VARCHAR,
                program VARCHAR
            );
        """)
        cur.execute("""
            CREATE TABLE competentions (
                sub_index VARCHAR,
                index VARCHAR,
                description VARCHAR,
                type VARCHAR
            );
        """)
        cur.execute("""
            CREATE TABLE plans (
                count_in_plan BOOLEAN,
                index VARCHAR,
                name VARCHAR,
                exam VARCHAR,
                midterm VARCHAR,
                kp VARCHAR,
                coursework VARCHAR,
                controlwork VARCHAR,
                midtermwithmark VARCHAR,
                expert VARCHAR,
                factual VARCHAR,
                expert_hour VARCHAR,
                plan VARCHAR,
                controlwork_hour VARCHAR,
                aud VARCHAR,
                sr VARCHAR,
                control VARCHAR,
                preparation VARCHAR,
                courses_semesters TEXT[],
                faculty_code VARCHAR,
                faculty_name VARCHAR
            );
        """)

def insert_data(conn, titular, competentions, plans):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO titulars (profile, beginning_year, fgos, program) VALUES (%s, %s, %s, %s)",
            (titular.profile, titular.beginning_year, titular.fgos, titular.program),
        )

        competention_values = [
            (comp.sub_index, comp.index, comp.description, comp.type) for comp in competentions
        ]
        execute_values(
            cur,
            "INSERT INTO competentions (sub_index, index, description, type) VALUES %s",
            competention_values,
        )

        plan_values = [
            (
                plan.count_in_plan, plan.index, plan.name, plan.exam, plan.midterm, plan.kp,
                plan.coursework, plan.controlwork, plan.midtermwithmark, plan.expert,
                plan.factual, plan.expert_hour, plan.plan, plan.controlwork_hour, plan.aud,
                plan.sr, plan.control, plan.preparation, plan.courses_semesters,
                plan.faculty_code, plan.faculty_name
            )
            for plan in plans
        ]
        execute_values(
            cur,
            "INSERT INTO plans (count_in_plan, index, name, exam, midterm, kp, coursework, "
            "controlwork, midtermwithmark, expert, factual, expert_hour, plan, controlwork_hour, "
            "aud, sr, control, preparation, courses_semesters, faculty_code, faculty_name) VALUES %s",
            plan_values,
        )

def start_parsing(filename, connection_string):
    conn = connect(connection_string)
    workbook = openpyxl.load_workbook(filename)

    titular = parse_titular(workbook)
    competentions = parse_competentions(workbook)
    plans = parse_plans(workbook, titular.program)

    create_tables(conn)
    insert_data(conn, titular, competentions, plans)

    conn.commit()
    conn.close()