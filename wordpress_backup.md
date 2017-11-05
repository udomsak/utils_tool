# Wordpress backup script 

Wordpress backup เป็น Python script สำหรับใช้ในการ backup wordpress site โดยจะทำงานกับ wp-cli ( wordpress command line utility ). และ 
tool อื่นๆ 

## วิธีติดตั้ง

1. ดาวน์โหลดไฟล์ wordpress_backup.py 
2. กำหนดสิทธิ ให้เป็น execute file ( chmod =x wordpress_backup.py ) 
3. ( option ) อาจเปลี่ยนชื่อไฟล์ ไม่ต้องมีนามสกุลก็ได้  
4. ( option ) นำไปวางไว้ directory ที่อยู่ใน system Path ( เพือความสะดวกในการเรียกใช้ ) 

#### requirement 

*  wp-cli 

## วิธีใช้ 
พิมพ์ Option -h เพื่อดูวิธีใช้งาน

```
usage: wordpress_backup.py [-h] [--clean] [--backup BACKUP] [--backup_all]
                     [--restore RESTORE] [--restore_all] [--list_site]

Wordpress Backup script

optional arguments:
  -h, --help         show this help message and exit
  --clean            Check file roration and cleansing
  --backup BACKUP    Backup { wordpress_site }
  --backup_all       Backup ALL wordpress site
  --restore RESTORE  Restore wordpress specify site
  --restore_all      Restore ALL wordpress
  --list_site        List site in config file (/etc/wordpress_backup.ini)

```

### วิธี backup 
หลังจากกำหนด site ไว้ใน file configuration แล้ว ( /etc/wordpress_backup.ini ) โดยมี Option ให้ใช้ัตามนี้ 

#### backup บาง site
```
wordpress_backup.py --backup { site ที่เราจะทำการ backup } 
```
#### backup ทั้งหมด 
```
wordpress_backup.py --backup_all 
```

### วิธี restore   
หลังจากกำหนด site ไว้ใน file configuration แล้ว ( /etc/wordpress_backup.ini ) โดยมี Option ให้ใช้ัตามนี้ 

#### restore บาง site  
```
wordpress_backup.py --restore { site ที่เราจะทำการ restore } 
```
#### restore ทั้งหมด
```
wordpress_backup.py --restore_all 
```
## Config file 
Wordpress backup มี configuration file โดยจะอยู่ที่ /etc/wordpress_backup.ini โดยมีรายละเอียด ของ section ตามนี้ 

*  website เป็น configuration สำหรับ backup แต่ละ site
*  database_backup_path เป็น configuration สำหรับ กำหนด directory สำหรับเก็บ ไฟล์ backup 
*  backup_policy เป็น configuration สำหรับ กำหนด rotation policy โดย หากครบจำนวน rotation script จะทำการลบ backup file ให้เหลือ 
เฉพาะไฟล์ backup ล่าสุด ไฟล์ backup ล่าสุดจะชื่อ ```{รายการbackup}_latest.sql```    

### การเพิ่ม แก้ไข รายการที่ต้องการ backup ให้ไปแก้ไขที่ section "website" 

โดยให้มี รูปแบบ ดังต่อไปนี้  
```
[website]
{ ชื่อรายการจะตังเป็น ชื่ออะไรก็ได้ } = { absolute path ของ wordpress site } 
```
ตัวอย่าง 
```
[website]
project1 = /home/webs/Projects/Wordpress_site1
project2 = /home/webs/Projects/Wordpress_site2
```

### กำหนด directory สำหรับเก็บ backup file ให้ไปแก้ไขที่ section "database_backup_path" 
โดยให้มีรูปแบบ ดังต่อไปนี้ 
```
[database_backup_path]
path = { directory ที่เราทำการ สร้างไว้ )  
```
ดัวอย่าง 

```
[database_backup_path]
path = { directory ที่เราทำการ สร้างไว้ )
```
### กำหนด จำนวน file sql ก่อนที่จะทำการ rotate ให้ไปแก้ไขที่ section "backup_policy"
โดยให้มีรูปแบบ ดังต่อไปนี้ 
```
[backup_policy]
rotate = { จำนวน sql ที่จะมีได้ ก่อนทำการ rotate }  
```
ตัวอย่าง 
```
[backup_policy]
rotate = 7 
```
