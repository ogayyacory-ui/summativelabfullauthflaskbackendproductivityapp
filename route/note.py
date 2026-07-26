from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.note import Note

class NoteListResource(Resource):
    @jwt_required()
    def get(self):
        """GET /notes?page=1&per_page=10 (Paginated)"""
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Retrieve ONLY notes belonging to current authenticated user
        pagination = Note.query.filter_by(user_id=current_user_id)\
                               .order_by(Note.created_at.desc())\
                               .paginate(page=page, per_page=per_page, error_out=False)

        return {
            "notes": [note.to_dict() for note in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page
        }, 200

    @jwt_required()
    def post(self):
        """POST /notes"""
        current_user_id = int(get_jwt_identity())
        data = request.get_json() or {}

        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {"error": "Title and content are required"}, 400

        new_note = Note(
            title=title,
            content=content,
            user_id=current_user_id
        )
        db.session.add(new_note)
        db.session.commit()

        return new_note.to_dict(), 201


class NoteDetailResource(Resource):
    @jwt_required()
    def get(self, note_id):
        """GET /notes/<id>"""
        current_user_id = int(get_jwt_identity())
        note = Note.query.get(note_id)

        if not note:
            return {"error": "Note not found"}, 404

        # Route protection & authorization check
        if note.user_id != current_user_id:
            return {"error": "Unauthorized access to this resource"}, 403

        return note.to_dict(), 200

    @jwt_required()
    def patch(self, note_id):
        """PATCH /notes/<id>"""
        current_user_id = int(get_jwt_identity())
        note = Note.query.get(note_id)

        if not note:
            return {"error": "Note not found"}, 404

        if note.user_id != current_user_id:
            return {"error": "Unauthorized modification attempt"}, 403

        data = request.get_json() or {}
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']

        db.session.commit()
        return note.to_dict(), 200

    @jwt_required()
    def delete(self, note_id):
        """DELETE /notes/<id>"""
        current_user_id = int(get_jwt_identity())
        note = Note.query.get(note_id)

        if not note:
            return {"error": "Note not found"}, 404

        if note.user_id != current_user_id:
            return {"error": "Unauthorized deletion attempt"}, 403

        db.session.delete(note)
        db.session.commit()
        return {"message": "Note deleted successfully"}, 200