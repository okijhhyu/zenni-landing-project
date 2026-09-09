# --- Build stage -----------------------------------------------------------
FROM node:20-alpine AS build

WORKDIR /app

# These are baked into the static build at compile time (Vite env vars are
# compile-time, not runtime). Override at build time, e.g.:
#   docker build --build-arg VITE_BACKEND_URL=https://... --build-arg VITE_GA_ID=G-XXXX .
ARG VITE_BACKEND_URL=http://localhost:8000
ARG VITE_GA_ID=
ARG VITE_GTM_ID=
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
ENV VITE_GA_ID=$VITE_GA_ID
ENV VITE_GTM_ID=$VITE_GTM_ID

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
