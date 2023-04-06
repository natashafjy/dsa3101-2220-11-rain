CREATE TABLE USERS (
        u_id int AUTO_INCREMENT PRIMARY KEY,
        username varchar(255),
        password varchar(255)
        );

CREATE TABLE ROUTINES (
      id int AUTO_INCREMENT PRIMARY KEY,
      u_id int,
      routine_id int,
      pin1_long varchar(255),
      pin1_lat varchar(255),
      pin2_long varchar(255),
      pin2_lat varchar(255),
      pin3_long varchar(255),
      pin3_lat varchar(255),
      pin4_long varchar(255),
      pin4_lat varchar(255),
      pin5_long varchar(255),
      pin5_lat varchar(255),
      pin6_long varchar(255),
      pin6_lat varchar(255),
      FOREIGN KEY (u_id) REFERENCES USERS(u_id) ON DELETE CASCADE 
      );