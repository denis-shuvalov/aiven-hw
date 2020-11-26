from app.settings import POSTGRES_TABLE


async def get_last_events(conn, num_events):

    if num_events:
        data_from_db = await conn.fetch(
            f"""SELECT * FROM {POSTGRES_TABLE}
                ORDER BY created_at DESC
                LIMIT {num_events}
            """
        )
    else:
        data_from_db = await conn.fetch(
            f"""SELECT * FROM {POSTGRES_TABLE}
                ORDER BY created_at DESC
            """
        )

    resp = [rec["value"] for rec in data_from_db]

    return resp