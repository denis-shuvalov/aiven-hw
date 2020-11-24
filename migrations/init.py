from yoyo import step

steps = [
    step(
        """CREATE TABLE kafka_events (
            topic VARCHAR(30),
            value VARCHAR(50)
        )"""
    )
]