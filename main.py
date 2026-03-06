import sqlite3
def create_database():
    conn=sqlite3.connect("ogrenciler.db")
    cursor=conn.cursor()
    return conn, cursor

def create_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    class INTEGER)
    ''')
    print("Başarılı bir şekilde oluşturuldu.")

def menu():
    print("Öğrenci Sistemi")
    print("1. Öğrenci Ekle")
    print("2. Öğrencileri Listele")
    print("3. Öğrenci Sil")
    print("4. Öğrenci Güncelle")
    print("5. Öğrenci Ara")
    print("6. Programdan çık")
    secim=input("Yapmak istediğiniz işlemi seçin:")
    return secim

def ogrenci_ekle(cursor, conn):
    isim=input("Öğrenci ismini giriniz:")
    yas=input("öğrenci yaşını giriniz:")
    sinif=input("öğrencinin sınıfını giriniz:")
    sorgu = "INSERT INTO Students (name, age, class) VALUES (?, ?, ?)"
    cursor.execute(sorgu, (isim,yas,sinif))
    conn.commit()
    print(f"{isim} başarıyla kaydedildi.")

def ogrenci_listele(cursor):
    cursor.execute("SELECT * FROM Students")
    ogrenci=cursor.fetchall()
    for i, row in enumerate(ogrenci, start=1):
        print(f"{i}. Sırada -> [Gerçek ID: {row[0]}] İsim: {row[1]}, Sınıf: {row[3]}")

def ogrenci_sil(cursor,conn):
    ogrenci_listele(cursor)
    silinecek_id=input("Silmek istediğiniz id numarasını giriniz:")
    sorgu="DELETE FROM Students WHERE id=? "
    cursor.execute(sorgu,(silinecek_id,))
    if cursor.rowcount>0:
        print(f"ID: {silinecek_id} olan kayıt silindi.")
    else:
        print(f"{silinecek_id} id numaralı öğrenci yok tekrar deneyiniz.")

def ogrenci_guncelle(cursor,conn):
    ogrenci_listele(cursor)
    guncellenecek_id = input("Güncellemek istediğiniz öğrencinin id numarasını girin: ")

    cursor.execute("SELECT * FROM Students WHERE id = ?", (guncellenecek_id,))
    ogrenci = cursor.fetchone()

    if ogrenci:
        yeni_isim = input("Yeni isim giriniz (yoksa boş geçiniz): ")
        yeni_yas = input("Yeni yaş giriniz (yoksa boş geçiniz): ")
        yeni_sinif = input("Yeni sınıf giriniz (yoksa boş geçiniz): ")

        if yeni_isim:
            cursor.execute("UPDATE Students SET name = ? WHERE id = ?", (yeni_isim, guncellenecek_id))
        if yeni_yas:
            cursor.execute("UPDATE Students SET age = ? WHERE id = ?", (yeni_yas, guncellenecek_id))
        if yeni_sinif:
            cursor.execute("UPDATE Students SET class = ? WHERE id = ?", (yeni_sinif, guncellenecek_id))

        conn.commit()
        print(f"ID: {guncellenecek_id} başarıyla güncellendi.")

    else:
        print(f" {guncellenecek_id} id numaralı bir öğrenci bulunamadı!")

def ogrenci_ara(cursor):
    aranilan_ogrenci=input("Aramak istediğiniz ismi girin: ")
    aranacak_deger=f"%{aranilan_ogrenci}%"
    cursor.execute("SELECT * FROM Students WHERE name LIKE ?",(aranacak_deger,))
    ogrenciler=cursor.fetchall()
    if ogrenciler:
        print(f"{aranilan_ogrenci} var.")
        for i, row in enumerate(ogrenciler, start=1):
            print(f"{i}. Sırada -> [Gerçek ID: {row[0]}] İsim: {row[1]}, Sınıf: {row[3]}")

    else:
        print(f"{aranilan_ogrenci}yok.")


def main():
    conn, cursor=create_database()
    try:
        create_table(cursor)
        while True:
            islem=menu()
            if islem=="1":
                ogrenci_ekle(cursor, conn)
            elif islem=="2":
                ogrenci_listele(cursor)
            elif islem=="3":
                ogrenci_sil(cursor,conn)
            elif islem=="4":
                ogrenci_guncelle(cursor, conn)
            elif islem=='5':
                ogrenci_ara(cursor)
            elif islem=="6":
                break
            else:
                print("Geçersiz işlem girdiniz tekrar deneyin.")
        conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

if __name__=="__main__":
    main()
