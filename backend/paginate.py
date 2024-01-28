from fastapi import HTTPException


def paginate(db, url, query, page, per_page=20):
    total = db.count_documents(query)
    if page < 1 or (page - 1) * per_page >= total:
        raise HTTPException(
            status_code=400, detail="Requested page index out of bounds"
        )

    items = []
    for item in db.find(query, skip=(per_page * (page - 1)), limit=per_page):
        item["_id"] = str(item["_id"])
        items.append(item)

    pagination = {
        "total": total,
        "per_page": per_page,
    }
    if page > 1:
        pagination["prev_page"] = f"/{url}?page={page - 1}"
    if page * per_page < total:
        pagination["next_page"] = f"/{url}?page={page + 1}"

    return {
        "pagination": pagination,
        "data": items,
    }
