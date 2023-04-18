import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
from root.utils.hashDetails import passwordAdminHash,getAdminToken
from root.utils.getDate import getDateTime
import os
from dotenv import load_dotenv
load_dotenv()




def createTables():
    mydb = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'))
    cursor = mydb.cursor(buffered=True)
    database_sql = "USE {};".format(os.getenv('database'))
    cursor.execute(database_sql)
    createTableIfNotExists=f"""CREATE TABLE IF NOT EXISTS `intbl_items` (
    `idIntbl_Items` int(11) NOT NULL AUTO_INCREMENT,
    `Name` varchar(100) DEFAULT NULL,
    `BrandName` varchar(100) DEFAULT NULL,
    `Code` varchar(50) DEFAULT NULL,
    `UOM` varchar(20) DEFAULT NULL,
    `StockType` varchar(15) DEFAULT NULL,
    `Department` varchar(50) DEFAULT NULL,
    `GroupName` varchar(100) DEFAULT NULL,
    `ExpDate` date DEFAULT NULL,
    `Status` varchar(20) DEFAULT NULL,
    `Taxable` varchar(10) DEFAULT NULL,
    `Rate` decimal(10,2) DEFAULT NULL,
    PRIMARY KEY (`idIntbl_Items`)
);
"""





    cursor.execute(createTableIfNotExists)
    mydb.commit()
    createTableIfNotExists=f"""CREATE TABLE IF NOT EXISTS `intblstorerequisition` (
    `idintblStoreRequisition` int(11) NOT NULL AUTO_INCREMENT,
    `Date` datetime DEFAULT NULL,
    `Department` varchar(50) DEFAULT NULL,
    `Type` varchar(50) DEFAULT NULL,
    `Origin` varchar(50) DEFAULT NULL,
    `DestinationStore` varchar(50) DEFAULT NULL,
    `State` varchar(50) DEFAULT NULL,
    `receivedDate` date DEFAULT NULL,
    PRIMARY KEY (`idintblStoreRequisition`)
);
"""





    cursor.execute(createTableIfNotExists)
    mydb.commit()
    
    
    createTableIfNotExists=f"""CREATE TABLE IF NOT EXISTS `intblstorereqdetails` (
    `idintblStoreReqDetails` int(11) NOT NULL AUTO_INCREMENT,
    `ItemID` int(11) DEFAULT NULL,
    `StoreReqID` int(11) DEFAULT NULL,
    `Amount` decimal(10,3) DEFAULT NULL,
    `UOM` varchar(50) DEFAULT NULL,
    `Rate` decimal(10,2) DEFAULT NULL,
    PRIMARY KEY (`idintblStoreReqDetails`),
    KEY `RecKey212` (`ItemID`),
    KEY `RecKey213` (`StoreReqID`),
    CONSTRAINT `RecKe212` FOREIGN KEY (`ItemID`) REFERENCES `intbl_items` (`idIntbl_Items`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `RecKe213` FOREIGN KEY (`StoreReqID`) REFERENCES `intblstorerequisition` (`idintblStoreRequisition`) ON DELETE NO ACTION ON UPDATE NO ACTION
);
"""





    cursor.execute(createTableIfNotExists)
    mydb.commit()

    createTableIfNotExists=f"""CREATE TABLE IF NOT EXISTS `tblLogin` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(40) NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT '1',
  `token` varchar(200) DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `username` (`username`)
);
"""
    cursor.execute(createTableIfNotExists)
    mydb.commit()
    currentDate=getDateTime()
    passwordhash = passwordAdminHash(os.getenv('ADMIN_PASSWORD'))
    tokenstring = "{}{}".format(currentDate,os.getenv('ADMIN_PASSWORD'))
    token = getAdminToken(tokenstring)
    createTableIfNotExists=f"""INSERT IGNORE INTO `tblLogin`(`username`, `password`,`token`,`type`) VALUES (%s,%s,%s,"ADMIN");"""
    cursor.execute(createTableIfNotExists,(os.getenv('ADMIN_USERNAME'),passwordhash,token,),)
    mydb.commit()
    mydb.close()