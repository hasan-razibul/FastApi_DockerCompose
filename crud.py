from sqlalchemy.orm import Session
import models
import schemas
from fastapi import UploadFile
from typing import Optional
import os


def get_project_by_name(db: Session, name: str):
    return db.query(models.Project).filter(models.Project.name == name).first()


def create_project(db: Session, name: str, description: str, status: str, pdf: UploadFile):
    file_location = f"/app/pdfs/{pdf.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(pdf.file.read())
    db_project = models.Project(name=name, description=description, status=status, pdf=file_location)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_pdf(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        return None
    return db_project.pdf


def update_project(db: Session, project_id: int, project: schemas.ProjectCreate, pdf: Optional[UploadFile] = None):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        return None

    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)

    if pdf:
        # Delete the old PDF file
        try:
            os.remove(db_project.pdf)
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")

        # Save the new PDF file
        file_location = f"/app/pdfs/{pdf.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(pdf.file.read())
        db_project.pdf = file_location

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        return None
    db.delete(db_project)
    db.commit()
    return db_project
