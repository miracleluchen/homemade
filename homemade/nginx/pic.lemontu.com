server {
        server_name pic.lemontu.com;
        access_log /var/log/nginx/pic.lemontu.com.access.log;
        error_log  /var/log/nginx/pic.lemontu.com.error.log;

        location /images {
            alias /var/www/pic.lemontu.com/images;
        }
}
