import datetime

from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

from webargs import fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
db = SQLAlchemy(app)
cors = CORS(app)

class Feedback(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String)
    referer = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    settings = db.Column(JSON)

    upvote = db.Column(db.Boolean)
    comment = db.Column(db.Text)

@app.route('/feedback/', methods=['POST'])
@use_kwargs({
    'url': fields.Url(required=True),
    'referer': fields.Url(missing=None),
    'upvote': fields.Boolean(missing=None),
    'comment': fields.Str(missing=None),
})
def submit_feedback(**kwargs):
    kwargs.update({
        'timestamp': datetime.datetime.utcnow(),
        'settings': {
            'headers': dict(request.headers),
        },
    })
    feedback = Feedback(**kwargs)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'status': 'success'}), 201

@app.route('/summary/', methods=['GET'])
def aggregate_upvotes():
    """Aggregate upvotes and downvotes by feedback URL.
    """
    rows = Feedback.query.with_entities(
        Feedback.url,
        sa.func.sum(sa.case([(Feedback.upvote == True, 1)])).label('upvotes'),  # noqa
        sa.func.sum(sa.case([(Feedback.upvote == False, 1)])).label('downvotes'),  # noqa
        sa.func.count(Feedback.upvote).label('count'),
    ).group_by(
        Feedback.url
    )
    return jsonify({
        'results': {
            row.url: {
                'upvotes': row.upvotes,
                'downvotes': row.downvotes,
            }
            for row in rows
        }
    })

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
