CREATE TABLE USERS (
        username varchar(255) PRIMARY KEY,
        password varchar(255)
        );

CREATE TABLE ROUTINES (
      username varchar(255) ,
      routine_id int,
      start_address varchar(255),
      start_long varchar(255),
      start_lat varchar(255),
      end_address varchar(255),
      end_long varchar(255),
      end_lat varchar(255),
      start_time varchar(10),
      end_time varchar(10),
      days_of_week varchar(255),
      PRIMARY KEY unique_user_routine (username, routine_id),
      FOREIGN KEY (username) REFERENCES USERS(username) ON DELETE CASCADE
      );
