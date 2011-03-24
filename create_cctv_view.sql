CREATE VIEW cctv AS 
SELECT n.id,n.geom,n.tags,n.tstamp,n.user_id,u.name AS user_name FROM nodes AS n 
  INNER JOIN users AS u ON n.user_id = u.id 
  WHERE tags->'man_made'='surveillance' ;