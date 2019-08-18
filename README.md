<h1 align="center">Welcome to Asistent František</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.2-blue.svg?cacheSeconds=2592000" />
  <a href="https://soosops.eu/licenses/llnmvp.pdf">
    <img alt="License: LL-NMV-P" src="https://img.shields.io/badge/license-LL--NMV--P-green" />
  </a>
  <a href="https://twitter.com/loupeznik01">
    <img alt="Twitter: loupeznik01" src="https://img.shields.io/twitter/follow/loupeznik01.svg?style=social" target="_blank" />
  </a>
</p>

> František je osobní asistent provádějící úlohy na základě hlasových příkazů uživatele. <br>

## Funkce

- František umí zapínat programy, ke kterým má přístup pomocí zástupců umístěných ve složce src
- František umí vykopávat uživatele z TeamSpeak serveru pomocí jednoduchého příkazu
- Vypnout PC

##Syntax hlasových příkazů

Pro spuštění programu: *"Františku [jméno zástupce programu]"* <br>
Pro vykopnutí uživatele z TeamSpeak serveru: *"Františku TeamSpeak query kopni [jméno uživatele TS]"* <br>
Pro vypnutí počítače: *"Františku vypni stroj"*

## Instalace & požadavky

Požadované nástroje:
- Python 3.7 a vyšší
- SpeechRecognition
- PyAudio
- ts3query

Instalace knihoven:

```pip install SpeechRecognition``` <br>
```pip install ts3query``` <br>
```pipwin install pyaudio``` (je nutné použít pipwin, přes pip nelze knihovna stáhnout) <br>

Testováno pouze na systému Windows

## Author

🧔 **Loupeznik**

* Twitter: [@loupeznik01](https://twitter.com/loupeznik01)
* Github: [@Loupeznik](https://github.com/Loupeznik)

## 📝 License

Copyright © 2019 [Loupeznik](https://github.com/Loupeznik).<br />
This project is [LL-NMV-P](https://soosops.eu/licenses/llnmvp.pdf) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_