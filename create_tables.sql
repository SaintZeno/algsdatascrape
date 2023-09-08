CREATE TABLE if not exists algs_game_placement(
   team          VARCHAR 
  ,placement     VARCHAR 
  ,season_split  VARCHAR 
  ,season_league VARCHAR 
  ,region        VARCHAR 
  ,game_name     VARCHAR 
  ,gameTitle     VARCHAR 
  ,gameMap       VARCHAR 
);

CREATE TABLE if not exists algs_statistics(
   Player        VARCHAR
  ,Legend        VARCHAR
  ,Kills         VARCHAR
  ,Knockdowns    VARCHAR
  ,Assists       VARCHAR
  ,Damage_Dealt  VARCHAR
  ,Damage_Taken  VARCHAR
  ,Damage_Ratio  VARCHAR
  ,Ring_Damage   VARCHAR
  ,Revives       VARCHAR
  ,Respawns      VARCHAR
  ,season_split  VARCHAR
  ,season_league VARCHAR
  ,region        VARCHAR
  ,game_name     VARCHAR
  ,gameTitle     VARCHAR
  ,gameMap       VARCHAR
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
order by table_name;

select count(*) from algs_statistics;