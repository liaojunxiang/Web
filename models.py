#定義資料庫結構
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)       # 病人姓名
    report_year = db.Column(db.Integer, nullable=False)    # 報告年度
    pathology_count = db.Column(db.Integer, default=0)     # 病理報告
    audit_count = db.Column(db.Integer, default=0)         # 抽查報告
    other_count = db.Column(db.Integer, default=0)         # 其他報告
    cancer_type = db.Column(db.String(50), nullable=False) # 癌症類別
    hospital_code = db.Column(db.String(20), nullable=False) # 醫院代碼
