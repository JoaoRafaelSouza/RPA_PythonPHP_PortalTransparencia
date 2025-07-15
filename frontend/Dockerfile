FROM php:8.2-apache

RUN a2enmod rewrite

COPY . /var/www/html/

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

RUN docker-php-ext-install mysqli pdo pdo_mysql

WORKDIR /var/www/html