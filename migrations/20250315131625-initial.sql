-- +migrate Up
create table cities
(
    id    uuid primary key,
    title varchar(64) unique
);

create table categories
(
    id    uuid primary key,
    title varchar(64) unique

);

create type media_type as enum('png', 'mp4');

create table stores
(
    id                 uuid primary key,
    title              varchar(64),
    description        varchar(4096),
    preview_media_type media_type,
    main_media_type    media_type,
    main_page_url      varchar(512),
    display_priority   int
);


create table stores_cities
(
    id       uuid primary key,
    store_id uuid,
    city_id  uuid,

    constraint fk_store_id foreign key (store_id) references stores (id) on delete cascade,
    constraint fk_city_id foreign key (city_id) references cities (id) on delete cascade
);


create table stores_categories
(
    id          uuid primary key,
    store_id    uuid,
    category_id uuid,
    constraint fk_store_id foreign key (store_id) references stores (id) on delete cascade,
    constraint fk_city_id foreign key (category_id) references categories (id) on delete cascade

);

create table store_resources
(
    id         uuid primary key,
    title      varchar(64),
    target_url varchar(512),
    store_id   uuid,
    constraint fk_stote_id foreign key (store_id) references stores (id) on delete cascade
);


-- +migrate Down
