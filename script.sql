-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema competicao_2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema competicao_2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `competicao_2` DEFAULT CHARACTER SET utf8mb3 ;
USE `competicao_2` ;

-- -----------------------------------------------------
-- Table `competicao_2`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competicao_2`.`cliente` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `cpf` VARCHAR(14) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;

SELECT * FROM cliente;

-- -----------------------------------------------------
-- Table `competicao_2`.`perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competicao_2`.`perfil` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nome_UNIQUE` (`nome` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;

SELECT * FROM perfil;

-- -----------------------------------------------------
-- Table `competicao_2`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competicao_2`.`usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `cpf` VARCHAR(14) NOT NULL,
  `senha` VARCHAR(340) NOT NULL,
  `perfil_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC) VISIBLE,
  UNIQUE INDEX `senha_UNIQUE` (`senha` ASC) VISIBLE,
  INDEX `fk_usuario_perfil_idx` (`perfil_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_perfil`
    FOREIGN KEY (`perfil_id`)
    REFERENCES `competicao_2`.`perfil` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;

SELECT u.nome, u.email AS nome_usuario, p.nome AS nome_perfil
FROM usuario u
INNER JOIN perfil p
ON u.perfil_id = p.id;

SELECT * FROM usuario;	


-- -----------------------------------------------------
-- Table `competicao_2`.`evento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competicao_2`.`evento` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `dia` DATE NOT NULL,
  `horario` TIME NOT NULL,
  `cpt_evento` INT NOT NULL,
  `preco` VARCHAR(45) NOT NULL,
  `usuario_id` INT NOT NULL,
  `imagem` VARCHAR(100) NULL DEFAULT NULL,
  `descricao` VARCHAR(250) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `horario_UNIQUE` (`horario` ASC) VISIBLE,
  INDEX `fk_evento_usuario1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_evento_usuario1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `competicao_2`.`usuario` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;

SELECT * FROM evento;


-- -----------------------------------------------------
-- Table `competicao_2`.`setor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competicao_2`.`setor` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `qtd_setor` INT NOT NULL,
  `evento_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_setor_evento1_idx` (`evento_id` ASC) VISIBLE,
  CONSTRAINT `fk_setor_evento1`
    FOREIGN KEY (`evento_id`)
    REFERENCES `competicao_2`.`evento` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb3;

SELECT * FROM setor;

-- -----------------------------------------------------
-- Table `competicao_2`.`ingresso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competicao_2`.`ingresso` (
  `cliente_id` INT NOT NULL,
  `evento_id` INT NOT NULL,
  `setor_id` INT NOT NULL,
  `id_ingresso` VARCHAR(45) NOT NULL,
  `data_emissao` DATETIME NOT NULL,
  `valor` VARCHAR(45) NOT NULL,
  `status_Ingresso` VARCHAR(45) NOT NULL DEFAULT 'emitido',
  INDEX `fk_cliente_has_evento_evento1_idx` (`evento_id` ASC) VISIBLE,
  INDEX `fk_cliente_has_evento_cliente1_idx` (`cliente_id` ASC) VISIBLE,
  INDEX `fk_cliente_has_evento_setor1_idx` (`setor_id` ASC) VISIBLE,
  UNIQUE INDEX `id_ingresso_UNIQUE` (`id_ingresso` ASC) VISIBLE,
  PRIMARY KEY (`id_ingresso`),
  CONSTRAINT `fk_cliente_has_evento_cliente1`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `competicao_2`.`cliente` (`id`),
  CONSTRAINT `fk_cliente_has_evento_evento1`
    FOREIGN KEY (`evento_id`)
    REFERENCES `competicao_2`.`evento` (`id`),
  CONSTRAINT `fk_cliente_has_evento_setor1`
    FOREIGN KEY (`setor_id`)
    REFERENCES `competicao_2`.`setor` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

SELECT * FROM ingresso;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
