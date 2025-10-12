echo "Activare mediu Conda..."
conda activate licenta-backend

echo "Pornire server FastAPI pe http://127.0.0.1:8000 ..."
uvicorn main:app --reload
