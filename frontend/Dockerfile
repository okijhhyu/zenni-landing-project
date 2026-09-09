# --- Build stage -----------------------------------------------------------
FROM node:20-alpine AS build

WORKDIR /app

# Backend URL to bake into the static build (Vite env vars are compile-time).
# Override at build time: docker build --build-arg VITE_BACKEND_URL=https://... .
ARG VITE_BACKEND_URL=http://localhost:8000
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# --- Serve stage -------------------------------------------------------------
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
