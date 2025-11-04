import requests

BASE_URL = "http://localhost:8000/recommend"

def test_cold():
    r = requests.get(BASE_URL, params={"user_id": 1324025})  # нет персональных
    print("Cold user:", r.json())

def test_warm_no_history():
    r = requests.get(BASE_URL, params={"user_id": 1000000})  # есть персональные, нет онлайн-истории
    print("Warm user:", r.json())

def test_warm_with_history():
    r = requests.get(BASE_URL, params={"user_id": 1000000, "history": [16078, 985364]})
    print("Warm user with history:", r.json())

if __name__ == "__main__":
    test_cold()
    test_warm_no_history()
    test_warm_with_history()