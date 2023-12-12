# Start with Arch Linux as the base image
FROM archlinux/archlinux:base-devel

ENV container docker

# Update system and install git, wget, curl
RUN pacman -Syyu --noconfirm \
    && pacman -S --needed --noconfirm git wget curl

# Create a new user for building packages (e.g., 'builder') and give sudo privileges
RUN useradd -m builder \
    && echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch to the new user
USER builder
WORKDIR /home/builder

# Install yay (AUR Helper)
RUN git clone https://aur.archlinux.org/yay.git \
    && cd yay \
    && makepkg -si --noconfirm \
    && cd .. \
    && rm -rf yay

# Install Python, Node.js, and Go using yay
RUN yay -S --noconfirm python python-pip nodejs npm go

# Create a Python virtual environment and activate it
RUN python -m venv /home/builder/venv
ENV PATH="/home/builder/venv/bin:$PATH"

# Install Cypress
# RUN npm install cypress --save-dev

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file and install Python dependencies in the virtual environment
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Make port 8888 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
