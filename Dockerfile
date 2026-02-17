FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY index-hu.html /usr/share/nginx/html/index-hu.html
COPY style.css /usr/share/nginx/html/style.css
COPY images/ /usr/share/nginx/html/images/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
