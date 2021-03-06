from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject


## HTML 화면 보여주기
@app.route('/')
def reviews():
    return render_template('index_profile.html')


# 주문하기(POST) API
@app.route('/reviews', methods=['POST'])
def save_profile():
    phone_number_receive = request.form['phone_number_give']
    pharm_name_receive = request.form['pharm_name_give']
    star_give_receive = request.form['star_give']
    review_detail_receive = request.form['review_detail_give']

    reviews = {
        'phone_number' : phone_number_receive,
        'pharm_name' : pharm_name_receive,
        'star_give' : star_give_receive,
        'review_detail' : review_detail_receive,
    }

    db.reviews.insert_one(reviews)

    return jsonify({'result': 'success', 'msg' : '후기등록이 완료되었습니다!'})


# 주문 목록보기(Read) API
# @app.route('/order', methods=['GET'])
# def view_orders():
#     order_list = list(db.cosults.find({}, {'_id' : False}))
#     return jsonify({'result': 'success', 'orders': order_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)