# Stage 1: Build the React frontend
FROM node:18-alpine AS build
WORKDIR /app/client-react
COPY client-react/package.json ./
COPY client-react/package-lock.json ./
RUN npm install
COPY client-react/ ./
RUN npm run build

# Stage 2: Create the production image
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP="oasis-serverside.app:create_app()"
ENV FLASK_ENV=production

WORKDIR /app
COPY oasis-serverside/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY oasis-serverside/ ./oasis-serverside/
COPY --from=build /app/client-react/dist ./oasis-serverside/client/dist

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "oasis-serverside.app:app"]
