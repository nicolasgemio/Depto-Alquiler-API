from controllers.department_controller import DepartmentController

app = DepartmentController().get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)