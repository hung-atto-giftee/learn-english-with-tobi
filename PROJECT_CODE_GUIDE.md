# Phan Tich Code Cho Nguoi Moi

Tai lieu nay giup ban doc va hoc du an theo goc nhin cua nguoi moi bat dau voi Python, FastAPI, React va cach frontend giao tiep voi backend.

## 1. Du an nay lam gi?

Day la mot he thong hoc nghe tieng Anh.

Backend FastAPI se:
- tao file audio tu van ban bang `edge-tts`
- tao audio phat am cho tung tu trong dictionary popup
- cham bai dictation bang `difflib`
- quan ly dang nhap bang JWT
- luu lich su hoc tap vao PostgreSQL
- luu tu dien vao SQLite cache

Frontend React se:
- cho nguoi dung nhap doan van
- tach thanh tung cau
- goi backend de tao audio
- cho nguoi dung nhap lai cau nghe duoc
- hien ket qua cham bai
- tra tu, xem lich su hoc va tu vung

Neu ban hoc tot du an nay, ban se hoc duoc:
- Python co ban va to chuc code backend
- FastAPI route, service, auth, database
- React state, effect, router, auth context
- cach frontend va backend noi chuyen voi nhau qua API

## 2. Kien truc tong quan

Du an duoc tach thanh 2 phan:

### Backend

Thu muc: [app](/Users/hungatto/Desktop/tts-learn-listening/app)

Nhan chinh:
- [main.py](/Users/hungatto/Desktop/tts-learn-listening/app/main.py): diem khoi dong FastAPI
- [tts.py](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py): tao file mp3
- [evaluator.py](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py): cham bai dictation
- [database.py](/Users/hungatto/Desktop/tts-learn-listening/app/database.py): ket noi PostgreSQL va tao bang
- [auth/](/Users/hungatto/Desktop/tts-learn-listening/app/auth): dang ky, dang nhap, JWT
- [routes/training.py](/Users/hungatto/Desktop/tts-learn-listening/app/routes/training.py): `/tts`, `/practice`, `/evaluate`
- [history/](/Users/hungatto/Desktop/tts-learn-listening/app/history): lich su hoc tap
- [dictionary/](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary): tra tu, cache, lich su tra tu

### Frontend

Thu muc: [frontend/src](/Users/hungatto/Desktop/tts-learn-listening/frontend/src)

Nhan chinh:
- [main.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/main.jsx): diem mount app React
- [App.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/App.jsx): route toan app
- [lib/api.js](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/lib/api.js): ham goi API
- [auth/AuthContext.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/auth/AuthContext.jsx): quan ly token va user
- [pages/PracticePage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx): man hinh hoc chinh
- [pages/HistoryPage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/HistoryPage.jsx): lich su hoc
- [pages/VocabularyPage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/VocabularyPage.jsx): tu vung va dictionary search
- [components/DictionaryModal.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/DictionaryModal.jsx): popup nghia cua tu
- [components/Word.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/Word.jsx): render tung tu co the click

## 3. Nen doc theo thu tu nao?

Neu ban moi hoc, day la thu tu doc rat hop ly:

