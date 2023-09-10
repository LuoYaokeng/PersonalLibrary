from flask import Flask, request, json, Response
from flask.views import MethodView
import configs
from extension import db,cors


app = Flask(__name__)
app.config.from_object(configs)
db.init_app(app)
cors.init_app(app)

class Book(db.Model):
    __tablename__ = 'Book'
    book_id = db.Column(db.Integer, primary_key=True, doc="书本id")
    book_title = db.Column(db.String, nullable=True, doc="书名")
    book_author = db.Column(db.String, doc="作者")
    book_borrow_date = db.Column(db.DateTime, nullable=False, doc="借阅日期")
    book_return_date = db.Column(db.DateTime, nullable=False, doc="应还日期")
    book_borrower_id = db.Column(db.String, doc="借阅人id")
    book_status = db.Column(db.Enum('0','1','2'),doc="0:想看;1:在借;2:已还;")


@app.route('/')
def hello_world():
    return 'Hello World'

class BookApi(MethodView):
    def get(self,book_id):
        if not book_id:
            books = Book.query.all()
            results = [
                {
                    'book_id': book.book_id,
                    'book_title': book.book_title,
                    'book_author': book.book_author,
                    'book_borrow_date': book.book_borrow_date.strftime('%Y-%m-%d'),
                    'book_return_date': book.book_return_date.strftime('%Y-%m-%d'),
                    'book_borrower_id': book.book_borrower_id,
                    'book_status': book.book_status
                } for book in books
            ]
            return({
                'status': 'success', 
                'message': '数据查询成功',
                'results': results
            })
        book:Book = Book.query.get(book_id)
        return{
            'status': 'success', 
            'message': '数据查询成功',
            'results': {
                'book_id': book.book_id,
                'book_title': book.book_title,
                'book_author': book.book_author,
                'book_borrow_date': book.book_borrow_date.strftime('%Y-%m-%d'),
                'book_return_date': book.book_return_date.strftime('%Y-%m-%d'),
                'book_borrower_id': book.book_borrower_id,
                'book_status': book.book_status
            }
        }

    def post(self):
        form = request.json
        book = Book()
        book.book_title = form.get('book_title')
        book.book_author = form.get('book_author')
        book.book_borrow_date = form.get('book_borrow_date')
        book.book_return_date = form.get('book_return_date')
        book.book_borrower_id = form.get('book_borrower_id')
        book.book_status = form.get('book_status')
        db.session.add(book)
        db.session.commit()

        return{
            'status': 'success', 
            'message': '数据添加成功',
        }
    
    def delete(self,book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return{
            'status': 'success', 
            'message': '数据删除成功',
        }

    def put(self,book_id):
        book:Book = Book.query.get(book_id)
        book.book_title = request.json.get('book_title')
        book.book_author = request.json.get('book_author')
        book.book_borrow_date = request.json.get('book_borrow_date')
        book.book_return_date = request.json.get('book_return_date')
        book.book_borrower_id = request.json.get('book_borrower_id')
        book.book_status = request.json.get('book_status')
        db.session.commit()
        return{
            'status': 'success', 
            'message': '数据修改成功',
        }


book_view = BookApi.as_view('book_api')
app.add_url_rule('/books/',defaults={'book_id':None},view_func=book_view,methods=['GET'])
app.add_url_rule('/books',view_func=book_view,methods=['POST'])
app.add_url_rule('/books/<int:book_id>',view_func=book_view,methods=['GET','PUT','DELETE'])

@app.cli.command()
def create():
    db.create_all()
    Book.init_db()


if __name__=='__main__':
    app.run(debug=True)