from yoyo import step


steps = [
    step(
        f"""CREATE TABLE kafka_events (
            topic VARCHAR(30),
            value VARCHAR(50),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )"""
    )
]