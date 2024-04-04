import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OrdinalEncoder 

user_id = input("Kullanıcı Id'nizi Giriniz:\n")
print(user_id)
# Veriyi pandas ile okuyoruz. Verinin başlık satırı yok ise names parametresinde belirterek
# başlıkları satır olarak verisetinin başına ekliyoruz.
rating = pd.read_csv('Veriseti/steam-200k.csv', names=["userId", "gameName", 
                                                     "purchase", "hoursPlayed", "null"])
# şimdilik purchase keywordünü içeren satırları kullanmayıp sadece play keywordünü içeren
# satırları filtreden geçirerek verisetimizi güncelliyoruz.
rating = rating[rating.purchase == 'play']
# indexleri resetliyoruz.
rating = rating.reset_index(drop=True)
# userId - gameName - hoursPlayed kolonları içerecek şekilde tablosunu oluşturduk.
data = rating[['userId', 'gameName', 'hoursPlayed']]
# ilgili tabloyu okuttuk.
print(data)


# vg_sales verisetinden elde ettiğimiz benzer isimli oyunları çekiyoruz.
similar_named_games = pd.read_csv('Veriseti/close_matched_games.csv', names=["gameNameAfter", "gameName"], delimiter=';')
# oyunları yeni verisetindeki oyunlar ile güncelleyebilmek için merge ediyoruz.
data = pd.merge(data, similar_named_games)
# oyun adları sütunumuzu güncelliyoruz.
data['gameName'] = data['gameNameAfter']
# artık gerek olmayan gameNameAfter sütununu siliyoruz.
del data['gameNameAfter']
# son halini okutuyoruz.
print(data)

# vg_sales verisetini content based filtreleme için dosyadan okuyoruz.
vg_sales = pd.read_csv('Veriseti/vgsales.csv')
# Name sütununun adını gameName olarak değiştiriyoruz.
vg_sales = vg_sales.rename(columns={'Name': 'gameName'})
# Daha sonra oyunların adlarının yer aldığı sütunu ve türlerini çekiyoruz.
data2 = vg_sales[['gameName', 'Genre']]

# elde ettiğimiz dataFrame verisini okutuyoruz.
print(data2)


# son olarak verisetimize oyun türlerini dahil edebilmek için data2 veriseti ile
# bir merge işlemi daha gerçekleştiriyoruz.
data = pd.merge(data, data2, on='gameName', how='left')
# duplicate'lerden arındırıp güncel halini elde ediyoruz.
data.drop_duplicates(subset=['userId', 'gameName'],
                     keep = 'last', inplace = True)
# son halini okutuyoruz.
print(data)
# İlgili kullanıcı için oynanılan oyunları, kategorileri ile birlikte getiriyoruz.
category = data[data['userId'] == int(user_id)]
# çektiğimiz oyunları okutuyoruz.
print(category)
# creating bool series False for NaN values
bool_series = pd.notnull(data["Genre"])
 
# Sadece dolu olan değerleri içeren kayıtları atıyoruz.
test_data_d = data[bool_series]
# Atamamızı yazdırıyoruz.
print(test_data_d)
# Genre'lerde karşılığı olmayan null değerleri ayıklıyoruz.
category2 = pd.notnull(category["Genre"])
# Boş olan değerleri elediğimiz dataframe atamasını sağlıyoruz.
category3 = category[bool_series]
# Atadığımız halini yazdırıyoruz.
print(category3)
# Transform için gereken nesneyi tanımlıyoruz.
oe = OrdinalEncoder() 
#Atama yapacağımız kolonu seçiyoruz.
cols = ['gameName']
# Transform işlemini gerçekleştiriyoruz.
category3[cols] = oe.fit_transform(category3[cols]) 
# Train ve test için x verisini hazırlıyoruz.
X = category3[cols]
# Train ve test için y verisini hazırlıyoruz.
y = category3['Genre']
# Train ve test verilerini ayırıyoruz.
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)
# Knn değişkenini ayarlıyoruz.
classifier = KNeighborsClassifier(n_neighbors=5)
# Eğitimi gerçekleştiriyoruz.
classifier.fit(X_train, y_train)
# Eğitimin skoruna bakıyoruz.
classifier.score(X_test, y_test)

# En çok oynanan oyunu seçiyoruz.
most_played = category3.head(1)
# En çok oynanan oyunun kolonunu alıyoruz.
most_played_game = most_played['gameName']
# Array formatına dönüştürüyoruz.
test = np.array([most_played_game])
# test düzenini ayarlıyoruz.
test = test.reshape(1, -1)
# En uygun kategori için tahminleme işlemini gerçekleştiriyoruz.
print('En çok oynanılan kategori: ' + classifier.predict(test))
#En uygun kategori için tahminlemeyi değişkene atıyoruz.
most_genre = classifier.predict(test)

# İkinci eğitimimiz için verileri düzenliyoruz.
data_egitim = test_data_d[['gameName', 'Genre', 'hoursPlayed']]
# Grup işlemini gerçekleştiriyoruz.
data_egitim2 = data_egitim.groupby(['gameName','Genre'],as_index = False)['hoursPlayed'].sum()
# Sıralama işlemini gerçekleştiriyoruz.
data_egitim2 = data_egitim2.sort_values('hoursPlayed', ascending=False)
# Veriyi yazdırıyoruz.
print(data_egitim2)

# Transofrm işlemi için gereken nesneyi tanımlıyoruz.
oe2 = OrdinalEncoder()
# Kategori kolonunu seçiyoruz.
cols2 = ['Genre']
# Transform öncesi kategoriyi tutmak için kopyalama işlemi gerçekleştiriyoruz.
dt_test = data_egitim2.copy()
# Transform işlemi gerçekleştiriyoruz.
data_egitim2[cols2] = oe2.fit_transform(data_egitim2[cols2]) 
# Transform incesi ve sonrası listeleri merge ediyoruz.
data_merged = pd.merge(dt_test, data_egitim2, on='gameName', how='outer')

# İkinci eğitim için x verisini ayarlıyoruz.
X2 = data_egitim2[cols2]
# İkinci eğitim için y verisini ayarlıyoruz.
y2 = data_egitim2['gameName']
# Train ve test verilerini ayırıyoruz.
X_train, X_test, y_train, y_test = train_test_split(X2, y2, train_size=0.7, random_state=42)
# Knn ayarlarını yapıyoruz.
kumeleme = KNeighborsClassifier(n_neighbors=5)
# Eğitimi gerçekleştiriyoruz.
kumeleme.fit(X_train, y_train)
# Eğitimin skoruna bakıyoruz.
kumeleme.score(X_test, y_test)

# Önerilecek kategorinin transform öncesi değerinden transform sonrası değerini bulmak 
# için seçim yapıyoruz.
aa = data_merged[data_merged['Genre_x'] == str(most_genre[0])]
# Çoklu kayıtlardan arındırıyoruz.
aa.drop_duplicates(subset=['Genre_y'], keep = 'last', inplace = True)

# Transofrm işlemi için gereken nesneyi tanımlıyoruz.
oe3 = OrdinalEncoder()
# Array'e cast ediyoruz.
test3 = np.array([aa["Genre_y"]])
# Düzenlemesini sağlıyoruz.
most_genre2 = test3.reshape(1, -1)
# Sonuç olarak en uygun kategoriye göre en uygun oyun önerisini gerçekleştiriyoruz.
print('Önerilen Oyun: ' + kumeleme.predict(most_genre2))