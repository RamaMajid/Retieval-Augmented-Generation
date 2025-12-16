fe : - npm dev
be : - npx prisma studio
     - npm start:dev
python: - myenv\Scripts\activate
        - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000