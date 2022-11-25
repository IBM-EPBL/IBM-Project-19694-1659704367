FROM python:3.10.6
WORKDIR /Expense_Tracker    
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python","app.py"]