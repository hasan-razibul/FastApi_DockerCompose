import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/projects/", response_model=schemas.Project)
def create_project(name: str = Form(...), description: str = Form(...), status: str = Form(...), pdf: UploadFile = File(...), db: Session = Depends(get_db)):
    db_project = crud.get_project_by_name(db, name=name)
    if db_project:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_project(db=db, name=name, description=description, status=status, pdf=pdf)


@app.get("/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.get("/projects/{project_id}/pdf")
def get_project_pdf(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    pdf_path = db_project.pdf
    pdf_filename = os.path.basename(pdf_path)
    response = FileResponse(pdf_path, media_type='application/pdf')
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_filename}"
    return response


@app.put("/projects/{project_id}", response_model=schemas.Project)
async def update_project(
    project_id: int, 
    name: str = Form(None), 
    description: str = Form(None), 
    status: str = Form(None), 
    pdf: UploadFile = File(None), 
    db: Session = Depends(get_db)
):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if name is not None:
        db_project.name = name
    if description is not None:
        db_project.description = description
    if status is not None:
        db_project.status = status
    if pdf is not None:
        # delete the old file
        if os.path.exists(db_project.pdf):
            os.remove(db_project.pdf)

        # save the new file
        file_location = f"/app/pdfs/{pdf.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(await pdf.read())

        # update the database record
        db_project.pdf = file_location

    db.commit()
    db.refresh(db_project)
    return db_project


@app.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    # Delete the PDF file
    try:
        os.remove(db_project.pdf)
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")
    
    return crud.delete_project(db=db, project_id=project_id)
