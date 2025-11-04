import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from typing import List

app = FastAPI()

personal_recs = pd.read_parquet("recommendations.parquet").rename(columns={'item_id':'track_id'})
top_popular = pd.read_parquet("top_popular.parquet").rename(columns={'recommended_track_id':'track_id'})

user2rec = personal_recs.groupby('user_id')['track_id'].apply(list).to_dict()
top_popular_list = top_popular['track_id'].tolist()

@app.get("/recommend")
def recommend(
    user_id: int = Query(...),
    user_history: List[int] = Query([], alias='history')
):
    recs = user2rec.get(user_id, [])
    recs = [track for track in recs if track not in user_history]
    need_more = 10 - len(recs)
    filler = [track for track in top_popular_list if track not in recs and track not in user_history]
    recs += filler[:need_more]
    
    recs = recs[:10]
    if not recs:
        raise HTTPException(status_code=404, detail="no recommendations available")
    return {"user_id": user_id, "recommendations": recs}