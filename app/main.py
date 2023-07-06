import uvicorn
from fastapi import FastAPI

from app.modules.employees.views import router as employee_router
from app.modules.positions.views import router as position_router
from app.modules.divisions.views import router as division_router
from app.modules.jobs.views import router as job_router

app = FastAPI()

app.include_router(employee_router)
app.include_router(position_router)
app.include_router(division_router)
app.include_router(job_router)


@app.get('/')
def root():
    return {
        'name': 'lab9',
        'version': '1.0.0',
        'swagger': '/docs'
    }


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
