#! /usr/bin/env python3
#
# BitBake Hash Server Reference Implementation
#
# Copyright (C) 2018 Garmin International
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
import sqlite3
import hashlib
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hashes.db'

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    taskhash = db.Column(db.String(), nullable=False)
    method = db.Column(db.String(), nullable=False)
    outhash = db.Column(db.String(), nullable=False)
    depid = db.Column(db.String(), nullable=False)
    owner = db.Column(db.String())
    created = db.Column(db.DateTime)
    count = db.Column(db.Integer)

    __table_args__ = (
            #db.UniqueConstraint('taskhash', 'method', 'outhash', name='unique_task'),
            # Make an index on taskhash and method for fast lookup
            db.Index('lookup_index', 'taskhash', 'method'),
            )

    def __init__(self, taskhash, method, outhash, depid, owner=None):
        self.taskhash = taskhash
        self.method = method
        self.outhash = outhash
        self.depid = depid
        self.owner = owner
        self.created = datetime.datetime.utcnow()

class TaskSchema(ma.ModelSchema):
    class Meta:
        model = TaskModel

#class OutHashSchema(TaskSchema):
#    class Meta:
#        fields = ['outhash']

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
#outhash_schema = OutHashSchema()
#outhashes_schema = OutHashSchema(many=True)

# TODO: Handle errors. Currently, everything is a 500 error

#@app.route("/v1/outhashes", methods=["GET"])
#def outhashes():
#    query = TaskModel.query.with_entities(TaskModel.outhash).filter(
#            TaskModel.taskhash == request.args['taskhash'],
#            TaskModel.method == request.args['method']).order_by(
#                    # Oldest first
#                    TaskModel.created)
#
#    return outhash_schema.jsonify(query.first())

@app.route("/v1/tasks", methods=["GET", "POST"])
def taskhash():
    if request.method == 'GET':
        query = TaskModel.query
        for key in request.args:
            if hasattr(TaskModel, key):
                vals = request.args.getlist(key)
                query = query.filter(getattr(TaskModel, key).in_(vals))

        return tasks_schema.jsonify(query.all())

    # TODO: Handle authentication

    data = request.get_json()
    # TODO handle when data is None. Currently breaks

    args = {}
    for a in ('taskhash', 'method', 'outhash', 'depid'):
        args[a] = data[a]

    new_task = TaskModel.query.filter(
            TaskModel.taskhash == data['taskhash'],
            TaskModel.method == data['method'],
            TaskModel.outhash == data['outhash']).first()

    if not new_task:
        new_task = TaskModel(**args)
        db.session.add(new_task)
        db.session.commit()

    return task_schema.jsonify(new_task)

#@app.route("/v1/taskhashes/<int:hash_id>", methods=["GET"])
#def get_hash_by_id(hash_id):
#    return task_schema.jsonify(TaskModel.query.filter(TaskModel.id == hash_id).one_or_none())

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

