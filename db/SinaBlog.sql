CREATE TABLE AuthorInfo (
  logo            VARCHAR(255)          DEFAULT "http://p1.zhimg.com/da/8e/da8e974dc_m.jpg",
  author_id       VARCHAR(255) NOT NULL DEFAULT 'null',
  hash            VARCHAR(255)          DEFAULT '',
  name            VARCHAR(255)          DEFAULT '',
  followee        INT                   DEFAULT 0,
  follower        INT                   DEFAULT 0,
  gender          VARCHAR(255)          DEFAULT '',
  weibo           VARCHAR(255)          DEFAULT '',
  PRIMARY KEY (author_id)
);

CREATE TABLE Article (
  author_id    VARCHAR(255)  NOT NULL    DEFAULT '',
  author_hash  VARCHAR(255)  NOT NULL    DEFAULT '',
  author_sign  VARCHAR(2000) NOT NULL    DEFAULT '',
  author_name  VARCHAR(255)  NOT NULL    DEFAULT '',
  author_logo  VARCHAR(255)  NOT NULL    DEFAULT '',

  name         VARCHAR(255)  NOT NULL    DEFAULT '',
  article_id   VARCHAR(255)  NOT NULL    DEFAULT '',
  href         VARCHAR(255)  NOT NULL    DEFAULT '',
  title        VARCHAR(2000) NOT NULL    DEFAULT '',
  title_image  VARCHAR(255)  NOT NULL    DEFAULT '',
  content      longtext      NOT NULL    DEFAULT '',
  comment      INT(20)       NOT NULL    DEFAULT 0,
  publish_date DATE          NOT NULL    DEFAULT '2000-01-01',
  PRIMARY KEY (href)
);