from fastapi import FastAPI, HTTPException, Response
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
import pytz
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

cred = credentials.Certificate("scrapping-deptos-firebase-adminsdk-fbsvc-6339a65ce9.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
from starlette.requests import Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

@app.get("/seleccionar-persona", response_class=HTMLResponse)
async def select_person(request: Request):
    return templates.TemplateResponse("departments.html", {"request": request })

@app.get("/departments", response_class=HTMLResponse)
async def get_departments(request: Request, response: Response):
    deptos_dict = {}
    person = request.cookies.get("person")
    if not person:
        return templates.TemplateResponse("seleccionar_persona.html", {"request": request })

    for doc in db.collection("deptos").where("rejected_n", "==", False).stream():
        deptos_dict[doc.id] = doc

    for doc in db.collection("deptos").where("rejected_a", "==", False).stream():
        deptos_dict[doc.id] = doc  # Si ya está en el diccionario, se sobrescribe (sin duplicados)
    
    combined_docs = sorted(
        deptos_dict.values(),  # Tomamos solo los valores únicos
        key=sort_key_nico,
    )

    departments = [{
        "id": doc.id, 
        "title": doc.to_dict().get('titulo'), 
        "link": doc.to_dict().get('link'), 
        "rejected_n": doc.to_dict().get('rejected_n', False), 
        "rejected_a": doc.to_dict().get('rejected_a', False),
        "precio": doc.to_dict().get('precio'),
        "creacion": get_local_time(doc.to_dict().get('creacion')),
        "favorito_n": doc.to_dict().get('favorito_n', False),
        "favorito_a": doc.to_dict().get('favorito_a', False),
        "codigo": doc.to_dict().get('codigo'),
        "comentario_n": doc.to_dict().get('comentario_n', ''),
        "comentario_a": doc.to_dict().get('comentario_a', ''),
        "direccion": doc.to_dict().get('direccion', '')
        } for doc in combined_docs]
    
    # Se pasa la lista de departamentos al template HTML
    return templates.TemplateResponse("departments.html", {"request": request, "departments": departments, "person": person})

@app.get('/departments/{department_id}')
async def department_detail(request: Request, department_id: str):

    person = request.cookies.get("person")
    if not person:
        return templates.TemplateResponse("seleccionar_persona.html", {"request": request })
    
    doc_ref = db.collection("deptos").document(department_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"error": "Departamento no encontrado"}

    department = {
        "id": doc.id, 
        "title": doc.to_dict().get('titulo'), 
        "link": doc.to_dict().get('link'), 
        "rejected_n": doc.to_dict().get('rejected_n', False), 
        "rejected_a": doc.to_dict().get('rejected_a', False),
        "precio": doc.to_dict().get('precio'),
        "creacion": get_local_time(doc.to_dict().get('creacion')),
        "favorito_n": doc.to_dict().get('favorito_n', False),
        "favorito_a": doc.to_dict().get('favorito_a', False),
        "codigo": doc.to_dict().get('codigo'),
        "comentario_n": doc.to_dict().get('comentario_n', ''),
        "comentario_a": doc.to_dict().get('comentario_a', ''),
        "direccion": doc.to_dict().get('direccion', '')
        }

    return templates.TemplateResponse(
        "department_detail.html",
        {"request": request, "department": department, "person": person }
    )

@app.get("/all")
def obtener_departamentos():
    docs = db.collection("deptos").stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

@app.post("/reject/{departamento_id}")
def rechazar_departamento(departamento_id: str, request: Request):
    person = request.cookies.get("person")
    if not person:
        return templates.TemplateResponse("seleccionar_persona.html", {"request": request })
    
    if person == 'nico':
        db.collection("deptos").document(departamento_id).update({"rejected_n": True})
        db.collection("deptos").document(departamento_id).update({"favorito_n": False})
    if person == 'ampi':
        db.collection("deptos").document(departamento_id).update({"rejected_a": True})
        db.collection("deptos").document(departamento_id).update({"favorito_a": False})
    else:
        return {"mensaje": "Departamento no rechazado"}
    return {"mensaje": "Departamento rechazado"}

@app.post("/remove/{departamento_id}")
def removeDepartment(departamento_id: str):
    
    db.collection("deptos").document(departamento_id).update({"favorito_n": False})
    db.collection("deptos").document(departamento_id).update({"favorito_a": False})

    db.collection("deptos").document(departamento_id).update({"rejected_n": True})
    db.collection("deptos").document(departamento_id).update({"rejected_a": True})

    return {"mensaje": "Departamento removido"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.post("/favorite/{departamento_id}")
def marcar_departamento(departamento_id: str, request: Request):
    person = request.cookies.get("person")
    if not person:
        return templates.TemplateResponse("seleccionar_persona.html", {"request": request })
    
    if person == 'nico':
        db.collection("deptos").document(departamento_id).update({"favorito_n": True})
        db.collection("deptos").document(departamento_id).update({"rejected_n": False})
    if person == 'ampi':
        db.collection("deptos").document(departamento_id).update({"favorito_a": True})
        db.collection("deptos").document(departamento_id).update({"rejected_a": False})
    else:
        return {"mensaje": "Departamento no rechazado"}
    return {"mensaje": "Departamento rechazado"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

class CommentRequest(BaseModel):
    comentario: str

@app.post("/comment/{departamento_id}")
def comentar_departamento(departamento_id: str, request: Request, body: CommentRequest):
    comentario = body.comentario

    person = request.cookies.get("person")
    if not person:
        return templates.TemplateResponse("seleccionar_persona.html", {"request": request })

    if person not in ['nico', 'ampi']:
        raise HTTPException(status_code=400, detail="Persona no válida")

    campo = "comentario_n" if person == "nico" else "comentario_a"
    
    db.collection("deptos").document(departamento_id).update({campo: comentario})
    
    return {"mensaje": "Departamento comentado"}

@app.post("/remove/{departamento_id}")
def remover_departamento(departamento_id: str, request: Request):
    person = request.cookies.get("person")
    if not person:
        return templates.TemplateResponse("seleccionar_persona.html", {"request": request })
    
    if person == 'nico':
        db.collection("deptos").document(departamento_id).update({"favorito_n": True})
        db.collection("deptos").document(departamento_id).update({"rejected_n": False})
    if person == 'ampi':
        db.collection("deptos").document(departamento_id).update({"favorito_a": True})
        db.collection("deptos").document(departamento_id).update({"rejected_a": False})
    else:
        return {"mensaje": "Departamento no rechazado"}
    return {"mensaje": "Departamento rechazado"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

def sort_key_ampi(doc):
    data = doc.to_dict()
    rejected_n = data.get("rejected_n", False)
    rejected_a = data.get("rejected_a", False)
    favorito_n = data.get("favorito_n", False)
    favorito_a = data.get("favorito_a", False)
    creacion = data.get("creacion", datetime.min)  # Si no tiene fecha, usa datetime.min
    
    # Asignamos prioridad (valores más pequeños van primeros en sorted)
    if favorito_n or favorito_a:
        priority = 0  # Favoritos primero
    elif rejected_n:
        priority = 1  # Luego los rechazados por Nico
    elif not rejected_a:
        priority = 2  # Los que no están rechazados por nadie en el medio
    else:
        priority = 3  # Los rechazados por Ampi al final

    return (priority, creacion)

def sort_key_nico(doc):
    data = doc.to_dict()
    rejected_n = data.get("rejected_n", False)
    rejected_a = data.get("rejected_a", False)
    favorito_n = data.get("favorito_n", False)
    favorito_a = data.get("favorito_a", False)
    creacion = data.get("creacion", datetime.min)  # Si no tiene fecha, usa datetime.min

    # Asignamos prioridad (valores más pequeños van primeros en sorted)
    if favorito_n or favorito_a:
        priority = 0  # Favoritos primero
    elif rejected_a:
        priority = 1  # Luego los rechazados por Nico
    elif not rejected_n:
        priority = 2  # Los que no están rechazados por nadie en el medio
    else:
        priority = 3  # Los rechazados por Ampi al final

    return (priority, creacion)

def get_local_time(create_date):
    utc_dt = create_date.replace(tzinfo=pytz.utc)

    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    local_dt = utc_dt.astimezone(local_tz)

    fecha_local = local_dt.strftime("%Y-%m-%d %H:%M:%S")

    return fecha_local