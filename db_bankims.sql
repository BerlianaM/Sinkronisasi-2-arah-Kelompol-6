/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 10.1.37-MariaDB : Database - db_bankims
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_bankims` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `db_bankims`;

/*Table structure for table `tb_integrasi` */

DROP TABLE IF EXISTS `tb_integrasi`;

CREATE TABLE `tb_integrasi` (
  `id_transaksi` varchar(10) DEFAULT NULL,
  `no_rekening` varchar(10) DEFAULT NULL,
  `tgl_transaksi` datetime DEFAULT NULL,
  `total_transaksi` int(11) DEFAULT '0',
  `status` enum('0','1') DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tb_integrasi` */

insert  into `tb_integrasi`(`id_transaksi`,`no_rekening`,`tgl_transaksi`,`total_transaksi`,`status`) values ('1','1234','2019-05-22 15:20:03',123000,'1'),('2','1234','2019-05-22 16:05:47',125000,'0'),('3','1234','2019-05-22 16:13:18',230000,'0'),('4','1234','2019-05-15 16:29:01',1,'0'),('5','1234','2019-05-22 16:33:37',125000,'0'),('6','1234','2019-05-08 15:31:14',123187,'0'),('4','1234','2019-05-15 16:29:01',1,'0'),('7','1234','2019-05-01 15:35:32',126000,'0');

/*Table structure for table `tb_nasabah` */

DROP TABLE IF EXISTS `tb_nasabah`;

CREATE TABLE `tb_nasabah` (
  `no_rekening` char(10) NOT NULL,
  `nama_nasabah` varchar(255) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `no_telepon` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`no_rekening`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tb_nasabah` */

/*Table structure for table `tb_pegawai` */

DROP TABLE IF EXISTS `tb_pegawai`;

CREATE TABLE `tb_pegawai` (
  `id_pegawai` bigint(20) NOT NULL AUTO_INCREMENT,
  `nama_pegawai` varchar(50) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_pegawai`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tb_pegawai` */

/*Table structure for table `tb_transaksi` */

DROP TABLE IF EXISTS `tb_transaksi`;

CREATE TABLE `tb_transaksi` (
  `id_transaksi` varchar(10) NOT NULL,
  `no_rekening` varchar(10) DEFAULT NULL,
  `tgl_transaksi` datetime DEFAULT NULL,
  `total_transaksi` int(11) DEFAULT '0',
  `status` enum('0','1') DEFAULT '0',
  PRIMARY KEY (`id_transaksi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tb_transaksi` */

insert  into `tb_transaksi`(`id_transaksi`,`no_rekening`,`tgl_transaksi`,`total_transaksi`,`status`) values ('1','1234','2019-05-22 15:20:03',123000,'1'),('2','1234','2019-05-22 16:05:47',125000,'0'),('3','1234','2019-05-22 16:13:18',230000,'0'),('4','1234','2019-05-15 16:29:01',1,'0'),('5','1234','2019-05-22 16:33:37',125000,'0'),('6','1234','2019-05-08 15:31:14',123187,'0'),('7','1234','2019-05-01 15:35:32',126000,'0');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
