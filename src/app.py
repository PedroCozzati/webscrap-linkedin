from fastapi import FastAPI
from src.database import create_db_and_tables, Vaga, engine
from sqlmodel import Session, select
import pandas as pd

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    df = pd.read_csv("results/linkedin_jobs.csv")
    for index, row in df.iterrows():
        with Session(engine) as session:
            vaga = session.exec(select(Vaga).where(Vaga.link == row["link"])).first()
            if vaga is None:
                vaga = Vaga(
                    title=row["title"],
                    location=row["location"],
                    time_opened=row["time_opened"],
                    link=row["link"],
                    applications=row["applications"],
                    experience_level=row["experience_level"],
                    job_type=row["job_type"],
                    role=row["role"],
                    sectors=row["sectors"],
                    description=row["description"],
                )
                session.add(vaga)
                session.commit()


@app.post("/vaga/")
def create_vaga(vaga: Vaga):
    with Session(engine) as session:
        session.add(vaga)
        session.commit()
        session.refresh(vaga)
        return vaga


@app.get("/vagas/")
def read_vagas():
    with Session(engine) as session:
        vagas = session.exec(select(Vaga)).all()
        return vagas