1. [README.md](/Users/hungatto/Desktop/tts-learn-listening/README.md)
2. [app/main.py](/Users/hungatto/Desktop/tts-learn-listening/app/main.py)
3. [app/routes/training.py](/Users/hungatto/Desktop/tts-learn-listening/app/routes/training.py)
4. [app/tts.py](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py)
5. [app/evaluator.py](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py)
6. [app/auth/utils.py](/Users/hungatto/Desktop/tts-learn-listening/app/auth/utils.py)
7. [app/database.py](/Users/hungatto/Desktop/tts-learn-listening/app/database.py)
8. [app/dictionary/service.py](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/service.py)
9. [frontend/src/App.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/App.jsx)
10. [frontend/src/auth/AuthContext.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/auth/AuthContext.jsx)
11. [frontend/src/lib/api.js](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/lib/api.js)
12. [frontend/src/pages/PracticePage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)
13. [frontend/src/pages/VocabularyPage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

Ly do:
- ban se thay duoc luong du lieu chinh truoc
- sau do moi di vao auth, database va dictionary
- ben frontend cung doc tu route tong den page cu the

## 4. Backend FastAPI: hoc Python qua du an nay

### 4.1. Diem vao cua backend

File: [app/main.py](/Users/hungatto/Desktop/tts-learn-listening/app/main.py)

Day la file nen doc dau tien o backend.

No cho ban thay:
- app FastAPI duoc tao nhu the nao
- middleware CORS de frontend goi duoc API
- static files duoc mount o dau
- cac router duoc include vao app ra sao

Ban se thay:
- `init_db()` de tao bang PostgreSQL
- `init_dictionary_cache()` de tao cache SQLite cho dictionary
- `app.mount("/static/audio", ...)` de phuc vu file mp3

Khai niem Python/FastAPI ban hoc duoc:
- ham tao ung dung
- import module
- chia router thanh nhieu file
- khoi tao tai nguyen luc startup

### 4.2. Route training

File: [app/routes/training.py](/Users/hungatto/Desktop/tts-learn-listening/app/routes/training.py)

Day la trai tim cua app hoc nghe.

Co 4 endpoint chinh:
- `POST /tts`
- `POST /practice`
- `POST /evaluate`
- `GET /tts/word`

Ban hoc duoc:
- `pydantic` model de validate input
- `async def` cho cac tac vu bat dong bo
- `Depends(get_current_user)` de bat buoc dang nhap
- goi service function thay vi nhung het logic vao route

Vi du:
- `/practice` nhan mot cau
- goi `generate_audio_file(...)` 2 lan cho toc do thuong va cham
- tra ve 2 URL audio

Day la mot mau thiet ke backend rat tot cho nguoi moi:
- route nhan request
- service xu ly nghiep vu
- route tra response

### 4.3. TTS service

File: [app/tts.py](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py)

File nay rat de hoc Python vi ngan gon nhung thuc te.

No day ban:
- `Enum` trong Python
- `Path` de lam viec voi duong dan
- `async/await`
- goi thu vien ngoai `edge_tts`

Mot vai diem hay:
- `SpeechSpeed` chi cho phep `normal` va `slow`
- `RATE_BY_SPEED` la dictionary map toc do sang rate cua TTS
- `generate_audio_file()` sinh ten file bang `uuid4`
- `generate_word_audio_file()` luu file theo ten tu da normalize de tranh tao lai

Tu file nay ban co the hoc:
- cach viet code ro nghia
- cach tach hang so ra khoi business logic
- cach luu file tao ra vao mot thu muc rieng

### 4.4. Cham bai dictation

File: [app/evaluator.py](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py)

Neu ban moi hoc Python, file nay rat dang doc ky.

No dung:
- `re` de tach token
- `difflib.SequenceMatcher` de so sanh 2 cau

No tra ra:
- `accuracy`
- `diff`
- `correct_sentence`

Tu day ban hoc duoc:
- list
- dict
- vong lap `for`
- dieu kien `if/elif`
- cach bien mot bai toan "so sanh chuoi" thanh du lieu de frontend hien thi

Hay chu y:
- backend khong tra HTML
- backend tra JSON co cau truc ro rang
- frontend se dua vao `type` cua `diff` de to mau va hien thi loi

### 4.5. Authentication

Files:
- [app/auth/routes.py](/Users/hungatto/Desktop/tts-learn-listening/app/auth/routes.py)
- [app/auth/utils.py](/Users/hungatto/Desktop/tts-learn-listening/app/auth/utils.py)

Phan nay day ban nhieu kien thuc backend thuc te:
- hash password bang `bcrypt`
- tao JWT
- doc JWT de lay user hien tai
- OAuth2PasswordBearer trong FastAPI

Mot chi tiet rat dang hoc:
- password khong duoc luu plaintext
- code hash password truoc roi moi luu DB
- moi request can auth se di qua `get_current_user`

Khai niem quan trong:
- `create_access_token(...)`: tao token
- `authenticate_user(...)`: kiem tra email/password
- `get_current_user(...)`: xac minh token va lay user

Neu ban muon hoc backend dung cach, hay tu ve lai flow:

1. frontend goi `/auth/login`
2. backend verify password
3. backend tra JWT
4. frontend luu token
5. frontend gui token trong header `Authorization`
6. backend doc token o cac route duoc bao ve

### 4.6. Database PostgreSQL

File: [app/database.py](/Users/hungatto/Desktop/tts-learn-listening/app/database.py)

File nay cho ban thay cach backend ket noi DB that.

No dung:
- `psycopg`
- `.env`
- `load_dotenv(...)`

Ban hoc duoc:
- doc bien moi truong
- tao ket noi DB
- chay SQL thuan
- `fetchone()`, `fetchall()`
- ham helper de doc/ghi du lieu

Bang chinh:
- `users`
- `learning_history`
- `user_word_history`

Day la mot du an tot de hoc tu tu:
- ban chua can SQLAlchemy
- SQL hien ra ro rang
- de biet moi bang duoc dung vao viec gi

### 4.7. Dictionary service

Files:
- [app/dictionary/routes.py](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/routes.py)
- [app/dictionary/service.py](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/service.py)

Day la module nhieu kien thuc nhat.

No cho ban hoc:
- goi API ngoai bang `httpx`
- normalize du lieu
- cache vao SQLite
- retry/fallback khi API loi
- translation English sang Vietnamese
- luu lich su tra tu theo user

Phan nay co 2 database:
- PostgreSQL: luu du lieu nguoi dung va lich su user
- SQLite: luu cache dictionary de tra nhanh hon

Nhung y tuong backend rat hay:
- `normalize_word(word)` de tranh trung lap
- `get_word(word)` doc cache truoc
- `save_word(data)` dung upsert de khong luu duplicate
- `translate_to_vi(text)` tach rieng thanh 1 ham

Day la mot bai hoc cuc hay:
- code tot khong chi "chay duoc"
- code tot con phai nghi den caching, duplicate, fallback va performance

### 4.8. History module

Files:
- [app/history/routes.py](/Users/hungatto/Desktop/tts-learn-listening/app/history/routes.py)
- [app/history/service.py](/Users/hungatto/Desktop/tts-learn-listening/app/history/service.py)

Day la noi de hoc cach tach nghiep vu.

Tuong tu dictionary:
- route chi xu ly HTTP
- service lo xu ly data

Ban se hoc duoc cach:
- luu ket qua hoc moi lan `/evaluate`
- lay 50 ban ghi moi nhat
- tinh thong ke `average_accuracy`

## 5. Frontend React: hoc React qua du an nay

### 5.1. App va route

File: [frontend/src/App.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/App.jsx)

File nay day ban:
- React Router
- route public va protected route

Ban se thay:
- `/login`
- `/register`
- `/`
- `/history`
- `/vocabulary`

Neu ban moi hoc React, hay nho:
- React khong tu "co page"
- React dung router de map URL sang component

### 5.2. Auth context

File: [frontend/src/auth/AuthContext.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/auth/AuthContext.jsx)

Day la file rat quan trong de hoc state management co ban.

No quan ly:
- token
- user
- login
- register
- logout
- kiem tra session khi app vua mo

Ban hoc duoc:
- `createContext`
- `useContext`
- `useEffect`
- `useMemo`
- chia logic dung chung cho nhieu page

Hay de y flow:
- app mo len
- `useEffect` goi `/auth/me`
- neu token hop le thi lay user
- neu token hong thi xoa token

Day la mot mau rat thuc te cho app co auth.

### 5.3. Lop API chung

File: [frontend/src/lib/api.js](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/lib/api.js)

File nay nho nhung rat quan trong.

No giup:
- luu token vao `localStorage`
- tu dong gan `Authorization: Bearer ...`
- gom logic `fetch` ve mot cho

Tu day ban hoc duoc mot bai hoc frontend rat hay:
- khong nen viet `fetch(...)` lung tung moi file
- nen co 1 lop API dung chung

### 5.4. Practice page

File: [frontend/src/pages/PracticePage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)

Day la file lon nhat va cung la file giup ban hoc React nhanh nhat.

Ban se thay:
- `useState` cho rat nhieu state
- `useMemo` de tinh `currentSentence` va `currentWords`
- `useRef` de quan ly audio va dictionary cache
- nhieu ham async goi backend

Nhung bai hoc chinh:

#### Tach paragraph thanh cau

Ham `splitIntoSentences(paragraph)` day ban:
- regex trong JavaScript
- xu ly text input

#### Goi API practice

Ham `requestPractice(sentence)` day ban:
- cach goi backend
- bat loi bang `try/catch`
- xu ly `401`
- update state sau khi co response

#### Goi API evaluate

Ham `handleEvaluate()` day ban:
- gui du lieu nguoi dung len server
- nhan JSON ket qua
- luu vao state de render lai UI

#### Phat audio

Ham `playAudio(speed, rate = 1)` day ban:
- tao `Audio` object bang JavaScript
- doi `playbackRate`
- dung `useRef` de giu object audio giua nhieu lan render

#### Dictionary popup

Ham `handleWordClick(word)` day ban:
- cache phia frontend bang `Map`
- tranh goi lai API voi cung mot tu
- mo modal voi data da tra ve

Trong [DictionaryModal.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/DictionaryModal.jsx), ban se hoc them:
- cach them mot nut chuc nang vao popup
- cach goi `GET /tts/word?word=...`
- cach tao `Audio` object va phat phat am cua tu

Neu ban doc ky file nay, ban se hoc duoc:
- state la gi
- event handler la gi
- component render theo state nhu the nao
- vi sao app React phai chia trang thai ro rang

### 5.5. Vocabulary page

File: [frontend/src/pages/VocabularyPage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

Day la file cuc hay de hoc:
- search
- debounce
- pagination
- highlight tu khoa

Ban se thay:
- `searchInput`
- `debouncedSearch`
- `page`
- `pagination`

Flow:
- nguoi dung nhap search
- `useEffect` doi 300ms
- moi cap nhat `debouncedSearch`
- `useEffect` khac goi `/dictionary/list`

Day la mot bai hoc frontend rat thuc te:
- khong nen goi API moi khi user vua bam 1 ky tu
- debounce giup toi uu request

### 5.6. Modal va component nho

Files:
- [frontend/src/components/DictionaryModal.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/DictionaryModal.jsx)
- [frontend/src/components/Word.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/Word.jsx)
- [frontend/src/components/ProtectedRoute.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/ProtectedRoute.jsx)

Day la bai hoc ve component hoa.

Hay nho:
- component nho de doc
- de test
- de tai su dung

Vi du:
- `ProtectedRoute` giu logic bao ve route
- `Word` giu logic hien 1 tu co the click
- `DictionaryModal` giu logic hien popup

## 6. Luong du lieu trong he thong

Hay hinh dung 1 buoi hoc cua nguoi dung:

1. User dang nhap tren frontend
2. Frontend luu JWT vao `localStorage`
3. User nhap paragraph
4. Frontend tach thanh tung cau
5. Frontend goi `POST /practice`
6. Backend tao 2 file audio
7. Frontend phat audio
8. User nhap cau nghe duoc
9. Frontend goi `POST /evaluate`
10. Backend cham bai va luu `learning_history`
11. Frontend hien accuracy va diff
12. User click 1 tu
13. Frontend goi `GET /dictionary?word=...`
14. Backend check cache SQLite
15. Neu chua co thi goi dictionary API + translation API
16. Backend luu cache va luu `user_word_history`
17. Frontend hien modal nghia cua tu

Neu ban muon hoc fullstack dung cach, hay doc code theo luong nay.

## 7. Ban hoc duoc gi ve Python?

Tu du an nay, ban co the hoc Python theo tung tang:

### Muc co ban

- bien, ham, `if`, `for`
- `dict`, `list`, `str`
- import module
- tach code thanh file

### Muc trung binh

- `async def` va `await`
- `Enum`
- `Path`
- regex
- `try/except`
- type hints nhu `dict[str, Any]`

### Muc backend thuc te

- FastAPI
- Pydantic model
- JWT
- bcrypt
- PostgreSQL
- SQLite cache
- goi API ngoai bang `httpx`

## 8. Ban hoc duoc gi ve React?

### Muc co ban

- component function
- JSX
- props
- event handler

### Muc trung binh

- `useState`
- `useEffect`
- `useMemo`
- `useRef`
- React Router

### Muc app thuc te

- auth context
- protected routes
- API layer
- loading state
- empty state
- modal
- search debounce
- pagination

## 9. Cach doc code cho de hieu

Day la cach doc code rat hop voi nguoi moi:

### Cach 1: Doc tu tren xuong

Vi du voi [app/routes/training.py](/Users/hungatto/Desktop/tts-learn-listening/app/routes/training.py):
- doc model request truoc
- doc route
- xem route goi service nao
- mo service do ra doc tiep

### Cach 2: Lan theo 1 tinh nang

Vi du tinh nang dictionary:
- frontend click tu trong [PracticePage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)
- goi [api.js](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/lib/api.js)
- backend nhan o [routes.py](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/routes.py)
- xu ly o [service.py](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/service.py)
- tra JSON ve frontend
- frontend render o [DictionaryModal.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/DictionaryModal.jsx)

### Cach 3: Them log tam thoi

Neu chua hieu code chay the nao, hay them:

```python
print("payload:", payload)
print("result:", result)
```

hoac ben React:

```js
console.log("practiceData", practiceData);
```

Day la cach hoc rat thuc te.

## 10. Bai tap tu hoc rat hop voi du an nay

Neu ban muon hoc nhanh, hay tu lam nhung bai nho sau:

### Bai 1

Them toc do audio moi:
- `very_slow = "-40%"`

Ban se sua:
- [app/tts.py](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py)
- [frontend/src/pages/PracticePage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)

### Bai 2

Them endpoint `/profile`

Ban se hoc:
- auth
- route moi
- tra JSON user

### Bai 3

Them filter accuracy cao/thap o lich su hoc

Ban se sua:
- backend history route
- frontend history page

### Bai 4

Them nut "Save favorite word"

Ban se hoc:
- them bang DB
- them route
- them button frontend

### Bai 5

Hien thi them so tu sai trong ket qua evaluate

Ban se sua:
- [app/evaluator.py](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py)
- [frontend/src/pages/PracticePage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)

## 11. Nhung bai hoc ve thiet ke code

Du an nay cung day ban cach to chuc code cho sach:

### Tach route va service

Khong de route lam qua nhieu viec.

Tot:
- route nhan request
- service xu ly logic
- database helper xu ly luu/doc du lieu

### Tach auth thanh module rieng

Auth la phan de roi, nen tach rieng se de bao tri hon.

### Cache dictionary

Khong phai luc nao cung goi API ngoai.

Do la bai hoc quan trong:
- giam request
- nhanh hon
- on dinh hon

### Frontend co lop API rieng

Khong de token va fetch nam tung page.

## 12. Mot vai tu khoa quan trong ban nen nho

- `async`: chay bat dong bo
- `await`: doi ket qua cua ham async
- `JWT`: token xac thuc user
- `bcrypt`: hash password
- `route`: duong dan API
- `service`: noi chua business logic
- `state`: du lieu thay doi trong React
- `effect`: logic chay khi component mount hoac khi dependency doi
- `cache`: luu tam ket qua de dung lai nhanh hon
- `upsert`: neu co roi thi update, chua co thi insert

## 13. Goi y cach hoc trong 7 ngay

### Ngay 1

Doc:
- [README.md](/Users/hungatto/Desktop/tts-learn-listening/README.md)
- [app/main.py](/Users/hungatto/Desktop/tts-learn-listening/app/main.py)
- [frontend/src/App.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/App.jsx)

Muc tieu:
- hieu tong quan app

### Ngay 2

Doc:
- [app/tts.py](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py)
- [app/routes/training.py](/Users/hungatto/Desktop/tts-learn-listening/app/routes/training.py)

Muc tieu:
- hieu request/response va audio flow

### Ngay 3

Doc:
- [app/evaluator.py](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py)
- [frontend/src/pages/PracticePage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)

Muc tieu:
- hieu dictation va evaluation

### Ngay 4

Doc:
- [app/auth/utils.py](/Users/hungatto/Desktop/tts-learn-listening/app/auth/utils.py)
- [frontend/src/auth/AuthContext.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/auth/AuthContext.jsx)

Muc tieu:
- hieu auth fullstack

### Ngay 5

Doc:
- [app/database.py](/Users/hungatto/Desktop/tts-learn-listening/app/database.py)
- [app/history/service.py](/Users/hungatto/Desktop/tts-learn-listening/app/history/service.py)

Muc tieu:
- hieu DB va luu lich su

### Ngay 6

Doc:
- [app/dictionary/service.py](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/service.py)
- [frontend/src/pages/VocabularyPage.jsx](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

Muc tieu:
- hieu API ngoai, cache, search, pagination

### Ngay 7

Tu lam 1 tinh nang nho.

Vi du:
- them mot button moi
- them mot field moi vao DB
- them mot endpoint moi

Day la ngay giup ban chuyen tu "doc code" sang "viet duoc code".

## 14. Ket luan

Du an nay rat hop de hoc fullstack vi no co du:
- backend that
- frontend that
- auth
- database
- API ngoai
- audio
- dictionary
- history

Neu ban la nguoi moi, dung co gang doc tat ca trong 1 ngay.

Hay chon 1 luong cu the, vi du:
- login
- practice
- evaluate
- dictionary

roi lan theo request tu frontend sang backend va quay nguoc lai.

Do la cach hoc nhanh nhat.
