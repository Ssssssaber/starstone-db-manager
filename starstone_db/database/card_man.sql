CREATE USER 'card_man'@'%' IDENTIFIED BY 'KekeIsStarstone';
GRANT SELECT, INSERT, UPDATE, DELETE on starstoneapp.* to 'card_man'@'%';
FLUSH PRIVILEGES;
