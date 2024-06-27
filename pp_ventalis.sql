-- This SQL script matches the model definitions in Django and assumes the default 'public' schema

CREATE TABLE public.users_newuser (
    id BIGINT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    company VARCHAR(100),
    is_active BOOLEAN NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_client BOOLEAN NOT NULL,
    is_employee BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL,
    date_joined TIMESTAMP NOT NULL
);

CREATE TABLE public.api_apimessage (
    id BIGINT PRIMARY KEY,
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    receiver_id BIGINT REFERENCES public.users_newuser(id),
    sender_id BIGINT REFERENCES public.users_newuser(id)
);

CREATE TABLE public.consultants (
    newuser_id BIGINT PRIMARY KEY REFERENCES public.users_newuser(id),
    matricule VARCHAR(5) UNIQUE NOT NULL
);

CREATE TABLE public.customers (
    newuser_id BIGINT PRIMARY KEY REFERENCES public.users_newuser(id),
    consultant_applied_id BIGINT REFERENCES public.consultants(newuser_id)
);

CREATE TABLE public.messagerie_threadmodel (
    id BIGINT PRIMARY KEY,
    has_unread BOOLEAN NOT NULL,
    receiver_id BIGINT REFERENCES public.users_newuser(id),
    user_id BIGINT REFERENCES public.users_newuser(id)
);

CREATE TABLE public.messagerie_messagemodel (
    id BIGINT PRIMARY KEY,
    body VARCHAR(1000) NOT NULL,
    image VARCHAR(100),
    date TIMESTAMP NOT NULL,
    is_read BOOLEAN NOT NULL,
    receiver_user_id BIGINT REFERENCES public.users_newuser(id),
    sender_user_id BIGINT REFERENCES public.users_newuser(id),
    thread_id BIGINT REFERENCES public.messagerie_threadmodel(id)
);

CREATE TABLE public.store_category (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    slug VARCHAR(255) NOT NULL
);

CREATE TABLE public.store_product (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    discount_price DECIMAL(10, 2),
    image VARCHAR(100),
    created_at TIMESTAMP NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    updated TIMESTAMP NOT NULL,
    category_id BIGINT REFERENCES public.store_category(id),
    created_by_id BIGINT REFERENCES public.users_newuser(id)
);

CREATE TABLE public.store_order (
    id BIGINT PRIMARY KEY,
    transactionid VARCHAR(20),
    date_ordered TIMESTAMP NOT NULL,
    completed BOOLEAN NOT NULL,
    comment TEXT,
    customer_id BIGINT REFERENCES public.customers(newuser_id)
);

CREATE TABLE public.store_orderitem (
    id BIGINT PRIMARY KEY,
    status VARCHAR(2) NOT NULL,
    ordered BOOLEAN NOT NULL,
    quantity INT NOT NULL,
    comment TEXT,
    date_added TIMESTAMP NOT NULL,
    customer_id BIGINT REFERENCES public.customers(newuser_id),
    order_id BIGINT REFERENCES public.store_order(id),
    product_id BIGINT REFERENCES public.store_product(id)
);

CREATE TABLE public.store_orderitemstatushistory (
    id BIGINT PRIMARY KEY,
    status VARCHAR(2) NOT NULL,
    comment TEXT,
    date_modified TIMESTAMP NOT NULL,
    consultant_id BIGINT REFERENCES public.consultants(newuser_id),
    customer_id BIGINT REFERENCES public.customers(newuser_id),
    order_item_id BIGINT REFERENCES public.store_orderitem(id)
);

CREATE TABLE public.users_address (
    id BIGINT PRIMARY KEY,
    street VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    zipcode VARCHAR(20) NOT NULL,
    date_added TIMESTAMP NOT NULL,
    address_type CHAR(1) NOT NULL,
    default BOOLEAN NOT NULL,
    order_id BIGINT REFERENCES public.store_order(id),
    user_id BIGINT REFERENCES public.customers(newuser_id)
);
