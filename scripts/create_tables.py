from app.db.postgres import Base, engine

Base.metadata.create_all(bind=engine)

print("Tables created")
