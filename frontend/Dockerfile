FROM node:18

WORKDIR /app

COPY frontend/package*.json /app/
RUN npm install

COPY frontend /app

ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

RUN npm install -g serve
RUN chmod +x /app/entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["/app/entrypoint.sh"]
