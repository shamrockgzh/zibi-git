# -*- coding: utf-8 -*-

from flask import Flask, abort, jsonify, render_template, request, make_response, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@127.0.0.1:3306/zibizheng?charset=utf8&use_unicode=0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = "/Users/liulizhe/Documents/zibizheng/views/uploads"#图片文件路径,绝对路径
db = SQLAlchemy(app)

#自闭症评估题库
class assessItem(db.Model):
    __tablename__ = 'assessItem'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text,nullable=False)
    score = db.Column(db.Integer,nullable=False)

#评估结果
class assessResult(db.Model):
    __tablename__ = 'assessResult'
    id = db.Column(db.Integer, primary_key=True)
    Result = db.Column(db.Text,nullable=False)
    gradeMin = db.Column(db.Integer,nullable=False)
    gradeMax = db.Column(db.Integer,nullable=False)


#机构认证
class organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40))
    NumPeople = db.Column(db.Integer)
    province = db.Column(db.String(20))
    city = db.Column(db.String(20))
    district = db.Column(db.String(20))
    abstract = db.Column(db.Text,nullable=False)
    introduce = db.Column(db.Text,nullable=False)

#课程设置：服务模式：硬件设施：师资队伍：
#机构介绍
class orgIntro(db.Model):
    __tablename__ = 'orgIntro'
    id = db.Column(db.Integer,primary_key=True)
    org_id = db.Column(db.Integer,db.ForeignKey('organization.id',ondelete='CASCADE'),nullable=False)
    abstract = db.Column(db.Text)
    course = db.Column(db.Text)
    service = db.Column(db.Text)
    hardware = db.Column(db.Text)
    team = db.Column(db.Text)
    phone = db.Column(db.Text)
    address = db.Column(db.Text)
    #关联organization
    organization = db.relationship(
        'organization',
        foreign_keys = [org_id],primaryjoin='orgIntro.org_id == organization.id',
        backref=db.backref('orgIntro', cascade='all, delete-orphan')
    )

#主页
@app.route('/')
def home():
    return render_template('project.html')

#获得评测表1
@app.route('/assess/',methods=['GET'])
def assess():
    return render_template('items.html')
#获得评测表2
@app.route('/get_assess/',methods=['GET'])
def GetAssessItem():
    if request.method == 'GET':
        items = assessItem.query.all()

        resp_data = {
            'items': [{
                'id':item.id,
                'title':item.title,
                'score':item.score,
                      }for item in items],
        }
        return jsonify(**resp_data)


#评测结果
@app.route('/get_result/',methods=['POST'])
def getResult():
    if request.method == 'POST':
        req_data = request.json
        grade = int(req_data['grade'])
        resultItems = assessResult.query.all()
        for result in resultItems:
            if (grade>=int(result.gradeMin))and(grade<int(result.gradeMax)):
                resp_data = {
                    'result':result.Result,
                }
                return jsonify(**resp_data)
#评测结果-了解更多1
@app.route('/result_more/',methods=['GET'])
def hello():
    #id = request.values.get("id")
    return render_template('resultMore.html')

#评测结果-了解更多2
@app.route('/get_result_more/',methods=['GET'])
def getResultMore():
    if request.method == 'GET':

        req_data = request.json
        grade = int(request.headers.get('grade'))

        if (grade>=0)and(grade<53):
            req_data = {
                'resultMore':'该儿童患有自闭症的可能性较小，建议您进行正常教育的强化，即丰富环境的教育活动。重点包括以下几点：\n'
                            +'1.尽可能不让孩子独自闲着（或独自忙着），父母总是在与孩子处于一对一、面对面地互动中。\n'
                            +'2.父母要利用丰富的眼神、真实略带夸张的表情与动作、动听的语言对孩子进行密集的社交互动。父母要热情奔放、言语抑扬顿挫。\n'
                            +'3.父母要借助孩子生理需求、日常养育活动、亲子游戏等过程中开展干预。尽可能避免孩子看电视或玩电脑游戏。多做传统婴幼儿游戏。\n'
                            +'4.强调父母对婴儿气质的了解，据此实施个体化教养，帮助孩子形成安全依恋。\n'
                            +'5.强调根据儿童社交发展的规律开展相关的亲子游戏和社交互动活动。'
                            +'无论孩子是否反应，父母不要因此受到影响。如果孩子反应恰当，那就愉快地继续这样的活动；如果孩子没有反应，不要因感受挫败而停止计划中的教育活动，要保障孩子在这个时期，在与父母以及家人丰富的社交互动中成长。也许孩子逐渐改善了，不是孤独症了，我们和父母乐观其成；也许孩子随着年龄增长，孤独症相关特征依然，那么我们并没有耽误孩子，婴儿早期神经系统可塑性理论告诉我们，此前的教育干预活动对孩子的症状有缓解的效应，甚至发生了重要的逆转缓解效应。'
                ,
            }
        if (grade>=53)and(grade<67):
            req_data = {
                'grade':'',
            }
        if grade>=67:
            req_data = {
                'grade':grade,
            }

        return jsonify(**req_data)


#获得机构列表1
@app.route('/organization/',methods=['GET'])
def Organization():
    return render_template('organization.html')

#获得机构列表2
@app.route('/get_organization/',methods=['GET'])
def getOrganization():
    if request.method == 'GET':
        items = organization.query.all()

        resp_data = {
            'organization': [{
                'id':item.id,
                'name':item.name,
                'NumPeople':item.NumPeople,
                'province':item.province,
                'city':item.city,
                'district':item.district,
                'abstract':item.abstract,
                      }for item in items],
        }
        return jsonify(**resp_data)

#更多机构介绍1
@app.route('/get_org_intro1/',methods=['GET'])
def getOrgIntro1():
    return render_template('organintro.html')

#更多机构介绍2
@app.route('/get_org_intro/',methods=['GET'])
def getOrgIntro():
    if request.method == 'GET':
        OrgId = int(request.headers.get('id'))

        oIntro = orgIntro.query.filter(db.text('org_id = :temp')).params(temp=int(OrgId)).first()

        resq_data = {
            'orgIntro':{
                'id':oIntro.id,
                'abstract':oIntro.abstract,
                'course':oIntro.course,
                'service':oIntro.service,
                'hardware':oIntro.hardware,
                'team':oIntro.team,
                'phone':oIntro.phone,
                'address':oIntro.address,
            },
        }
        return jsonify(**resq_data)


#加载图片
@app.route('/OrgIntro/<string:book_id>/showimage/', methods=['GET'])     #显示图片封面保持幂等性用get
def image(book_id):                                              #必须有参数才能下面用
    return send_from_directory(app.config['UPLOAD_FOLDER'],u'%d.jpg' % book_id)




if __name__ == '__main__':
    app.run()