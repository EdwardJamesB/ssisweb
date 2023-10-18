DROP DATABASE IF EXISTS 'ssisweb';
CREATE DATABASE IF NOT EXISTS 'ssisweb'
USE 'ssisweb';

DROP TABLE IF EXISTS 'student';
CREATE TABLE IF NOT EXISTS `student` (
    'id' VARCHAR(50) NOT NULL,
	`firstname` VARCHAR(50) NOT NULL,
	`lastname` VARCHAR(50) NOT NULL,
	`course` VARCHAR(50) NOT NULL,
	`year` INT NOT NULL,
	`gender` VARCHAR(50) NOT NULL
    PRIMARY KEY ('id')
    FOREIGN KEY (course) REFERENCES course(code) ON DELETE CASCADE
)

DROP TABLE IF EXISTS 'course';
CREATE TABLE IF NOT EXISTS `course` (
	`code` VARCHAR(50) NOT NULL,
	`name ` VARCHAR(50) NOT NULL,
	`college` VARCHAR(50) NOT NULL
    PRIMARY KEY ('code')
    FOREIGN KEY (college) REFERENCES college(code) ON DELETE CASCADE
)

DROP TABLE IF EXISTS 'college';
CREATE TABLE IF NOT EXISTS `college` (
	`code` VARCHAR(50) NOT NULL,
	`name` VARCHAR(50) NOT NULL
)
