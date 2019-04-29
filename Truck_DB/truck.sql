/* TRUCK DB */

-- TABLES --

CREATE TABLE customer (
	customerid		int(11)			NOT NULL	AUTO_INCREMENT,
	first_name		varchar(20)		NOT NULL,
	last_name		varchar(20)		NOT NULL,
	email			varchar(40)		NOT NULL,
	password		varchar(20)		NOT NULL,
	address			varchar(100)	NOT NULL,
  primary key (customerid)
);

CREATE TABLE employee (
	employeeid		int(11)			NOT NULL	AUTO_INCREMENT,
	first_name		varchar(20)		NOT NULL,
	last_name		varchar(20)		NOT NULL,
	email			varchar(40)		NOT NULL,
	password		varchar(20)		NOT NULL,
	admin			tinyint(1)		NOT NULL,
  primary key (employeeid)
);

CREATE TABLE purchase (
	transactionid	int(11)			NOT NULL	AUTO_INCREMENT,
	vehicleid		int(11)			NOT NULL,
	employeeid		int(11)			NOT NULL,
	customerid		int(11)			NOT NULL,
  primary key (transactionid),
  foreign key (employeeid) references employee(employeeid),
  foreign key (customerid) references customer(customerid)
);

CREATE TABLE test_drive (
	date			date			NOT NULL,
	pickup_time		time			NOT NULL,
	dropoff_time	time			NOT NULL,
	customerid		int(11)			NOT NULL,
	employeeid		int(11)			NOT NULL,
	vehicleid		int(11)			NOT NULL,
  primary key (date, pickup_time, dropoff_time)
);

CREATE TABLE vehicle (
	vehicleid		int(11)			NOT NULL	AUTO_INCREMENT,
	make			varchar(20)		NOT NULL,
	model			varchar(20)		NOT NULL,
	color			varchar(20)		NOT NULL,
	year			int(11)			NOT NULL,
	price			int(11)			NOT NULL,
	picture			varchar(20)		NOT NULL,
  primary key (vehicleid)
);


-- INSERTS --

INSERT INTO `customer` (`customerid`, `first_name`, `last_name`, `email`, `password`, `address`) VALUES
(1, 'Neil', 'Rhea', 'neil.rhea@gmail.com', 'neilrhea', '1549 Brick Dr, Nashville, TN 37207'),
(2, 'Fabian', 'Kosloski', 'fabian.kosloski@gmail.com', 'fabiankosloski', '2374 Chickasaw St, Cincinnati, OH 45219'),
(3, 'Glen', 'Vandine', 'glen.vandine@gmail.com', 'glenvandine', '399 Lawndale Dr, Munster, IN 46321'),
(4, 'Toney', 'Aldaco', 'toney.aldaco@gmail.com', 'toneyaldaco', '1198 N 19th Ave, Melrose Park, IL 60160'),
(5, 'Gene', 'Bohlen', 'gene.bohlen@gmail.com', 'genebohlen', '2686 W Potomac Ave, Chicago, IL 60622'),
(6, 'Larisa', 'Botello', 'larisa.botello@gmail.com', 'larisabotello', '441 E Erie St, Chicago, IL 60611'),
(7, 'Meri', 'Chung', 'meri.chung@gmail.com', 'merichung', '5675 N Graceland Dr, Peoria, IL 61614'),
(8, 'Shanna', 'Mote', 'shanna.mote@gmail.com', 'shannamote', '3955 Dorchester Ave, Gurnee, IL 60031'),
(9, 'Shamika', 'Poss', 'shamika.poss@gmail.com', 'shamikaposs', '987 Bayview Dr, Round Lake Beach, IL 60073'),
(10, 'Maximina', 'Carrizales', 'maximina.carrizales@gmail.com', 'maximinacarrizales', '140 McKinley Ave, Libertyville, IL 60048');

INSERT INTO `employee` (`employeeid`, `first_name`, `last_name`, `email`, `password`, `admin`) VALUES
(1, 'Kenzo', 'Scheerlinck', 'kenzo@scheerlinck.be', 'abc', 1),
(2, 'Salvatore', 'Macrito', 'smacrito@gmail.com', 'abc', 1),
(3, 'Anthony', 'Soto', 'amsoto101@gmail.com', 'abc', 1);

INSERT INTO `vehicle` (`vehicleid`, `make`, `model`, `color`, `year`, `price`, `picture`) VALUES
(1, 'Kenworth', 'W990', 'White', 2019, 110000, 'w990.png'),
(3, 'Kenworth', 'W990', 'Black', 2019, 110000, 'w990.png'),
(4, 'Kenworth', 'W990', 'Blue', 2019, 110000, 'w990.png'),
(5, 'Kenworth', 'W990', 'Gray', 2019, 110000, 'w990.png'),
(6, 'Kenworth', 'W990', 'Beige', 2019, 110000, 'w990.png'),
(7, 'Kenworth', 'W990', 'Yellow', 2019, 110000, 'w990.png'),
(8, 'Kenworth', 'T680', 'White', 2019, 120000, 't680.png'),
(9, 'Kenworth', 'T680', 'White', 2018, 120000, 't680.png'),
(10, 'Kenworth', 'T680', 'White', 2019, 120000, 't680.png'),
(11, 'Kenworth', 'T680', 'Black', 2018, 120000, 't680.png'),
(12, 'Kenworth', 'T680', 'Blue', 2018, 120000, 't680.png'),
(13, 'Kenworth', 'T680', 'Black', 2019, 120000, 't680.png'),
(14, 'Peterbilt', '579', 'Red', 2019, 115000, '579.png'),
(15, 'Peterbilt', '579', 'Red', 2019, 115000, '579.png'),
(16, 'Peterbilt', '579', 'Black', 2019, 115000, '579.png'),
(17, 'Peterbilt', '579', 'Black', 2018, 115000, '579.png'),
(18, 'Peterbilt', '579', 'White', 2019, 115000, '579.png'),
(19, 'Peterbilt', '389', 'Red', 2019, 100000, '389.png'),
(20, 'Peterbilt', '389', 'Red', 2019, 100000, '389.png'),
(21, 'Peterbilt', '389', 'Black', 2018, 100000, '389.png'),
(22, 'Peterbilt', '389', 'White', 2018, 100000, '389.png');