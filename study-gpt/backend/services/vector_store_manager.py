#vector_store_manager.py

# room_id 기준
# vector_store 임시 저장 관리


# 메모리 저장소
vector_store_map = {}


# vector_store 저장
def save_vector_store(room_id,vector_store):
    vector_store_map[room_id] = (vector_store)


# vector_store 조회
def get_vector_store(room_id):

    return vector_store_map.get(room_id)

# vector_store 삭제
def remove_vector_store(room_id):

    if room_id in vector_store_map:
        del vector_store_map[room_id]