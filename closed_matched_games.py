# =============================================================================
# # Öncelikle iki verisetinde benzer isme sahip olan oyunlar çekebilmek için close_matched_games
# # adlı bir liste değişkeni oluşturduk.
# close_matched_games = np.asarray([])
# # Steam verisetindeki her oyunun vg_sales verisetindeki oyunlardan benzer isme sahip olanlarını
# # difflib kütüphanesi ile hesaplatarak listemize ekledik.
# i = 0
# for gameName in game['gameName']:
#     close_matched_games = np.append(close_matched_games, values = ([gameName], difflib.get_close_matches(gameName, data2['gameName'])[:1] or None))
#     i = i + 1
#     if i > 10:
#         break
#     
# print(close_matched_games)
# 
# # Son olarak elde ettiğimiz sonuçları csv olarak kaydettik.
# # NOT: Bu işlemi yapmamız ilk verisetindeki oyunlar ile ikinci verisetindeki oyunları
# # eşleştirip türlerini yeni bir DataFrame içinde ortaya koyabilmek için çok önemliydi.
# 
# np.savetxt("deneme.csv", close_matched_games, delimiter=",", fmt='%s')
# =============================================================================