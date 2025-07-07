from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #關閉追蹤資料是否被改動

db.init_app(app) 

# 初始化資料庫與預設資料
with app.app_context():
    db.create_all()  
    if not Patient.query.first(): #若空的就先放
        db.session.add_all([
            Patient(name="挖哩勒", report_year=2020, pathology_count=9, cancer_type="乳癌", hospital_code="H001"),
            Patient(name="哇啦啦", report_year=2021, pathology_count=8, cancer_type="大腸癌", hospital_code="H001"),
            Patient(name="挖喔喔", report_year=2022, pathology_count=5, cancer_type="乳癌", hospital_code="H002"),
        ])
        db.session.commit()


@app.route("/", methods=["GET"])
def index():
    # 從查詢字串中取得篩選條件（醫院代碼與癌症種類）
    hospital = request.args.get("hospital_code", "")
    cancer = request.args.get("cancer_type", "")

    # 從資料庫中取得所有醫院代碼
    hospitals = db.session.query(Patient.hospital_code).distinct().all()
    hospitals = [h[0] for h in hospitals]

    # 定義癌症選項
    cancers = ["乳癌", "大腸直腸癌", "肝癌", "口腔癌", "子宮頸癌", 
               "攝護腺癌", "卵巢癌", "胰臟癌", "食道癌", "胃癌"]

    # 查詢病人資料（可依篩選條件過濾）
    query = Patient.query
    if hospital:
        query = query.filter_by(hospital_code=hospital)
    if cancer:
        query = query.filter_by(cancer_type=cancer)

    patients = query.all()

    # 統計資料
    total_patients = len(patients)
    total_reports = sum(p.pathology_count for p in patients)

    # 渲染模板，傳回資料
    return render_template("index.html",
        hospitals=hospitals,
        selected_hospital=hospital,
        cancers=cancers,
        selected_cancer=cancer,
        patients=patients,
        total_patients=total_patients,
        total_reports=total_reports
    )

# 詳細資料頁面
@app.route("/detail/<int:patient_id>")
def detail(patient_id):
    patient = Patient.query.get_or_404(patient_id) 
    return render_template("detail.html", patient=patient)

# 病歷紀錄頁面
@app.route("/record/<int:patient_id>")
def record(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("record.html", patient=patient)

# 進步分析頁面
@app.route("/analyze/<int:patient_id>")
def analyze(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("analyze.html", patient=patient)

# 刪除病人功能
@app.route("/delete/<int:patient_id>")
def delete(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

# 新增病人頁面與功能
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # 從表單接收資料
        name = request.form["name"]
        report_year = int(request.form["report_year"])
        pathology_count = int(request.form["pathology_count"])
        audit_count = int(request.form["audit_count"])
        other_count = int(request.form["other_count"])
        cancer_type = request.form["cancer_type"]
        hospital_code = request.form["hospital_code"]

        # 建立病人並寫入資料庫
        new_patient = Patient(
            name=name,
            report_year=report_year,
            pathology_count=pathology_count,
            audit_count=audit_count,
            other_count=other_count,
            cancer_type=cancer_type,
            hospital_code=hospital_code
        )
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('index'))

    cancers = ["乳癌", "大腸直腸癌", "肝癌", "口腔癌", "子宮頸癌", 
               "攝護腺癌", "卵巢癌", "胰臟癌", "食道癌", "胃癌"]
    hospitals = db.session.query(Patient.hospital_code).distinct().all()
    hospitals = [h[0] for h in hospitals]
    return render_template("add.html", cancers=cancers, hospitals=hospitals)


if __name__ == "__main__":
    app.run(debug=True)
