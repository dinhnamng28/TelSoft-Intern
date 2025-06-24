FROM bitnami/spark:latest

USER root

# Copy requirements file vào container
COPY requirements.txt /tmp/requirements.txt

# Cài đặt pip và các package trong requirements.txt
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install -r /tmp/requirements.txt && \
    # Debug: Kiểm tra trước khi tạo người dùng
    # echo "Creating sparkuser" && \
    # groupadd -g 1001 sparkuser && \
    # useradd -m -u 1001 -g sparkuser -s /bin/bash sparkuser && \
    # echo "User sparkuser created successfully" && \
    # # Đảm bảo quyền sở hữu đối với thư mục /opt/bitnami/spark
    # chown -R sparkuser:sparkuser /opt/bitnami/spark

# Đổi người dùng thành sparkuser
USER sparkuser
