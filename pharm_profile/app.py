from flask import Flask, render_template, jsonify, request
from bson import ObjectId

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbproject


## HTML 화면 보여주기
@app.route('/pharmacists')
def pharm_profile():
    return render_template('index_profile.html')


# 주문하기(POST) API
@app.route('/pharmacists_db', methods=['POST'])
def save_profile():
    pharm_name_receive = request.form['pharm_name_give']
    pharm_img_receive = request.form['pharm_img_give']
    pharm_number_receive = request.form['pharm_number_give']
    school_receive = request.form['school_give']
    career_receive = request.form['career_give']
    education_receive = request.form['education_give']
    brief_explain_receive = request.form['brief_explain_give']
    detail_explain_receive = request.form['detail_explain_give']

    pharmacists = {
        'pharm_name' : pharm_name_receive,
        'pharm_img' : pharm_img_receive,
        'pharm_number' : pharm_number_receive,
        'school' : school_receive,
        'career' : career_receive,
        'education' : education_receive,
        'brief_explain' : brief_explain_receive,
        'detail_explain' : detail_explain_receive,
        'stars' : 0,
        'total_review' : 0
    }

    db.pharmacists.insert_one(pharmacists)

    return jsonify({'result': 'success', 'msg' : '프로필 등록이 완료되었습니다!'})


# 주문 목록보기(Read) API
# @app.route('/order', methods=['GET'])
# def view_orders():
#     order_list = list(db.cosults.find({}, {'_id' : False}))
#     return jsonify({'result': 'success', 'orders': order_list})



## HTML 화면 보여주기
# @app.route('/reviews')
# def reviews():
#     return render_template('index_one.html')


# 주문하기(POST) API
@app.route('/reviews_db', methods=['POST'])
def save_review():
    id_receive = request.form['_id']
    phone_number_receive = request.form['phone_number_give']
    star_give_receive = int(request.form['star_give'])
    review_detail_receive = request.form['review_detail_give']

    reviews = {
        'pharmacist_id' : id_receive,
        'phone_number' : phone_number_receive,
        'star_give' : star_give_receive,
        'review_detail' : review_detail_receive,
    }

    db.reviews.insert_one(reviews)
    pharmacist = db.pharmacists.find_one({'_id': ObjectId(id_receive)})
    new_total_review = pharmacist['total_review'] + 1
    new_total_star1 = pharmacist['stars'] * pharmacist['total_review']
    new_total_star2 = new_total_star1 + star_give_receive
    new_total_star3= new_total_star2 / new_total_review
    db.pharmacists.update_one({'_id': ObjectId(id_receive)}, {'$set' : {'stars' : new_total_star3}})
    db.pharmacists.update_one({'_id': ObjectId(id_receive)}, {'$set' : {'total_review' : new_total_review}})



    return jsonify({'result': 'success', 'msg' : '후기등록이 완료되었습니다!'})


@app.route('/reviews_db', methods=['GET'])
def show_review():
    id_receive = request.args.get('_id')
    pharmacist_review = object_id_decoder(db.reviews.find({'pharmacist_id': id_receive}))

    return jsonify({'result' : 'success', 'data' : pharmacist_review})

# # HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index_total_profile.html')



# API 역할을 하는 부분
@app.route('/pharmacists_db', methods=['GET'])
def show_pharmacist():
#     # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
#     # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
#(list(db.mystar.find().sort('like', -1)))
    pharm_list = object_id_decoder(list(db.pharmacists.find().sort('total_review', -1)))

#     # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'data': pharm_list})

# 정렬기준 추가
@app.route('/pharmacists_db_star', methods=['GET'])
def show_pharmacist_star():
#     # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
#     # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
#(list(db.mystar.find().sort('like', -1)))
    pharm_list = object_id_decoder(list(db.pharmacists.find().sort('stars', -1)))

#     # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'data': pharm_list})




@app.route('/pharmacist_db', methods=['GET'])
def get_pharmacist():
    id = request.args.get('id')
    pharm = db.pharmacists.find_one({'_id': ObjectId(id)}, {'_id': False})
    return jsonify({'result': 'success', 'data': pharm})


@app.route('/one')
def one():

    id = request.args.get('id')


    return render_template('index_one.html', id = id)

def object_id_decoder(data_list):
    results = []
    for data in data_list:
        data['_id'] = str(data['_id'])
        results.append(data)
    return results

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

