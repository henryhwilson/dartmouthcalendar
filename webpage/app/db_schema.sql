create table if not exists events (
  id integer primary key autoincrement,
  event_from text not null,
  subject text not null,
  blitz_date text not null, 
  category text not null, 
  time_event text not null,
  date_event text not null,
  html text not null
);