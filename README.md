Repositori ini menyimpan kode sumber serta berbagai sumberdaya yang digunakan di laman [ghora.net/covid19](http://ghora.net/covid19).

Mengapa laman ini dibuat? ~~Ya terserah saya, dong.~~ Karena sejauh saya tahu, belum ada satu situs yang menyajikan data COVID-19 nasional secara terpusat dan mendetail hingga jenjang kabupaten/kota.

## Teknis
- Laman dibuat dengan HTML/CSS/JS stack, dengan pustaka... yang membosankan: jQuery, skeleton css. Tidak ada react bla bla bla di sini. Jadi, membosankan dan biasa saja. :)
- Laman di-*host* di *github page*. Mengapa? Gratis.
- Data langsung di-*scrap* di sisi *client* (peramban web) dan langsung ditampilkan jika memungkinkan. Jika tidak memungkinkan (dan sepertinya hampir selalu), data akan di-scrap dan disimpan dalam berjas JSON. Penggunaan DBMS sengaja dihindari. Mengapa? Agar tidak perlu bayar hosting. Fufufu.
- Scraping dengan berbagai macam pustaka:
  - beautifulsoup, pandas, json, requests, dll, dll.

## Metode scraping
Tentu saja *brute force*, karena saya tidak kenal orang dalam. Sumberdaya yang dimuat saat laman milik pemerintah dibuka, dianalisis satu-persatu. Ini dilakukan melalui *chrome developer tool* di tab *networks*. Sumberdaya yang ditengarai mengandung data terkait COVID-19 kemudian diunduh dan diformat hingga mudah untuk ditampilkan.

Terima kasih kepada developer laman web milik pemerintah yang menyajikan data yang sangat sulit untuk diakses (baca: di-scrap).

## Kontribusi
Anda dapat berkontribusi dengan melaporkan kesalahan pada laman [ghora.net/covid19](http://ghora.net/covid19) melalui surel hello[at]ghora.net. Lebih baik lagi jika anda membuka *issue* di repositori github ini.
Jika anda ingin berkontribusi untuk pengembangan laman ini, silakan *fork* dan buat *pull request*. Barangkali anda adalah ninja dengan kemampuan canggih.
