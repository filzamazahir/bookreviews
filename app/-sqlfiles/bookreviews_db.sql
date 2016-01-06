-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema bookreviews_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bookreviews_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bookreviews_db` DEFAULT CHARACTER SET utf8 ;
USE `bookreviews_db` ;

-- -----------------------------------------------------
-- Table `bookreviews_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookreviews_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `alias` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookreviews_db`.`authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookreviews_db`.`authors` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookreviews_db`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookreviews_db`.`books` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `author_id` INT NOT NULL,
  `title` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_books_authors1_idx` (`author_id` ASC),
  CONSTRAINT `fk_books_authors1`
    FOREIGN KEY (`author_id`)
    REFERENCES `bookreviews_db`.`authors` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookreviews_db`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookreviews_db`.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` TEXT NULL,
  `rating` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reviews_users_idx` (`user_id` ASC),
  INDEX `fk_reviews_books1_idx` (`book_id` ASC),
  CONSTRAINT `fk_reviews_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `bookreviews_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reviews_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `bookreviews_db`.`books` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
