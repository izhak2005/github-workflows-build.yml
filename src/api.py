from flask import Blueprint, jsonify, request
import json

api = Blueprint('api', __name__)

def load_texts():
    try:
        with open('database/texts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_texts(texts):
    with open('database/texts.json', 'w', encoding='utf-8') as f:
        json.dump(texts, f, ensure_ascii=False, indent=4)

@api.route('/save_text', methods=['POST'])
def save_text():
    try:
        data = request.json
        texts = load_texts()
        
        # יצירת מזהה חדש
        new_id = max([t['id'] for t in texts], default=0) + 1
        
        new_text = {
            'id': new_id,
            'title': data['title'],
            'content': data['content'],
            'folder': data['folder']
        }
        
        texts.append(new_text)
        save_texts(texts)
        
        return jsonify({'success': True, 'text_id': new_text['id']})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api.route('/get_texts/<int:folder>')
def get_texts(folder):
    texts = load_texts()
    folder_texts = [t for t in texts if t['folder'] == folder]
    return jsonify({'success': True, 'texts': folder_texts})

@api.route('/delete_text/<int:text_id>')
def delete_text(text_id):
    try:
        texts = load_texts()
        texts = [t for t in texts if t['id'] != text_id]
        save_texts(texts)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
