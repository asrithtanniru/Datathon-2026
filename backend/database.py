import sqlite3
import json
from pathlib import Path
from .config import SQLITE_DB_PATH

def get_db():
    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faiss_id INTEGER,
            title TEXT,
            location TEXT,
            price REAL,
            category TEXT,
            bedrooms INTEGER,
            guests INTEGER,
            image_filename TEXT,
            room_type TEXT,
            design_style TEXT,
            lighting TEXT,
            features TEXT,
            objects TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_listing(data: dict) -> int:
    conn = get_db()
    cursor = conn.cursor()
    
    features = data.get("ai_features", [])
    if isinstance(features, list):
        features = json.dumps(features)
        
    objects = data.get("ai_objects", [])
    if isinstance(objects, list):
        objects = json.dumps(objects)

    cursor.execute('''
        INSERT INTO listings (
            faiss_id, title, location, price, category, bedrooms, guests, 
            image_filename, room_type, design_style, lighting, features, objects
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get("faiss_id"),
        data.get("title", ""),
        data.get("location", ""),
        data.get("price", 0.0),
        data.get("category", ""),
        data.get("bedrooms", 0),
        data.get("guests", 0),
        data.get("image_filename", ""),
        data.get("ai_room_type", ""),
        data.get("ai_design_style", ""),
        data.get("ai_lighting", ""),
        features,
        objects
    ))
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id

def get_all_listings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM listings ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]

def get_listings_by_faiss_ids(faiss_ids: list[int]):
    if not faiss_ids:
        return []
    conn = get_db()
    cursor = conn.cursor()
    placeholders = ','.join('?' * len(faiss_ids))
    cursor.execute(f'SELECT * FROM listings WHERE faiss_id IN ({placeholders})', faiss_ids)
    rows = cursor.fetchall()
    conn.close()
    
    # We want to maintain FAISS ranking order!
    unsorted_results = {row['faiss_id']: _row_to_dict(row) for row in rows}
    
    results = []
    for fid in faiss_ids:
        if fid in unsorted_results:
            results.append(unsorted_results[fid])
            
    return results

def _row_to_dict(row):
    d = dict(row)
    try:
        d['features'] = json.loads(d['features'])
    except:
        d['features'] = []
        
    try:
        d['objects'] = json.loads(d['objects'])
    except:
        d['objects'] = []
    return d
