FROM python:3.9-slim-buster

# 备份并更换软件源为阿里云镜像源
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com\/debian-security/g' /etc/apt/sources.list

# 设置工作目录
WORKDIR /app

# 安装系统依赖，添加 --fix-missing 参数
RUN apt-get update && apt-get install -y --fix-missing \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装 Python 依赖
COPY requirements.txt .
# 更新 pip、setuptools 和 wheel
RUN python -m pip install --upgrade pip setuptools wheel
# 使用阿里云镜像源安装依赖（移除实验性选项）
RUN pip cache purge && pip install --no-cache-dir --verbose -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

# 复制项目代码
COPY . .

# 设置环境变量（可选）
ENV PYTHONUNBUFFERED=1

# 暴露端口（如果需要）
EXPOSE 8000

# 定义启动命令
CMD ["python", "main.py"]
