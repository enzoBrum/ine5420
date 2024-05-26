FROM fedora:40

RUN dnf install python python-tkinter python-pip xorg-x11-fonts-100dpi -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

CMD ["/usr/bin/python", "src/app.py"]
