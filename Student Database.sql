use StudentsManagement;
create table student(
  id INT auto_increment primary key,
  name varchar(255) not null,
  roll_number varchar(50) not null,
  semester varchar(50) not null,
  branch varchar(100) not null,
  contact varchar(10) not null,
  address text not null,
  gender varchar(10) not null,
  dateofbirth date not null
);