FROM nginx:alpine

# Instalacia Python3 pre contact API backend
RUN apk add --no-cache python3

# Nginx staticke subory
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY index-hu.html /usr/share/nginx/html/index-hu.html
COPY style.css /usr/share/nginx/html/style.css
COPY images/ /usr/share/nginx/html/images/

# Contact API backend
COPY contact_api.py /app/contact_api.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 80

# Spusti oboje — Python API + Nginx
CMD ["/app/start.sh"]
